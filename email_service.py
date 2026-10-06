# ==================================================
# EMAIL SERVICE
# ==================================================

import os
import re
import smtplib
import ssl

from email.message import EmailMessage

from config import (
    EMAIL_SMTP_HOST,
    EMAIL_SMTP_PORT,
)

from speech_service import (
    speak,
    ask_for_speech,
)


# ==================================================
# NORMALIZE SPOKEN EMAIL ADDRESS
# ==================================================

def normalize_email_address(email_text):
    """
    Converts a spoken-style email address into
    conventional email format.

    Examples:

        john at gmail dot com
        ->
        john@gmail.com

        john underscore doe at gmail dot com
        ->
        john_doe@gmail.com
    """

    email = email_text.lower().strip()

    replacements = {

        " at ": "@",

        " dot ": ".",

        " underscore ": "_",

        " hyphen ": "-",

        " dash ": "-",

        " space ": "",
    }

    for spoken, symbol in replacements.items():

        email = email.replace(
            spoken,
            symbol
        )

    email = email.replace(
        " @",
        "@"
    )

    email = email.replace(
        "@ ",
        "@"
    )

    email = email.replace(
        " .",
        "."
    )

    email = email.replace(
        ". ",
        "."
    )

    email = email.replace(
        " ",
        ""
    )

    return email


# ==================================================
# VALIDATE EMAIL ADDRESS
# ==================================================

def is_valid_email(email):
    """
    Performs a basic email address format check.

    Returns:
        True  -> valid format
        False -> invalid format
    """

    pattern = (
        r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    )

    return re.match(
        pattern,
        email
    ) is not None


# ==================================================
# SEND EMAIL
# ==================================================

def send_email(
    recipient,
    subject,
    body
):
    """
    Sends an email through Gmail SMTP.

    Credentials are obtained from:

        EMAIL_ADDRESS
        EMAIL_APP_PASSWORD

    environment variables.

    Returns:
        True  -> email sent successfully
        False -> email was not sent
    """

    sender = os.getenv(
        "EMAIL_ADDRESS"
    )

    app_password = os.getenv(
        "EMAIL_APP_PASSWORD"
    )

    # --------------------------------------------------
    # CHECK EMAIL CONFIGURATION
    # --------------------------------------------------

    if not sender or not app_password:

        print(
            "Email credentials are not configured."
        )

        speak(
            "The email service has not been "
            "configured yet."
        )

        return False

    # --------------------------------------------------
    # CREATE MESSAGE
    # --------------------------------------------------

    message = EmailMessage()

    message["From"] = sender

    message["To"] = recipient

    message["Subject"] = subject

    message.set_content(
        body
    )

    # --------------------------------------------------
    # CONNECT TO SMTP SERVER
    # --------------------------------------------------

    try:

        context = (
            ssl.create_default_context()
        )

        with smtplib.SMTP(
            EMAIL_SMTP_HOST,
            EMAIL_SMTP_PORT,
            timeout=20
        ) as server:

            server.ehlo()

            server.starttls(
                context=context
            )

            server.ehlo()

            server.login(
                sender,
                app_password
            )

            server.send_message(
                message
            )

        print(
            f"Email successfully sent "
            f"to {recipient}."
        )

        return True

    # --------------------------------------------------
    # AUTHENTICATION ERROR
    # --------------------------------------------------

    except smtplib.SMTPAuthenticationError:

        print(
            "Email authentication failed."
        )

        speak(
            "I couldn't authenticate with "
            "the email service. Please check "
            "the email address and App Password."
        )

        return False

    # --------------------------------------------------
    # RECIPIENT ERROR
    # --------------------------------------------------

    except smtplib.SMTPRecipientsRefused:

        print(
            "The recipient was refused."
        )

        speak(
            "The email recipient was refused "
            "by the mail server."
        )

        return False

    # --------------------------------------------------
    # CONNECTION ERROR
    # --------------------------------------------------

    except smtplib.SMTPConnectError:

        print(
            "Could not connect to the email server."
        )

        speak(
            "I couldn't connect to the email "
            "service. Please check your internet "
            "connection."
        )

        return False

    # --------------------------------------------------
    # GENERAL EMAIL ERROR
    # --------------------------------------------------

    except (
        smtplib.SMTPException,
        OSError
    ) as error:

        print(
            f"Email sending error: {error}"
        )

        speak(
            "I couldn't send the email because "
            "an email service error occurred."
        )

        return False


# ==================================================
# VOICE-CONTROLLED EMAIL
# ==================================================

def compose_and_send_email():
    """
    Guides the user through composing and sending
    an email using voice interaction.
    """

    # --------------------------------------------------
    # RECIPIENT
    # --------------------------------------------------

    recipient_text = ask_for_speech(
        "Who should I send the email to?"
    )

    if recipient_text is None:

        return

    recipient = normalize_email_address(
        recipient_text
    )

    print(
        "Normalized recipient:",
        recipient
    )

    if not is_valid_email(recipient):

        speak(
            "That does not appear to be "
            "a valid email address. "
            "Please try again."
        )

        print(
            "Invalid email address:",
            recipient
        )

        return

    # --------------------------------------------------
    # SUBJECT
    # --------------------------------------------------

    subject = ask_for_speech(
        "What should be the subject "
        "of the email?"
    )

    if subject is None:

        return

    # --------------------------------------------------
    # BODY
    # --------------------------------------------------

    body = ask_for_speech(
        "What should I write in the email?"
    )

    if body is None:

        return

    # --------------------------------------------------
    # CONFIRM EMAIL
    # --------------------------------------------------

    speak(
        f"I am preparing an email to "
        f"{recipient} with the subject "
        f"{subject}."
    )

    confirmation = ask_for_speech(
        "Would you like me to send the email? "
        "Please say yes or no."
    )

    if confirmation is None:

        return

    confirmation = (
        confirmation.lower().strip()
    )

    # --------------------------------------------------
    # CANCEL EMAIL
    # --------------------------------------------------

    if confirmation not in [
        "yes",
        "yeah",
        "yep",
        "send it",
        "send",
    ]:

        speak(
            "Okay. I will not send the email."
        )

        print(
            "Email cancelled by user."
        )

        return

    # --------------------------------------------------
    # SEND EMAIL
    # --------------------------------------------------

    speak(
        "Sending the email now."
    )

    success = send_email(
        recipient,
        subject,
        body
    )

    if success:

        speak(
            "The email was sent successfully."
        )


# ==================================================
# MODULE TEST
# ==================================================

if __name__ == "__main__":

    print()
    print("Testing email service...")
    print()

    # --------------------------------------------------
    # EMAIL NORMALIZATION TESTS
    # --------------------------------------------------

    test_addresses = [

        "john at gmail dot com",

        "john underscore doe at gmail dot com",

        "test hyphen user at outlook dot com",

    ]

    for spoken_address in test_addresses:

        normalized = normalize_email_address(
            spoken_address
        )

        print(
            f"Spoken:     {spoken_address}"
        )

        print(
            f"Normalized: {normalized}"
        )

        print(
            f"Valid:      {is_valid_email(normalized)}"
        )

        print(
            "-" * 50
        )

    # --------------------------------------------------
    # INVALID ADDRESS TESTS
    # --------------------------------------------------

    invalid_addresses = [

        "invalid-email",

        "missing-at-symbol.com",

        "@gmail.com",

    ]

    for address in invalid_addresses:

        print(
            f"Testing invalid address: {address}"
        )

        print(
            f"Valid: {is_valid_email(address)}"
        )

        print(
            "-" * 50
        )

    print(
        "Email service tests completed."
    )