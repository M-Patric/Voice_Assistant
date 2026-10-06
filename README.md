# Python Voice Assistant

A Python-based voice assistant that listens to spoken commands, converts speech to text, identifies the user's intent using a local machine-learning NLP model, performs useful actions, and responds using text-to-speech.

This project was developed as part of the OASIS INFOBYTE Python Programming Internship.

---

## Features

### Core Voice Features

- Microphone-based voice input
- Speech-to-text using `SpeechRecognition`
- Text-to-speech using `pyttsx3`
- Continuous command listening
- Background-noise calibration
- Audio quality checks
- Graceful speech-recognition error handling
- Graceful application shutdown

### NLP and Intent Detection

- Local machine-learning intent classifier
- NLTK-based text preprocessing
- Word-level TF-IDF features
- Character-level TF-IDF features
- Logistic Regression classification
- Confidence-based prediction filtering
- Prediction-margin filtering for ambiguous commands
- Free-form natural-language command handling

### Web Features

- Open YouTube
- Open Google
- Open GitHub
- Search the web using Google
- Custom web commands loaded from JSON

### Productivity Features

- Timed reminders
- Audible reminder alerts
- Current time reporting
- Current date reporting
- Local general-knowledge responses

### Weather

- Live weather information using the OpenWeather API
- Temperature
- Weather description
- Humidity
- Wind speed
- API error handling
- Invalid-city handling
- Network timeout handling

### Email

- Voice-controlled email composition
- Spoken email address normalization
- Email address validation
- Gmail SMTP integration
- Subject and message collection by voice
- Send confirmation before transmission
- SMTP error handling

### Customization

Custom commands can be added through:

```text
assistant_commands.json