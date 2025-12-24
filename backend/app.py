from flask import Flask, jsonify, request
from backup_manager import BackupManager
from notification_manager import NotificationManager

app = Flask(__name__)
backup_manager = BackupManager()
notifier = NotificationManager()

@app.route("/backup", methods=["POST"])
def run_backup():
    profile = request.json.get("profile", "wg0")
    success, message = backup_manager.run_backup(profile)
    notifier.send_message(f"Backup {profile}: {'Success' if success else 'Failed'}\n{message}")
    return jsonify({"success": success, "message": message})

@app.route("/history", methods=["GET"])
def backup_history():
    history = backup_manager.get_history()
    return jsonify(history)

@app.route("/restore", methods=["POST"])
def restore_backup():
    backup_file = request.json.get("file")
    success, message = backup_manager.restore_backup(backup_file)
    notifier.send_message(f"Restore: {'Success' if success else 'Failed'}\n{message}")
    return jsonify({"success": success, "message": message})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
