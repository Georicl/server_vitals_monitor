import os
import sys
import getpass
import subprocess

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
SCRIPT_NAME = os.path.join(PROJECT_ROOT, "src", "server_monitor", "monitor.py")
SERVICE_NAME = "vitals_monitor.service"


def get_path():
    user_home = os.path.expanduser("~")
    # 生成用户级配置
    systemd_user_dir = os.path.join(user_home, ".config", "systemd", "user")

    project_dir = os.getcwd()
    # 获取python版本
    python_path = sys.executable
    script_path = os.path.join(project_dir, SCRIPT_NAME)

    return {
        "user": getpass.getuser(),
        "home": user_home,
        "python_path": python_path,
        "script_path": script_path,
        "systemd_dir": systemd_user_dir,
        "project_dir": project_dir,
        "server_file_path": os.path.join(systemd_user_dir, SERVICE_NAME),
    }


def check_enviroment(paths):
    if not os.path.exists(paths["script_path"]):
        print(f"脚本不存在: {SCRIPT_NAME}")
        sys.exit(1)

    if not os.path.exists(paths["systemd_dir"]):
        os.makedirs(paths["systemd_dir"], exist_ok=True)


def generate_server_file(paths):
    content = f"""[Unit]
Description=Server Vitals Monitor
After=network.target

[Service]
Type=simple
WorkingDirectory={paths["project_dir"]}
ExecStart={paths["python_path"]} -u {SCRIPT_NAME}
Restart=on-failure
RestartSec=10
# 输出重定向
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=default.target
"""
    return content


def install_service():
    print(" === Now you are installing Server Vitals Monitor === \n")

    paths = get_path()
    check_enviroment(paths)

    print("Now printing config info:\n")
    print(f"You will install this service in user: {paths['user']}")
    print(f"Project path: {paths['project_dir']}")
    print(f"The final file will install in path: {paths['server_file_path']}")

    # 生成服务文件
    content = generate_server_file(paths)
    with open(paths["server_file_path"], "w") as f:
        f.write(content)

    print("Service file generated done.")

    # 配置linger服务
    print("Now configuring service...")

    try:
        subprocess.run(["loginctl", "enable-linger", paths["user"]], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Fail to enable linger: {e}")

    # 启动服务
    print("Starting service...")
    try:
        subprocess.run(["systemctl", "--user", "daemon-reload"], check=True)
        subprocess.run(["systemctl", "--user", "enable", SERVICE_NAME], check=True)
        subprocess.run(["systemctl", "--user", "restart", SERVICE_NAME], check=True)

        print(f"Service {SERVICE_NAME} installed and started successfully.")

        subprocess.run(["systemctl", "--user", "status", SERVICE_NAME, "--no-pager"])
    except subprocess.CalledProcessError as e:
        print(f"Fail to start service: {e}")


if __name__ == "__main__":
    install_service()
