import os
import sys
import subprocess

def main():
    print("=== Server Vitals Monitor Installer ===")
    
    # 1. 安装 Python 包依赖及 CLI 命令
    print("\n[1/3] Installing package and CLI tools...")
    try:
        # 相当于运行 uv pip install -e .
        subprocess.run(["uv", "pip", "install", "-e", "."], check=True)
        print("CLI tools installed: 'task-guard', 'server-monitor'")
    except FileNotFoundError:
        # 如果用户没装 uv，尝试用 pip
        subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."], check=True)
    except subprocess.CalledProcessError:
        print("Installation failed.")
        sys.exit(1)
    
    print("\n All set! Try running 'task-guard --help'")

if __name__ == "__main__":
    main()