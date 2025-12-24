import subprocess

def check_wg_interface(profile):
    try:
        result = subprocess.run(["wg", "show", profile], capture_output=True)
        return result.returncode == 0
    except:
        return False
