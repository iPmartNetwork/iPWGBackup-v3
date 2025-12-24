import subprocess

def check_wg_interface(interface="wg0"):
    try:
        res = subprocess.run(["wg", "show", interface], capture_output=True, text=True)
        return res.returncode == 0 and "interface" in res.stdout
    except:
        return False
