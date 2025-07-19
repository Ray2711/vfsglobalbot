import os
import subprocess
import time
import datetime
from send_msg import send_telegram_message

def run_scripts(scripts_folder):
    scripts = [f for f in os.listdir(scripts_folder) if f.endswith('.py') and f.startswith("vfs_") and not f.endswith('main.py')]

    for script in scripts:
        script_path = os.path.join(scripts_folder, script)
        try:
            if script.endswith('.py'):
                os.system('python ' +script_path)
        except Exception as e:
            print("shit",e)

def switch_wireguard(wg_folder):
    if not os.path.exists(wg_folder):
        return  # Folder doesn't exist, so skip

    configs = [f for f in os.listdir(wg_folder) if f.endswith('.conf')]

    if configs:  # Only proceed if configs are present
        try:
            # Down the existing WireGuard interface (assuming 'wg0')
            subprocess.run(['wg-quick', 'down', 'wg0'], check=True)
            # Up the first config file
            first_config = os.path.join(wg_folder, configs[0])
            subprocess.run(['wg-quick', 'up', first_config], check=True)
        except subprocess.CalledProcessError as e:
            send_telegram_message(f"WireGuard switch error: {str(e)}")
        except Exception as e:
            send_telegram_message(f"Unexpected error in WireGuard switch: {str(e)}")

def main():
    
    scripts_folder = '.'  # Replace with your actual folder path
    wg_folder = './wg_configs'     # Replace with your actual folder path

    while True:
        run_scripts(scripts_folder)
        #switch_wireguard(wg_folder)
        now = datetime.datetime.now()
        # Calculate seconds until next :00 or :30
       # next_minute = 30 if now.minute < 30 else 60
        next_minute = 60
        next_time = now.replace(minute=next_minute % 60, second=0, microsecond=0)
        if next_minute == 60:
            next_time = next_time + datetime.timedelta(hours=1)
        sleep_seconds = (next_time - now).total_seconds()
        time.sleep(sleep_seconds)

if __name__ == '__main__':
    main()