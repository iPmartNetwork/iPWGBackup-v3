#!/bin/bash
apt update && apt install -y python3 python3-pip git
pip3 install flask requests pycryptodome

mkdir -p /opt/ipwgbackup/backups
cd /opt/ipwgbackup || mkdir -p /opt/ipwgbackup

cp -r ~/iPWGBackup-v2/* /opt/ipwgbackup

systemctl daemon-reload
systemctl enable wg_backup.service
systemctl enable wg_backup.timer
systemctl start wg_backup.timer

echo "iPWGBackup installed and running!"
