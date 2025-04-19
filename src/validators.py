import os
import json
import smtplib

def load_translations(language="en"):
    translations_path = f"translations/{language}.json"
    if not os.path.exists(translations_path):
        print(f"Translation file for language '{language}' not found. Falling back to English.")
        translations_path = "translations/en.json"
    with open(translations_path, 'r') as file:
        return json.load(file)

# Validate SMTP configuration
def validate_smtp_configuration(SMTP_SERVER, SMTP_PORT, USE_TLS, SENDER_EMAIL, SENDER_PASSWORD, language="en"):
    translations = load_translations(language)

    # Check if required SMTP variables are set
    if not SMTP_SERVER or not SMTP_PORT or not SENDER_EMAIL or not SENDER_PASSWORD:
        raise ValueError(translations["SMTP_CONFIG_MISSING"])

    # Validate SMTP connection
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            if USE_TLS:
                server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
    except smtplib.SMTPAuthenticationError:
        raise ValueError(translations["SMTP_AUTH_ERROR"])
    except Exception as e:
        raise ValueError(translations["SMTP_CONNECTION_ERROR"].format(error=str(e)))

# Validate environment variables
def validate_env_variables(SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD, EMAIL_MODE, SEND_EMAIL_INTERVAL, USE_TLS, SENDER_NAME, EMAIL_SUBJECT, EMAIL_BODY, EMAIL_DATA_CSV, EMAIL_DATA_JSON):
    # Load language from .env
    language = os.getenv("LANGUAGE", "en")  # Default to English if not set
    translations = load_translations(language)

    # Check if required environment variables are set
    if not all([SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD]):
        raise ValueError(translations["EMAIL_SMTP_PORT_INVALID"])

    # Check if the email mode is valid
    if EMAIL_MODE not in ["json", "csv"]:
        raise ValueError(translations["EMAIL_MODE_INVALID"])
    

    # Check if the send email interval is a positive integer
    if SEND_EMAIL_INTERVAL <= 0:
        raise ValueError(translations["EMAIL_SMTP_PORT_INVALID"])

    # Check if the SMTP port is a valid integer
    if not isinstance(SMTP_PORT, int) or SMTP_PORT <= 0:
        raise ValueError(translations["EMAIL_SMTP_PORT_INVALID"])

    # Check if the TLS setting is a boolean
    if not isinstance(USE_TLS, bool):
        raise ValueError(translations["EMAIL_USE_TLS_INVALID"])

    # Check if the sender name is a string
    if not isinstance(SENDER_NAME, str):
        raise ValueError(translations["SENDER_NAME_INVALID"])

    # Check if the email subject is a string
    if not isinstance(EMAIL_SUBJECT, str):
        raise ValueError(translations["EMAIL_SUBJECT_INVALID"])

    # Check if the email body is a string
    if not isinstance(EMAIL_BODY, str):
        raise ValueError(translations["EMAIL_BODY_INVALID"])

    # Check if the email data file exists
    if EMAIL_MODE == "csv" and not os.path.exists(EMAIL_DATA_CSV):
        raise FileNotFoundError(translations["EMAIL_DATA_FILE_NOT_FOUND"].format(file=EMAIL_DATA_CSV))

    if EMAIL_MODE == "json" and not os.path.exists(EMAIL_DATA_JSON):
        raise FileNotFoundError(translations["EMAIL_DATA_FILE_NOT_FOUND"].format(file=EMAIL_DATA_JSON))

    # Check if the email data file is empty
    if EMAIL_MODE == "csv":
        with open(EMAIL_DATA_CSV, 'r') as file:
            if not any(file):
                raise ValueError(translations["EMAIL_DATA_FILE_EMPTY"].format(file=EMAIL_DATA_CSV))

    if EMAIL_MODE == "json":
        with open(EMAIL_DATA_JSON, 'r') as file:
            data = json.load(file)
            if not data:
                raise ValueError(translations["EMAIL_DATA_FILE_EMPTY"].format(file=EMAIL_DATA_JSON))