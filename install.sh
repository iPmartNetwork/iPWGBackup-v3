#!/bin/bash
apt update && apt install -y python3 python3-pip git paramiko
pip3 install flask requests pycryptodome

mkdir -p /opt/ipwgbackup/{backups,keys,logs}
cp -r ~/iPWGBackup-v2-professional/* /opt/ipwgbackup/

systemctl daemon-reload
systemctl enable wg_backup.service
systemctl enable wg_backup.timer
systemctl start wg_backup.timer

echo "iPWGBackup Professional installed and running!"
