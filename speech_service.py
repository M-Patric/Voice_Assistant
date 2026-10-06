import speech_recognition as sr
import pyttsx3
import threading
import math
from array import array
import sys

from config import debug_print


# ==================================================
# INITIALIZE SPEECH SYSTEMS
# ==================================================

recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Prevent multiple threads from using the
# text-to-speech engine simultaneously.
speech_lock = threading.Lock()


# ==================================================
# SPEAK
# ==================================================

def speak(text):
    """
    Converts text into speech and speaks it aloud.

    A lock ensures that the main program and
    reminder threads do not use the speech engine
    simultaneously.
    """

    with speech_lock:

        engine.say(text)

        engine.runAndWait()


# ==================================================
# AUDIO RMS
# ==================================================

def calculate_audio_rms(audio):
    """
    Calculates the Root Mean Square (RMS) strength
    of captured audio.
    """

    raw_data = (
        audio.get_raw_data()
    )

    sample_width = (
        audio.sample_width
    )

    if not raw_data:

        return 0.0

    if sample_width == 2:

        samples = array(
            "h",
            raw_data
        )

        if sys.byteorder != "little":

            samples.byteswap()

        if not samples:

            return 0.0

        mean_square = (
            sum(
                sample * sample
                for sample in samples
            )
            / len(samples)
        )

        return math.sqrt(
            mean_square
        )

    if sample_width == 1:

        samples = array(
            "B",
            raw_data
        )

        if not samples:

            return 0.0

        centered_samples = [
            sample - 128
            for sample in samples
        ]

        mean_square = (
            sum(
                sample * sample
                for sample in centered_samples
            )
            / len(centered_samples)
        )

        return math.sqrt(
            mean_square
        )

    return None


# ==================================================
# AUDIO LENGTH CHECK
# ==================================================

def audio_is_long_enough(
    audio,
    minimum_seconds=0.35
):
    """
    Rejects extremely short audio captures that are
    unlikely to contain meaningful speech.
    """

    minimum_bytes = int(
        audio.sample_rate
        * audio.sample_width
        * minimum_seconds
    )

    return (
        len(audio.frame_data)
        >= minimum_bytes
    )


# ==================================================
# AUDIO SPEECH CHECK
# ==================================================

def audio_is_likely_speech(audio):
    """
    Performs a lightweight audio-strength check before
    speech recognition.
    """

    rms = calculate_audio_rms(
        audio
    )

    # If the audio format cannot be evaluated,
    # allow speech recognition to decide.
    if rms is None:

        return True

    energy_threshold = (
        recognizer.energy_threshold
    )

    minimum_rms = max(
        energy_threshold * 1.20,
        150
    )

    debug_print(
        f"Audio RMS: {rms:.2f}"
    )

    debug_print(
        f"Required RMS: {minimum_rms:.2f}"
    )

    return (
        rms >= minimum_rms
    )


# ==================================================
# LISTEN
# ==================================================

def listen():
    """
    Captures one spoken phrase.
    """

    with sr.Microphone() as source:

        print(
            "\nListening..."
        )

        audio = recognizer.listen(
            source,
            timeout=5,
            phrase_time_limit=10
        )

    return audio


# ==================================================
# ASK FOR SPEECH
# ==================================================

def ask_for_speech(prompt):
    """
    Speaks a prompt, listens for the response,
    and converts the response to text.

    Returns None when the response cannot be
    understood.
    """

    speak(
        prompt
    )

    try:

        audio = listen()

    except sr.WaitTimeoutError:

        print(
            "No response was detected."
        )

        speak(
            "I didn't hear a response. "
            "Please try again."
        )

        return None

    if not audio_is_long_enough(
        audio
    ):

        debug_print(
            "Very short audio was ignored."
        )

        speak(
            "I didn't hear a clear response. "
            "Please try again."
        )

        return None

    if not audio_is_likely_speech(
        audio
    ):

        debug_print(
            "Background noise was ignored."
        )

        speak(
            "I didn't hear a clear response. "
            "Please try again."
        )

        return None

    print(
        "Processing..."
    )

    try:

        response = (
            recognizer
            .recognize_google(
                audio
            )
            .strip()
        )

        debug_print(
            "You said:",
            response
        )

        return response

    except sr.UnknownValueError:

        print(
            "The response could not be understood."
        )

        speak(
            "Sorry, I couldn't understand "
            "your response."
        )

        return None

    except sr.RequestError:

        print(
            "Speech recognition service "
            "request failed."
        )

        speak(
            "There was a problem connecting "
            "to the speech recognition service."
        )

        return None


# ==================================================
# MICROPHONE PREPARATION
# ==================================================

def prepare_microphone():
    """
    Calibrates the microphone against background
    noise and applies the project's listening settings.
    """

    print(
        "Preparing the microphone..."
    )

    speak(
        "Please wait while I prepare "
        "the microphone."
    )

    with sr.Microphone() as source:

        print(
            "Adjusting for background noise..."
        )

        recognizer.adjust_for_ambient_noise(
            source,
            duration=1.5
        )

    recognizer.energy_threshold = max(
        recognizer.energy_threshold * 1.20,
        150
    )

    recognizer.dynamic_energy_threshold = False

    recognizer.phrase_threshold = 0.7

    recognizer.pause_threshold = 0.8

    recognizer.non_speaking_duration = 0.5

    print(
        "Microphone ready."
    )

    debug_print(
        "Energy threshold:",
        recognizer.energy_threshold
    )

    debug_print(
        "Phrase threshold:",
        recognizer.phrase_threshold
    )

    speak(
        "I am ready."
    )