import telebot
import os
from backup_manager import BackupManager
from notification_manager import NotificationManager
from remote_upload import RemoteUploader

BOT_TOKEN = open("/opt/ipwgbackup/bot_token.txt").read().strip()
ADMIN_ID = int(open("/opt/ipwgbackup/admin_id.txt").read().strip())

bot = telebot.TeleBot(BOT_TOKEN)
backup_manager = BackupManager()
notifier = NotificationManager()
uploader = RemoteUploader()

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id != ADMIN_ID:
        bot.reply_to(message, "Unauthorized")
        return
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    markup.add("Run Backup", "Restore Backup", "Show Status", "Update Script", "Uninstall Script")
    bot.send_message(ADMIN_ID, "Welcome to iPWGBackup Professional Bot", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def menu(message):
    if message.chat.id != ADMIN_ID:
        return
    text = message.text

    if text == "Run Backup":
        for profile in backup_manager.list_profiles():
            success, msg = backup_manager.run_backup(profile)
            bot.send_message(ADMIN_ID, f"[{profile}] Backup: {'Success' if success else 'Failed'}\n{msg}")
            notifier.send_message(f"[{profile}] Manual Backup: {msg}")
            uploader.upload_backup(profile)

    elif text == "Restore Backup":
        bot.send_message(ADMIN_ID, "Send the backup filename to restore:")

        @bot.message_handler(func=lambda m: True)
        def restore_file(msg):
            backup_file = msg.text.strip()
            success, msg_text = backup_manager.restore_backup(backup_file)
            bot.send_message(ADMIN_ID, f"Restore: {'Success' if success else 'Failed'}\n{msg_text}")
            notifier.send_message(f"Restore: {msg_text}")

    elif text == "Show Status":
        history = backup_manager.get_history()
        last = history[-1] if history else {"status":"No backups yet"}
        bot.send_message(ADMIN_ID, f"Last Backup Status:\n{last}")

    elif text == "Update Script":
        os.system("cd /opt/ipwgbackup && git pull")
        bot.send_message(ADMIN_ID, "Script updated successfully!")

    elif text == "Uninstall Script":
        os.system("systemctl stop wg_backup.service wg_backup.timer")
        os.system("systemctl disable wg_backup.service wg_backup.timer")
        bot.send_message(ADMIN_ID, "Script uninstalled. Goodbye!")

bot.polling(none_stop=True)
