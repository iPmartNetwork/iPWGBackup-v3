import os, shutil, json, datetime
from wg_checker import check_wg_interface
from crypto import encrypt_file

HISTORY_DB = "/opt/ipwgbackup/logs/backup_history.json"
STORAGE_DIR = "/opt/ipwgbackup/backups/"
KEYS_DIR = "/opt/ipwgbackup/keys/"

class BackupManager:
    def __init__(self):
        os.makedirs(STORAGE_DIR, exist_ok=True)
        os.makedirs(KEYS_DIR, exist_ok=True)
        os.makedirs(os.path.dirname(HISTORY_DB), exist_ok=True)
        if not os.path.exists(HISTORY_DB):
            with open(HISTORY_DB, "w") as f:
                json.dump([], f)

    def run_backup(self, profile="wg0"):
        if not check_wg_interface(profile):
            return False, "WireGuard interface offline"

        filename = f"{profile}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.conf"
        filepath = os.path.join(STORAGE_DIR, filename)
        shutil.copy(f"/etc/wireguard/{profile}.conf", filepath)

        key_path = os.path.join(KEYS_DIR, f"{profile}.key")
        if not os.path.exists(key_path):
            with open(key_path, "wb") as f:
                f.write(os.urandom(32))

        encrypt_file(filepath, key_path)

        with open(HISTORY_DB, "r+") as f:
            history = json.load(f)
            history.append({"file": filename+".enc", "profile": profile, "timestamp": str(datetime.datetime.now()), "status": "success"})
            f.seek(0)
            json.dump(history, f, indent=4)
        return True, f"Backup saved to {filepath}.enc"

    def get_history(self):
        with open(HISTORY_DB, "r") as f:
            return json.load(f)

    def restore_backup(self, backup_file):
        enc_path = os.path.join(STORAGE_DIR, backup_file)
        if not os.path.exists(enc_path):
            return False, "Backup file not found"

        # پیدا کردن کلید پروفایل
        profile = backup_file.split("_")[0]
        key_path = os.path.join(KEYS_DIR, f"{profile}.key")
        from crypto import decrypt_file
        decrypt_file(enc_path, key_path)
        return True, "Restore completed"
