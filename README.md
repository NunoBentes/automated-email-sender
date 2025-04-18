# Automated Email Sender

A Python script for sending automated emails at regular intervals using SMTP.

## Project Structure

```
email-sender
├── src
│   └── email-sender.py       # Main functionality for sending automated emails
├── .env                       # Environment variables for email authentication
├── emails.json                # Email data including recipient addresses and names
├── requirements.txt           # Python dependencies required for the project
└── README.md                  # Documentation for the project
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone https://github.com/yourusername/automated-email-sender.git
   cd automated-email-sender
   ```

2. **Install dependencies:**
   Make sure you have Python installed, then run:
   ```
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   Create a `.env` file in the root directory and add your email credentials:
   ```
   SENDER_EMAIL=your_email@example.com
   SENDER_PASSWORD=your_password
   ```

4. **Prepare email data:**
   Edit the `emails.json` file to include the recipient email addresses and names in the following format:
   ```json
   [
       {
           "email": "recipient1@example.com",
           "name": "Recipient One"
       },
       {
           "email": "recipient2@example.com",
           "name": "Recipient Two"
       }
   ]
   ```

5. **Run the email sender script:**
   Execute the script to start sending emails:
   ```
   python src/email-sender.py
   ```

## Usage

The script will send automated emails to the recipients listed in `emails.json` every 2 minutes. You can modify the email content and interval as needed within the `email-sender.py` file.

## License

This project is licensed under the MIT License. See the LICENSE file for details.