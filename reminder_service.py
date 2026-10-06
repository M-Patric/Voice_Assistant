# ==================================================
# REMINDER SERVICE
# ==================================================

import re
import threading

from speech_service import speak


# ==================================================
# REMINDER ALERT
# ==================================================

def reminder_alert():
    """
    Speaks an audible alert when the reminder timer
    finishes.
    """

    print(
        "\n*** REMINDER DUE ***"
    )

    speak(
        "Your reminder is due."
    )


# ==================================================
# EXTRACT REMINDER DURATION
# ==================================================

def extract_reminder_duration(command):
    """
    Extracts a numeric duration and time unit.

    Supported units:
        seconds
        minutes
        hours

    Returns:
        (duration_in_seconds, readable_duration)

    or:

        (None, None)
    """

    pattern = (
        r"(\d+)\s*"
        r"(seconds?|secs?|minutes?|mins?|"
        r"hours?|hrs?)"
    )

    match = re.search(
        pattern,
        command
    )

    if not match:
        return None, None

    amount = int(
        match.group(1)
    )

    unit = match.group(2)

    # --------------------------------------------------
    # SECONDS
    # --------------------------------------------------

    if (
        unit.startswith("second")
        or unit.startswith("sec")
    ):

        seconds = amount

        readable_duration = (
            "1 second"
            if amount == 1
            else f"{amount} seconds"
        )

    # --------------------------------------------------
    # MINUTES
    # --------------------------------------------------

    elif (
        unit.startswith("minute")
        or unit.startswith("min")
    ):

        seconds = amount * 60

        readable_duration = (
            "1 minute"
            if amount == 1
            else f"{amount} minutes"
        )

    # --------------------------------------------------
    # HOURS
    # --------------------------------------------------

    elif (
        unit.startswith("hour")
        or unit.startswith("hr")
    ):

        seconds = amount * 60 * 60

        readable_duration = (
            "1 hour"
            if amount == 1
            else f"{amount} hours"
        )

    else:
        return None, None

    return (
        seconds,
        readable_duration
    )


# ==================================================
# SET REMINDER
# ==================================================

def set_reminder(command):
    """
    Extracts the reminder duration, starts a timer,
    and informs the user that the reminder has been set.
    """

    duration_seconds, readable_duration = (
        extract_reminder_duration(command)
    )

    if duration_seconds is None:

        speak(
            "I couldn't determine the reminder "
            "duration. Please say something like, "
            "remind me in 10 seconds."
        )

        return

    timer = threading.Timer(
        duration_seconds,
        reminder_alert
    )

    timer.daemon = True

    timer.start()

    print(
        f"Reminder set for {readable_duration}."
    )

    speak(
        f"Reminder set for {readable_duration}."
    )


# ==================================================
# MODULE TEST
# ==================================================

if __name__ == "__main__":

    print(
        "Testing reminder service..."
    )

    test_commands = [
        "remind me in 10 seconds",
        "set a reminder for 5 minutes",
        "remind me in 2 hours",
        "set a reminder",
    ]

    for command in test_commands:

        duration, readable = (
            extract_reminder_duration(command)
        )

        print(
            f"Command: {command}"
        )

        print(
            f"Duration in seconds: {duration}"
        )

        print(
            f"Readable duration: {readable}"
        )

        print("-" * 50)