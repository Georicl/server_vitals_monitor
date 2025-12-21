import os
import sys
import subprocess


def run_installer(script_name):
    project_root = os.getcwd()
    script_path = os.path.join(project_root, "src", "install_scripts", script_name)

    if not os.path.exists(script_path):
        print(f"Error: {script_path} not found")
        return False

    print(f"\nNow start running {script_name}")
    print("-" * 40)

    env = os.environ.copy()
    env["PYTHONPATH"] = (
        os.path.join(project_root, "src") + os.pathsep + env.get("PYTHONPATH", "")
    )

    try:
        subprocess.run([sys.executable, script_path], check=True, env=env)
        print("-" * 40)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False

def main():
    print("=== Server Vitals Monitor Starter===")

    print("\n[1/3] Installing package and CLI tools...")

    try:
        subprocess.run(["uv", "pip", "install", "-e", "."], check=True)
    except FileNotFoundError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."], check=True)
    except subprocess.CalledProcessError:
        print("❌ Package installation failed.")
        sys.exit(1)

    print(" CLI tools installed (task-guard, server-monitor)")
    # 安装监控服务
    print("Installing Monitor Service...")
    if not run_installer("install_monitor.py"):
        sys.exit(1)

    # 安装绘图定时任务
    print("Installing Plotter Service...")
    if not run_installer("install_plotter.py"):
        sys.exit(1)

    print("All done!")


if __name__ == "__main__":
    main()
