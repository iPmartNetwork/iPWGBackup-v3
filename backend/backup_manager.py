import os, shutil, json, datetime
from wg_checker import check_wg_interface
from crypto import encrypt_file

HISTORY_DB = "/opt/ipwgbackup/backup_history.json"
STORAGE_DIR = "/opt/ipwgbackup/backups/"

class BackupManager:
    def __init__(self):
        os.makedirs(STORAGE_DIR, exist_ok=True)
        if not os.path.exists(HISTORY_DB):
            with open(HISTORY_DB, "w") as f:
                json.dump([], f)

    def run_backup(self, profile="wg0"):
        if not check_wg_interface(profile):
            return False, "WireGuard interface offline"

        filename = f"{profile}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.conf"
        filepath = os.path.join(STORAGE_DIR, filename)
        
        shutil.copy(f"/etc/wireguard/{profile}.conf", filepath)
        encrypt_file(filepath)

        with open(HISTORY_DB, "r+") as f:
            history = json.load(f)
            history.append({"file": filename, "timestamp": str(datetime.datetime.now()), "status": "success"})
            f.seek(0)
            json.dump(history, f, indent=4)
        return True, f"Backup saved to {filepath}"

    def get_history(self):
        with open(HISTORY_DB, "r") as f:
            return json.load(f)

    def restore_backup(self, backup_file):
        filepath = os.path.join(STORAGE_DIR, backup_file)
        if not os.path.exists(filepath):
            return False, "Backup file not found"
        shutil.copy(filepath, f"/etc/wireguard/{backup_file.replace('.conf.enc','')}.conf")
        return True, "Restore completed"
