import paramiko, os

SFTP_HOST = "sftp.example.com"
SFTP_PORT = 22
SFTP_USER = "user"
SFTP_PASS = "password"
REMOTE_PATH = "/remote/backups/"

class RemoteUploader:
    def upload_backup(self, profile):
        local_dir = "/opt/ipwgbackup/backups/"
        for file in os.listdir(local_dir):
            if file.startswith(profile) and file.endswith(".enc"):
                local_file = os.path.join(local_dir, file)
                try:
                    transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
                    transport.connect(username=SFTP_USER, password=SFTP_PASS)
                    sftp = paramiko.SFTPClient.from_transport(transport)
                    sftp.put(local_file, REMOTE_PATH + file)
                    sftp.close()
                    transport.close()
                except Exception as e:
                    print(f"SFTP upload failed: {e}")
