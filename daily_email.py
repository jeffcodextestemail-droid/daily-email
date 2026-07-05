import os
import smtplib
from datetime import datetime
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()


def get_email_settings():
    return {
        "sender": os.environ.get("DAILY_EMAIL_SENDER"),
        "recipient": os.environ.get("DAILY_EMAIL_RECIPIENT"),
        "smtp_server": os.environ.get("DAILY_EMAIL_SMTP_SERVER"),
        "smtp_port": os.environ.get("DAILY_EMAIL_SMTP_PORT", "587"),
        "password": os.environ.get("DAILY_EMAIL_PASSWORD"),
        "send_email": os.environ.get("DAILY_EMAIL_SEND", "false").lower() == "true",
    }


def find_missing_settings(settings):
    required_settings = {
        "sender": "DAILY_EMAIL_SENDER",
        "recipient": "DAILY_EMAIL_RECIPIENT",
        "smtp_server": "DAILY_EMAIL_SMTP_SERVER",
    }

    if settings["send_email"]:
        required_settings["password"] = "DAILY_EMAIL_PASSWORD"

    missing = []
    for key, environment_variable in required_settings.items():
        if not settings[key]:
            missing.append(environment_variable)

    return missing


def build_email_message(settings):
    timestamp = datetime.now().strftime("%B %d, %Y %I:%M:%S %p")

    message = EmailMessage()
    message["From"] = settings["sender"]
    message["To"] = settings["recipient"]
    message["Subject"] = f"Daily email for {timestamp}"
    message.set_content("Hello! This is your daily email.")

    return message


def send_email(settings, message):
    smtp_port = int(settings["smtp_port"])

    with smtplib.SMTP(settings["smtp_server"], smtp_port) as server:
        server.starttls()
        server.login(settings["sender"], settings["password"])
        server.send_message(message)


def main():
    settings = get_email_settings()
    missing_settings = find_missing_settings(settings)

    print("Daily email script is ready.")

    if missing_settings:
        print("Missing required settings:")
        for setting in missing_settings:
            print(f"  {setting}")
        return

    print("Email settings:")
    print(f"  Sender: {settings['sender'] or 'not set'}")
    print(f"  Recipient: {settings['recipient'] or 'not set'}")
    print(f"  SMTP server: {settings['smtp_server'] or 'not set'}")
    print(f"  SMTP port: {settings['smtp_port']}")
    print(f"  Send email: {settings['send_email']}")
    print(f"  Password: {'set' if settings['password'] else 'not set'}")

    message = build_email_message(settings)

    print("Email preview:")
    print(f"  From: {message['From']}")
    print(f"  To: {message['To']}")
    print(f"  Subject: {message['Subject']}")
    print(f"  Body: {message.get_content().strip()}")

    if not settings["send_email"]:
        print("Dry run only. Set DAILY_EMAIL_SEND=true when you are ready to send.")
        return

    send_email(settings, message)
    print("Email sent.")


if __name__ == "__main__":
    main()
