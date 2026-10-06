# ==================================================
# WEATHER SERVICE
# ==================================================

import os

import requests

from config import WEATHER_API_URL

from speech_service import speak


# ==================================================
# EXTRACT WEATHER CITY
# ==================================================

def extract_weather_city(command):
    """
    Extracts the city name from common weather commands.

    Returns:
        str: City name, or an empty string when no city
        can be extracted.
    """

    weather_phrases = [

        "what's the weather in ",

        "what is the weather in ",

        "tell me the weather in ",

        "weather in ",

        "weather for ",

        "what is the weather like in ",

        "how is the weather in ",

        "what is the temperature in ",
    ]

    for phrase in weather_phrases:

        if command.startswith(phrase):

            city = command.replace(
                phrase,
                "",
                1
            ).strip()

            return city

    return ""


# ==================================================
# GET WEATHER
# ==================================================

def get_weather(city):
    """
    Fetches current weather data from OpenWeather
    and speaks the result.

    The API key is loaded from the
    OPENWEATHER_API_KEY environment variable.
    """

    api_key = os.getenv(
        "OPENWEATHER_API_KEY"
    )

    # --------------------------------------------------
    # CHECK API CONFIGURATION
    # --------------------------------------------------

    if not api_key:

        speak(
            "The weather service API key "
            "has not been configured."
        )

        print(
            "OPENWEATHER_API_KEY environment "
            "variable was not found."
        )

        return

    # --------------------------------------------------
    # API REQUEST PARAMETERS
    # --------------------------------------------------

    params = {

        "q": city,

        "appid": api_key,

        "units": "metric",
    }

    # --------------------------------------------------
    # REQUEST WEATHER DATA
    # --------------------------------------------------

    try:

        response = requests.get(
            WEATHER_API_URL,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        # --------------------------------------------------
        # EXTRACT WEATHER INFORMATION
        # --------------------------------------------------

        temperature = (
            data["main"]["temp"]
        )

        humidity = (
            data["main"]["humidity"]
        )

        description = (
            data["weather"][0]["description"]
        )

        wind_speed = (
            data["wind"]["speed"]
        )

        # --------------------------------------------------
        # DISPLAY WEATHER
        # --------------------------------------------------

        print(
            f"Weather in {city}: "
            f"{temperature}°C, "
            f"{description}, "
            f"humidity {humidity}%, "
            f"wind {wind_speed} m/s"
        )

        # --------------------------------------------------
        # SPEAK WEATHER
        # --------------------------------------------------

        speak(
            f"The temperature in {city} is "
            f"{temperature:.1f} degrees Celsius. "
            f"The weather is {description}. "
            f"Humidity is {humidity} percent. "
            f"Wind speed is "
            f"{wind_speed:.1f} meters per second."
        )

    # --------------------------------------------------
    # TIMEOUT
    # --------------------------------------------------

    except requests.exceptions.Timeout:

        print(
            "Weather request timed out."
        )

        speak(
            "The weather service took too long "
            "to respond. Please try again."
        )

    # --------------------------------------------------
    # CONNECTION ERROR
    # --------------------------------------------------

    except requests.exceptions.ConnectionError:

        print(
            "Could not connect to the weather service."
        )

        speak(
            "I couldn't connect to the weather "
            "service. Please check your internet "
            "connection."
        )

    # --------------------------------------------------
    # HTTP ERROR
    # --------------------------------------------------

    except requests.exceptions.HTTPError as error:

        print(
            f"Weather API returned an HTTP error: "
            f"{error}"
        )

        status_code = response.status_code

        if status_code == 401:

            speak(
                "The weather API key is invalid "
                "or has not been activated."
            )

        elif status_code == 404:

            speak(
                f"I couldn't find weather data "
                f"for {city}."
            )

        else:

            speak(
                "The weather service returned "
                "an error. Please try again later."
            )

    # --------------------------------------------------
    # UNEXPECTED RESPONSE FORMAT
    # --------------------------------------------------

    except (
        KeyError,
        IndexError,
        TypeError
    ):

        print(
            "The weather response had "
            "an unexpected format."
        )

        speak(
            "I received unexpected weather data. "
            "Please try again."
        )

    # --------------------------------------------------
    # OTHER REQUEST ERRORS
    # --------------------------------------------------

    except requests.exceptions.RequestException:

        print(
            "An unexpected weather request "
            "error occurred."
        )

        speak(
            "I couldn't retrieve the weather right now."
        )


# ==================================================
# MODULE TEST
# ==================================================

if __name__ == "__main__":

    print()
    print("Testing weather service...")
    print()

    test_commands = [

        "what is the weather in Accra",

        "what's the weather in Kumasi",

        "tell me the weather in Takoradi",

        "what is the temperature in Accra",

        "weather in Cape Coast",

        "this does not contain a city",
    ]

    for command in test_commands:

        city = extract_weather_city(
            command.lower()
        )

        print(
            f"Command: {command}"
        )

        print(
            f"Extracted city: {city}"
        )

        print(
            "-" * 50
        )