# Live Translation App

A real-time speech transcription and translation web application.

## How it works

1. **Speech-to-Text** - The browser's [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API) captures your microphone audio and transcribes it to text in real time.
2. **Translation** - Each completed sentence is sent to the Flask backend, which translates it using `googletrans` and returns the result instantly.
3. **Display** - Both the original transcript and the translated text are displayed side-by-side and update live as you speak.

## Supported languages

The app supports 16+ languages for speech input and 23+ target languages for translation, including English, Spanish, French, German, Chinese, Japanese, Korean, Arabic, Hindi, and more.

## Quick start

```bash
cd live-translation-app

# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py
```

Then open **http://localhost:5000** in **Chrome**, **Edge**, or **Safari** (these browsers support the Web Speech API).

## Usage

1. Select the language you will **speak in** (source).
2. Select the language you want to **translate to** (target).
3. Click the microphone button to start recording.
4. Speak naturally — your words appear in the left panel, and the translation appears in the right panel in real time.
5. Click the microphone again to stop.

## Requirements

- Python 3.8+
- A modern browser with Web Speech API support (Chrome recommended)
- Microphone access
