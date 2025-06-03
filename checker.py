import os
import sys
import subprocess
import time
from send_msg import send_telegram_message

def run_and_monitor_scripts(scripts_folder):
    # Discover all vfs_*.py scripts (except main.py)
    scripts = [
        f for f in os.listdir(scripts_folder)
        if f.startswith("vfs_") and f.endswith(".py") and f != "vfs_main.py"
    ]

    processes = []
    for script in scripts:
        script_path = os.path.join(scripts_folder, script)
        try:
            # start_new_session=True detaches the child so it won't die
            # if this launcher gets a signal
            proc = subprocess.Popen(
                [sys.executable, script_path],
                start_new_session=True
            )
            processes.append((script, proc))
            print(f"Launched {script} (pid={proc.pid})")
        except Exception as e:
            print(f"Failed to launch {script}: {e}")

    # Monitor until every child has exited
    while processes:
        for script, proc in processes[:]:
            code = proc.poll()
            if code is not None:
                msg = f"{script} exited with code {code}"
                print(msg)
                if code != 0:
                    send_telegram_message(msg)
                processes.remove((script, proc))
        time.sleep(1)

if __name__ == "__main__":
    run_and_monitor_scripts('.')