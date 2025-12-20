import os
import sys
import stat


COMMAND_NAME = "task_guard"
SCRIPT_REL_PATH = "src/server_monitor/task_guard.py"

def install_cli_tool():
    print("=== Installing CLI task guard ===")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "../../"))   
    target_script = os.path.join(project_root, SCRIPT_REL_PATH)
    python_exe = sys.executable

    # install dir
    user_home = os.path.expanduser("~")
    bin_dir = os.path.join(user_home, "bin")

    if not os.path.exists(bin_dir):
        print(f"Creating directory: {bin_dir}")
        os.makedirs(bin_dir)

    wrapper_content = f"""#!/bin/bash
# Server Vitals Monitor - CLI Wrapper
# task guard

exec "{python_exe}" "{target_script}" "$@"
"""
    dest_path = os.path.join(bin_dir, COMMAND_NAME)

    try:
        with open(dest_path, "w") as f:
            f.write(wrapper_content)

        st = os.stat(dest_path)
        os.chmod(dest_path, st.st_mode | stat.S_IEXEC)

        print(f"generated short cut command: {dest_path}")
        print("-" * 40)
        print(f"Usage: nohup {COMMAND_NAME} \"your_command\" &")
        print("-" * 40)

        # check PATH
        if bin_dir not in os.environ["PATH"]:
            print(f"    notice: {bin_dir} does not exist in $PATH environment variable.")
            print("   Please run the following command (or add to .zshrc / .bashrc) to make it effective:")
            print(f"   export PATH=$HOME/bin:$PATH")
    except Exception as e:
        print(f"Error: {e}")
        return False
    
if __name__ == "__main__":
    install_cli_tool()