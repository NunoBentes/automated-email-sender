# filepath: email-sender/src/email-sender.py
import smtplib
import time
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load email data from a JSON file
def load_email_data(json_file):
    with open(json_file, 'r') as file:
        return json.load(file)

# Send an email
def send_email(smtp_server, port, sender_email, sender_password, recipient_email, subject, body, sender_name="Nuno Bentes"):
    try:
        # Set up the email
        msg = MIMEMultipart()
        msg['From'] = f"{sender_name} <{sender_email}>"  # Add sender name
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print(f"Email sent to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Main function to send emails every 2 minutes
def main():
    # Email configuration
    smtp_server = "mail.farmajuda24.pt"  # Replace with your SMTP server
    port = 587  # Replace with your SMTP port
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")

    # Load email data from JSON
    email_data = load_email_data("emails.json")

    # Loop through the email data and send emails every 2 minutes
    for index, entry in enumerate(email_data):
        recipient_email = entry['email']
        name = entry['name']
        subject = "Automated Email"
        body = f"Hello {name},\n\nThis is an automated email sent every 2 minutes.\n\nBest regards,\nYour Company"

        send_email(smtp_server, port, sender_email, sender_password, recipient_email, subject, body)
        print(f"Email successfully sent to {recipient_email}.")  # Message after each email is sent

        # Check if this is the last email
        if index == len(email_data) - 1:
            print("All emails have been sent. Task concluded.")  # Final message after the last email
        else:
            time.sleep(120)  # Wait for 2 minutes (120 seconds) before sending the next email

if __name__ == "__main__":
    main()