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
        print(f'Usage: nohup {COMMAND_NAME} "your_command" &')
        print("-" * 40)

        # check PATH
        if bin_dir not in os.environ["PATH"]:
            print(
                f"    notice: {bin_dir} does not exist in $PATH environment variable."
            )
            print(
                "   Please run the following command (or add to .zshrc / .bashrc) to make it effective:"
            )
            print("   export PATH=$HOME/bin:$PATH")
    except Exception as e:
        print(f"Error: {e}")
        return False


def add_path_to_shell_config(bin_dir):
    home = os.path.expanduser("~")
    shell = os.environ.get("SHELL", "")
    config_file = None

    # Check for zsh or bash
    if "zsh" in shell:
        config_file = os.path.join(home, ".zshrc")
    elif "bash" in shell:
        bashrc = os.path.join(home, ".bashrc")
        bash_profile = os.path.join(home, ".bash_profile")
        if os.path.exists(bashrc):
            config_file = bashrc
        elif os.path.exists(bash_profile):
            config_file = bash_profile
        else:
            config_file = bashrc
    else:
        print(f"can not identify ({shell}) skip to add PATH。")
        return False, None

    export_line = f'export PATH="{bin_dir}:$PATH"'

    # check file exists
    content = ""
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            content = f.read()

    if bin_dir in content:
        print(f"{bin_dir} had in {config_file}")
        return True, config_file

    # add PATH
    try:
        with open(config_file, "a") as f:
            f.write(f"\n# Added by Server Vitals Monitor\n{export_line}\n")
        print(f"add PATH to: {config_file}")
        return True, config_file
    except Exception as e:
        print(f"error: {e}")
        return False, config_file


if __name__ == "__main__":
    install_cli_tool()
