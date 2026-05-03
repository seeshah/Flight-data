#!/usr/bin/env python3
"""Check Resy for Bungalow NYC openings on 2026-05-17 (party of 2, 5pm-10pm).

Designed to run from GitHub Actions. Writes outputs to $GITHUB_OUTPUT and
the matching-slots issue body to ./body.md when slots are found.

This tool only checks availability and emits an alert. It does not book.
Run no more frequently than every few minutes.
"""

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, time

VENUE_SLUG = "bungalow-ny"
TARGET_DATE = "2026-05-17"
PARTY_SIZE = 2
WINDOW_START = time(17, 0)
WINDOW_END = time(22, 0)

# Public API key embedded in resy.com's web client. Not a secret.
RESY_API_KEY = "VbWk7s3L4KiK5fzlO7JD3Q5EYolJI7n5"
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
VENUE_URL = f"https://resy.com/cities/new-york-ny/venues/{VENUE_SLUG}"


def resy_get(url: str) -> dict:
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f'ResyAPI api_key="{RESY_API_KEY}"',
            "User-Agent": USER_AGENT,
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://resy.com",
            "Referer": "https://resy.com/",
            "X-Origin": "https://resy.com",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read())


def get_venue_id(slug: str) -> int:
    data = resy_get(f"https://api.resy.com/3/venue?url_slug={slug}")
    return int(data["id"]["resy"])


def find_slots(venue_id: int, day: str, party_size: int) -> list:
    url = (
        "https://api.resy.com/4/find"
        f"?lat=0&long=0&day={day}&party_size={party_size}&venue_id={venue_id}"
    )
    data = resy_get(url)
    venues = data.get("results", {}).get("venues", [])
    if not venues:
        return []
    return venues[0].get("slots", [])


def slot_in_window(slot: dict) -> bool:
    start = slot.get("date", {}).get("start")
    if not start:
        return False
    dt = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
    return WINDOW_START <= dt.time() <= WINDOW_END


def write_outputs(found: bool, title: str = "", body: str = "") -> None:
    out_path = os.environ.get("GITHUB_OUTPUT")
    if not out_path:
        return
    with open(out_path, "a") as f:
        f.write(f"found={'true' if found else 'false'}\n")
        if found:
            f.write(f"title={title}\n")
    if found:
        with open("body.md", "w") as f:
            f.write(body)


def main() -> int:
    try:
        venue_id = get_venue_id(VENUE_SLUG)
        slots = find_slots(venue_id, TARGET_DATE, PARTY_SIZE)
    except urllib.error.HTTPError as e:
        print(f"Resy HTTP {e.code}: {e.reason}", file=sys.stderr)
        write_outputs(False)
        return 0
    except Exception as e:
        print(f"Resy request failed: {e}", file=sys.stderr)
        write_outputs(False)
        return 0

    matching = [s for s in slots if slot_in_window(s)]
    print(f"venue_id={venue_id} total_slots={len(slots)} matching={len(matching)}")
    if not matching:
        write_outputs(False)
        return 0

    lines = []
    for s in matching:
        start = s["date"]["start"]
        slot_type = s.get("config", {}).get("type", "")
        lines.append(f"- {start}" + (f" ({slot_type})" if slot_type else ""))

    title = (
        f"Bungalow availability {TARGET_DATE}: {len(matching)} slot(s) "
        f"between 5pm-10pm"
    )
    body = (
        f"Found {len(matching)} slot(s) for Bungalow NYC on {TARGET_DATE}, "
        f"party of {PARTY_SIZE}, between 5pm and 10pm:\n\n"
        + "\n".join(lines)
        + f"\n\nBook fast: {VENUE_URL}\n"
    )
    write_outputs(True, title, body)
    print(body)
    return 0


if __name__ == "__main__":
    sys.exit(main())
