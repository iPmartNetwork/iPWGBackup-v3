import requests

BOT_TOKEN = open("/opt/ipwgbackup/bot_token.txt").read().strip()
ADMIN_ID = int(open("/opt/ipwgbackup/admin_id.txt").read().strip())

class NotificationManager:
    def send_message(self, message):
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": ADMIN_ID, "text": message})
