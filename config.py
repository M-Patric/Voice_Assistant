# ==================================================
# APPLICATION CONFIGURATION
# ==================================================

# Development diagnostics.
# Set to False for the final clean demo.
DEBUG = True


# --------------------------------------------------
# FILES
# --------------------------------------------------

CUSTOM_COMMANDS_FILE = "assistant_commands.json"


# --------------------------------------------------
# WEATHER API
# --------------------------------------------------

WEATHER_API_URL = (
    "https://api.openweathermap.org/data/2.5/weather"
)


# --------------------------------------------------
# EMAIL
# --------------------------------------------------

EMAIL_SMTP_HOST = "smtp.gmail.com"
EMAIL_SMTP_PORT = 587


# ==================================================
# DEBUG HELPER
# ==================================================

def debug_print(*messages):
    """
    Prints diagnostic information only when
    DEBUG mode is enabled.
    """

    if DEBUG:
        print(*messages)