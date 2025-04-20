# Automated Email Sender

![Automated Email Sender](automated-email-sender.png "Automated Email Sender")

A Python script for sending automated emails at regular intervals using SMTP. The script supports both JSON and CSV formats for recipient data and includes multi-language support for error messages and logs.

---

## Project Structure

```
automated-email-sender
├── src
│   ├── email-sender.py       # Main script for sending automated emails
│   ├── validators.py         # Validation logic for environment variables and SMTP configuration
├── data
│   ├── emails.csv            # CSV file containing recipient data
│   ├── emails.json           # JSON file containing recipient data
├── translations
│   ├── en.json               # English translations
│   ├── pt.json               # Portuguese translations
├── .env                      # Environment variables for email configuration
├── requirements.txt          # Python dependencies required for the project
├── email_sender.log          # Log file for email sending status and errors
├── README.md                 # Documentation for the project
```

---

## Setup Instructions

### 1. **Clone the Repository**
```bash
git clone https://github.com/NunoBentes/automated-email-sender.git
cd automated-email-sender
```

### 2. **Install Dependencies**
Make sure you have Python installed, then run the following command to install the required dependencies:
```bash
pip install -r requirements.txt
```

### 3. **Configure Environment Variables**
Edit the `.env` file in the root directory and add your email credentials and configuration:
```properties
# Preferred language for translations (e.g., 'en' for English, 'pt' for Portuguese)
LANGUAGE=pt

# Mode of the email data file: 'json' or 'csv'
EMAIL_MODE=csv

# Path to the CSV file
EMAIL_DATA_CSV=data/emails.csv

# Path to the JSON file
EMAIL_DATA_JSON=data/emails.json

# Interval in seconds between sending emails
SEND_EMAIL_INTERVAL=120

# SMTP server configuration
EMAIL_SMTP=mail.yourdomain.com
EMAIL_SMTP_PORT=587
EMAIL_USE_TLS=true  # Use TLS for secure email sending
SENDER_EMAIL=your.email@yourdomain.com
SENDER_PASSWORD=your_password

# Sender email credentials
SENDER_NAME=Nuno Bentes

# Email Subject
EMAIL_SUBJECT=Your Email Subject Here

# Email Body Template
EMAIL_BODY="Hello {recipient_name},\n
This is an automated email sent by {sender_name}.
Thank you for being a valued customer.\n
Best regards,
{sender_name}"
```

### 4. **Prepare Email Data**
You can use either a JSON or CSV file to store recipient data.

#### JSON Format (`emails.json`):
```json
[
    {
        "name": "John Doe",
        "email": "john.doe@example.com"
    },
    {
        "name": "Jane Smith",
        "email": "jane.smith@example.com"
    },
    {
        "name": "Alice Johnson",
        "email": "alice.johnson@example.com"
    }
]
```

#### CSV Format (`emails.csv`):
```csv
name,email
John Doe,john.doe@example.com
Jane Smith,jane.smith@example.com
Alice Johnson,alice.johnson@example.com
```

### 5. **Run the Email Sender Script**
Execute the script to start sending emails:
```bash
python src/email-sender.py
```

---

## Features

1. **Multi-Language Support**:
   - Error messages and logs are available in multiple languages (e.g., English and Portuguese). Configure the language in the `.env` file using the `LANGUAGE` variable.

2. **Flexible Recipient Data**:
   - Supports both JSON and CSV formats for recipient data.

3. **SMTP Configuration Validation**:
   - Validates SMTP credentials and connection before sending emails.

4. **Logging**:
   - Logs email sending status and errors to `email_sender.log`.

5. **Customizable Email Content**:
   - Use placeholders like `{recipient_name}`, `{sender_name}`, and `{date}` in the email body template.

---

## Example Email

**Subject**: Your Email Subject Here  
**Body**:
```
Hello Jane Smith,

This is an automated email sent by John Smith.
Thank you for being a valued customer.

Best regards,
John Smith
```

---

## Troubleshooting

1. **SMTP Authentication Error**:
   - If you see an error like `(535, b'Incorrect authentication data')`, check your SMTP credentials in the `.env` file.

2. **Missing Translation File**:
   - If a translation file is missing, the script will fall back to English. Ensure the `translations` directory contains `en.json` and `pt.json`.

3. **Email Data File Not Found**:
   - Ensure the `EMAIL_DATA_CSV` or `EMAIL_DATA_JSON` path in the `.env` file points to an existing file.

4. **Empty Email Data File**:
   - Ensure the recipient data file is not empty.

---

## Logs

The script logs all email sending statuses and errors to `email_sender.log`. Example log entry:
```
2025-04-19 16:45:18,630 - INFO - Email enviado com sucesso para john.doe@example.com.
```

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
