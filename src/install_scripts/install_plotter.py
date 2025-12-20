import os
import sys
import getpass
import subprocess

SERVICE_NAME = "vitals_plot.service"
TIMER_NAME = "vitals_plot.timer"
SCRIPT_REL_PATH = "src/server_monitor/daily_job.py"

def install_timer():
    print("=== Server Vitals Plotter Install===")

    # get path
    project_dir = os.getcwd()
    user_home = os.path.expanduser("~")
    systemd_dir = os.path.join(user_home, ".config", "systemd", "user")
    script_path = os.path.join(project_dir, SCRIPT_REL_PATH)
    python_path = sys.executable

    os.makedirs(systemd_dir, exist_ok=True)
    
    # generate service file
    content = f"""[Unit]
Description=Generate Daily Server Vitals Report

[Service]
Type=oneshot
WorkingDirectory={project_dir}
ExecStart={python_path} {script_path} --yesterday
"""
    service_path = os.path.join(systemd_dir, SERVICE_NAME)
    with open(service_path, "w") as f:
        f.write(content)

    # generate timer file
    timer_content = f"""[Unit]
Description=Run Vitals Plotter Daily

[Timer]
OnCalendar=*-*-* 00:10:00
Persistent=true

[Install]
WantedBy=timers.target
"""
    timer_path = os.path.join(systemd_dir, TIMER_NAME)
    with open(timer_path, "w") as f:
        f.write(timer_content)

    
    try:
        subprocess.run(["systemctl", "--user", "daemon-reload"], check=True)
        # run timer
        subprocess.run(["systemctl", "--user", "enable", "--now", TIMER_NAME], check=True)
        
        print("\n Done")
        print(f"script will run in 00:10:00 everyday")
        print("\nhow to check the status:")
        print(f"systemctl --user list-timers --all | grep vitals")
        
    except subprocess.CalledProcessError as e:
        print(f"Fail to install this plotter: {e}")

if __name__ == "__main__":
    install_timer()