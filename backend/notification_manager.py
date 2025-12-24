import requests
import smtplib
from email.message import EmailMessage

BOT_TOKEN = "123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZ"  # نمونه واقعی
CHAT_ID = "123456789"

SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
SMTP_USER = "user@example.com"
SMTP_PASS = "password"
TO_EMAIL = "admin@example.com"

class NotificationManager:
    def send_message(self, message):
        # Telegram
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": message})

        # Email
        try:
            msg = EmailMessage()
            msg.set_content(message)
            msg["Subject"] = "iPWGBackup Notification"
            msg["From"] = SMTP_USER
            msg["To"] = TO_EMAIL
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as s:
                s.starttls()
                s.login(SMTP_USER, SMTP_PASS)
                s.send_message(msg)
        except Exception as e:
            print(f"Email failed: {e}")
