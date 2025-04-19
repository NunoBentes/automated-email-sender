import smtplib
import time
import json
import os
import csv
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from validators import validate_env_variables, validate_smtp_configuration, load_translations

# Configure logging
logging.basicConfig(filename='email_sender.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
load_dotenv()

# Load translations
LANGUAGE = os.getenv("LANGUAGE", "en")  # Default to English if not set
translations = load_translations(LANGUAGE)

# Global configuration variables
EMAIL_MODE = os.getenv("EMAIL_MODE", "csv").strip().lower()  # Default to 'csv' if not set
EMAIL_DATA_CSV = os.getenv("EMAIL_DATA_CSV")
EMAIL_DATA_JSON = os.getenv("EMAIL_DATA_JSON")
SEND_EMAIL_INTERVAL = int(os.getenv("SEND_EMAIL_INTERVAL", 120))  # Default to 120 seconds if not set
SMTP_SERVER = os.getenv("EMAIL_SMTP")
SMTP_PORT = int(os.getenv("EMAIL_SMTP_PORT"))
USE_TLS = os.getenv("EMAIL_USE_TLS", "true").strip().lower() == "true"  # Default to True if not set
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
SENDER_NAME = os.getenv("SENDER_NAME", "John Doe")  # Default sender name if not set
EMAIL_SUBJECT = os.getenv("EMAIL_SUBJECT", "Email Subject")  # Default email subject if not set
EMAIL_BODY = os.getenv("EMAIL_BODY", "Hello {recipient_name},\n\nThis is a default email body.\n\nBest regards,\n{sender_name}")

# Load email data from a JSON file
def load_email_data(json_file):
    with open(json_file, 'r') as file:
        return json.load(file)

# Load email data from a CSV file
def load_email_data_from_csv(csv_file):
    email_data = []
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            email_data.append({
                "name": row["name"],
                "email": row["email"]
            })
    return email_data

# Send an email
def send_email(recipient_email, subject, body):
    try:
        # Set up the email
        msg = MIMEMultipart()
        msg['From'] = f"{SENDER_NAME} <{SENDER_EMAIL}>"  # Add sender name
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            if USE_TLS:
                server.starttls()  # Use TLS if enabled
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            logging.info(translations["EMAIL_SENT_SUCCESS"].format(recipient_email=recipient_email))
    except smtplib.SMTPAuthenticationError:
        logging.error(translations["SMTP_AUTH_ERROR"].format(recipient_email=recipient_email))
        raise
    except smtplib.SMTPException as e:
        logging.error(translations["SMTP_ERROR"].format(recipient_email=recipient_email, error=e))
        raise
    except Exception as e:
        logging.error(translations["UNEXPECTED_ERROR"].format(recipient_email=recipient_email, error=e))
        raise

# Validate configurations
def validate_configurations():
    validate_env_variables(
        SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD,
        EMAIL_MODE, SEND_EMAIL_INTERVAL, USE_TLS, SENDER_NAME,
        EMAIL_SUBJECT, EMAIL_BODY, EMAIL_DATA_CSV, EMAIL_DATA_JSON
    )
    validate_smtp_configuration(SMTP_SERVER, SMTP_PORT, USE_TLS, SENDER_EMAIL, SENDER_PASSWORD, language=LANGUAGE)

# Main function to send emails every 2 minutes
def main():
    try:
        # Validate configurations
        validate_configurations()

        # Determine the email data file based on the mode
        if EMAIL_MODE == "json":
            email_data_file = EMAIL_DATA_JSON
            email_data = load_email_data(email_data_file)
        elif EMAIL_MODE == "csv":
            email_data_file = EMAIL_DATA_CSV
            email_data = load_email_data_from_csv(email_data_file)
        else:
            raise ValueError(translations["EMAIL_MODE_INVALID"])

        # Loop through the email data and send emails every 2 minutes
        for index, entry in enumerate(email_data):
            recipient_name = entry['name']
            recipient_email = entry['email']

            # Define placeholders for the email template
            placeholders = {
                "recipient_name": recipient_name,
                "sender_name": SENDER_NAME,
                "date": time.strftime("%Y-%m-%d")  # Add the current date
            }

            # Format the email body using the placeholders
            body = EMAIL_BODY.format(**placeholders)
            subject = EMAIL_SUBJECT
            send_email(recipient_email, subject, body)

            # Check if this is the last email
            if index == len(email_data) - 1:
                logging.info(translations["ALL_EMAILS_SENT"])  # Final message after the last email
            else:
                time.sleep(SEND_EMAIL_INTERVAL)
    except Exception as e:
        logging.error(translations["SCRIPT_STOPPED_ERROR"].format(error=e))

if __name__ == "__main__":
    main()