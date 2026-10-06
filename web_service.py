# ==================================================
# WEB AND CUSTOM COMMAND SERVICE
# ==================================================

import json
import os
import webbrowser

from urllib.parse import quote

from config import CUSTOM_COMMANDS_FILE

from speech_service import speak


# ==================================================
# LOAD CUSTOM COMMANDS
# ==================================================

def load_custom_commands():
    """
    Loads custom commands from the JSON configuration file.

    Each command must map to a valid HTTP or HTTPS URL.

    Returns:
        dict: Valid custom commands.
    """

    if not os.path.exists(CUSTOM_COMMANDS_FILE):

        print(
            "Custom commands file was not found."
        )

        return {}

    try:

        with open(
            CUSTOM_COMMANDS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            commands = json.load(file)

        if not isinstance(commands, dict):

            print(
                "Custom commands file must contain "
                "a JSON object."
            )

            return {}

        valid_commands = {}

        for command, url in commands.items():

            if not isinstance(command, str):
                continue

            if not isinstance(url, str):
                continue

            normalized_command = (
                command.lower().strip()
            )

            normalized_url = url.strip()

            if not normalized_command:
                continue

            if not (
                normalized_url.startswith("http://")
                or normalized_url.startswith("https://")
            ):

                print(
                    f"Ignoring invalid URL for "
                    f"custom command: {command}"
                )

                continue

            valid_commands[
                normalized_command
            ] = normalized_url

        print(
            f"Loaded {len(valid_commands)} "
            f"custom command(s)."
        )

        return valid_commands

    except json.JSONDecodeError:

        print(
            "The custom commands file contains "
            "invalid JSON."
        )

        return {}

    except OSError as error:

        print(
            f"Could not read custom commands file: "
            f"{error}"
        )

        return {}


# ==================================================
# INITIALIZE CUSTOM COMMANDS
# ==================================================

CUSTOM_COMMANDS = load_custom_commands()


# ==================================================
# OPEN WEBSITE
# ==================================================

def open_website(website):
    """
    Opens a supported website in the default browser.
    """

    websites = {
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "github": "https://github.com",
    }

    url = websites.get(
        website
    )

    if url:

        webbrowser.open(url)

        speak(
            f"Opening {website}."
        )

    else:

        speak(
            "I don't know that website yet."
        )


# ==================================================
# OPEN CUSTOM COMMAND
# ==================================================

def open_custom_command(command):
    """
    Opens the URL associated with a custom command.
    """

    url = CUSTOM_COMMANDS.get(
        command
    )

    if not url:

        speak(
            "I couldn't find that custom command."
        )

        return

    webbrowser.open(
        url
    )

    speak(
        f"Opening {command}."
    )


# ==================================================
# WEB SEARCH
# ==================================================

def search_web(query):
    """
    Searches Google for the requested topic.
    """

    encoded_query = quote(
        query
    )

    url = (
        "https://www.google.com/search?"
        f"q={encoded_query}"
    )

    webbrowser.open(
        url
    )

    speak(
        f"Searching for {query}."
    )


# ==================================================
# EXTRACT SEARCH QUERY
# ==================================================

def extract_search_query(command):
    """
    Removes common search phrases from the command
    and returns the actual search topic.
    """

    search_phrases = [

        "search for ",

        "search ",

        "look up ",

        "look for ",

        "find information about ",

        "find information on ",

        "search the internet for ",
    ]

    for phrase in search_phrases:

        if command.startswith(phrase):

            return command.replace(
                phrase,
                "",
                1
            ).strip()

    return ""


# ==================================================
# MODULE TEST
# ==================================================

if __name__ == "__main__":

    print()
    print("Testing web service...")
    print()

    print(
        "Available custom commands:"
    )

    for command in CUSTOM_COMMANDS:

        print(
            f" - {command}"
        )

    print()

    test_search_commands = [
        "search python programming",
        "search for machine learning",
        "look up python tutorials",
        "look for programming courses",
        "find information about artificial intelligence",
    ]

    for command in test_search_commands:

        query = extract_search_query(
            command
        )

        print(
            f"Command: {command}"
        )

        print(
            f"Extracted query: {query}"
        )

        print(
            "-" * 50
        )