# ==================================================
# VOICE ASSISTANT APPLICATION
# ==================================================

import datetime

import speech_recognition as sr

from speech_service import (
    recognizer,
    speak,
    listen,
    prepare_microphone,
    audio_is_long_enough,
    audio_is_likely_speech,
)

from nlp_engine import classify_intent

from reminder_service import set_reminder

from web_service import (
    CUSTOM_COMMANDS,
    open_website,
    open_custom_command,
    search_web,
    extract_search_query,
)

from weather_service import (
    extract_weather_city,
    get_weather,
)

from email_service import (
    compose_and_send_email,
)

from knowledge_service import (
    answer_general_question,
)


# ==================================================
# TELL CURRENT TIME
# ==================================================

def tell_time():
    """
    Gets the current time and speaks it to the user.
    """

    current_time = datetime.datetime.now().strftime(
        "%I:%M %p"
    )

    speak(
        f"The current time is {current_time}."
    )


# ==================================================
# TELL CURRENT DATE
# ==================================================

def tell_date():
    """
    Gets the current date and speaks it to the user.
    """

    current_date = datetime.datetime.now().strftime(
        "%A, %d %B %Y"
    )

    speak(
        f"Today is {current_date}."
    )


# ==================================================
# INTENT DETECTION
# ==================================================

def get_intent(command):
    """
    Determines the user's intent.

    Exact goodbye commands and custom commands are
    checked before the NLP classifier.

    All other commands are processed by the
    local NLP engine.
    """

    goodbye_phrases = [

        "goodbye",

        "goodbye assistant",

        "quit",

        "exit",

        "please shut down",

        "stop the assistant",
    ]

    # --------------------------------------------------
    # GOODBYE CHECK
    # --------------------------------------------------

    if command in goodbye_phrases:

        return "goodbye"

    # --------------------------------------------------
    # CUSTOM COMMAND CHECK
    # --------------------------------------------------

    if command in CUSTOM_COMMANDS:

        return "custom_command"

    # --------------------------------------------------
    # NLP CLASSIFICATION
    # --------------------------------------------------

    intent, confidence, margin = (
        classify_intent(command)
    )

    print(
        f"Detected intent confidence: "
        f"{confidence:.2f}"
    )

    print(
        f"Detected intent margin: "
        f"{margin:.2f}"
    )

    return intent


# ==================================================
# HANDLE INTENT
# ==================================================

def handle_intent(
    intent,
    command
):
    """
    Performs the appropriate action based on
    the detected intent.
    """

    if intent == "greeting":

        speak(
            "Hello! How can I help you?"
        )

    elif intent == "time":

        tell_time()

    elif intent == "date":

        tell_date()

    elif intent == "search":

        query = extract_search_query(
            command
        )

        if query:

            search_web(
                query
            )

        else:

            speak(
                "What would you like me "
                "to search for?"
            )

    elif intent == "open_youtube":

        open_website(
            "youtube"
        )

    elif intent == "open_google":

        open_website(
            "google"
        )

    elif intent == "open_github":

        open_website(
            "github"
        )

    elif intent == "custom_command":

        open_custom_command(
            command
        )

    elif intent == "reminder":

        set_reminder(
            command
        )

    elif intent == "weather":

        city = extract_weather_city(
            command
        )

        if city:

            get_weather(
                city
            )

        else:

            speak(
                "Please tell me the city "
                "you want the weather for."
            )

    elif intent == "knowledge":

        found_answer = (
            answer_general_question(
                command
            )
        )

        if not found_answer:

            speak(
                "I don't have an answer to that "
                "question in my local knowledge "
                "base yet."
            )

            print(
                "No knowledge base match found."
            )

    elif intent == "email":

        compose_and_send_email()

    elif intent == "goodbye":

        speak(
            "Goodbye. Have a great day."
        )

    else:

        speak(
            "I don't understand that command yet."
        )


# ==================================================
# MAIN PROGRAM
# ==================================================

def main():
    """
    Starts and runs the voice assistant.
    """

    prepare_microphone()

    while True:

        try:

            audio = listen()

        except sr.WaitTimeoutError:

            print(
                "Listening timed out."
            )

            speak(
                "I didn't hear anything. "
                "Please try again."
            )

            continue

        # --------------------------------------------------
        # AUDIO QUALITY CHECKS
        # --------------------------------------------------

        if not audio_is_long_enough(audio):

            print(
                "Very short audio was ignored."
            )

            speak(
                "I didn't hear a clear command. "
                "Please try again."
            )

            continue

        if not audio_is_likely_speech(audio):

            print(
                "Background noise was ignored."
            )

            speak(
                "I didn't hear a clear command. "
                "Please try again."
            )

            continue

        print(
            "Processing..."
        )

        try:

            # --------------------------------------------------
            # SPEECH TO TEXT
            # --------------------------------------------------

            text = recognizer.recognize_google(
                audio
            )

            print(
                "You said:",
                text
            )

            # --------------------------------------------------
            # NORMALIZE COMMAND
            # --------------------------------------------------

            command = (
                text.lower().strip()
            )

            # --------------------------------------------------
            # INTENT DETECTION
            # --------------------------------------------------

            intent = get_intent(
                command
            )

            print(
                "Final intent:",
                intent
            )

            # --------------------------------------------------
            # HANDLE GOODBYE
            # --------------------------------------------------

            if intent == "goodbye":

                handle_intent(
                    intent,
                    command
                )

                break

            # --------------------------------------------------
            # HANDLE NORMAL COMMAND
            # --------------------------------------------------

            handle_intent(
                intent,
                command
            )

        except sr.UnknownValueError:

            print(
                "Sorry, I didn't understand that."
            )

            speak(
                "Sorry, I didn't understand that."
            )

        except sr.RequestError:

            print(
                "There was a problem connecting "
                "to the speech recognition service."
            )

            speak(
                "There was a problem connecting "
                "to the speech recognition service."
            )

        except KeyboardInterrupt:

            print(
                "\nAssistant stopped by user."
            )

            speak(
                "Goodbye."
            )

            break

        except Exception as error:

            print(
                f"Unexpected application error: "
                f"{error}"
            )

            speak(
                "An unexpected error occurred. "
                "Please try that command again."
            )


# ==================================================
# START PROGRAM
# ==================================================

if __name__ == "__main__":

    main()