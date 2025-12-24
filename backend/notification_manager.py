import requests

BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

class NotificationManager:
    def send_message(self, message):
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message}
        try:
            requests.post(url, data=payload)
        except Exception as e:
            print(f"Notification failed: {e}")
