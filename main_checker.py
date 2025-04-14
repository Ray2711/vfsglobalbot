import os
import subprocess
import time
from send_msg import send_telegram_message

def run_scripts(scripts_folder):
    if not os.path.exists(scripts_folder):
        send_telegram_message(f"Scripts folder does not exist: {scripts_folder}")
        return

    scripts = [f for f in os.listdir(scripts_folder) if f.endswith('.py') or f.endswith('.sh')]

    for script in scripts:
        script_path = os.path.join(scripts_folder, script)
        try:
            if script.endswith('.py'):
                result = subprocess.run(['python', script_path], capture_output=True, text=True)
            else:  # Assume .sh or other executable
                result = subprocess.run([script_path], capture_output=True, text=True)

            if result.returncode != 0:
                error_msg = f"Critical error in {script}: {result.stderr}"
                send_telegram_message(error_msg)
        except Exception as e:
            error_msg = f"Critical error while running {script}: {str(e)}"
            send_telegram_message(error_msg)

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
    scripts_folder = './scripts'  # Replace with your actual folder path
    wg_folder = './wg_configs'     # Replace with your actual folder path

    while True:
        run_scripts(scripts_folder)
        #switch_wireguard(wg_folder)
        time.sleep(3600)  # Sleep for 60 minutes (3600 seconds)

if __name__ == '__main__':
    main()