import sys
import os
import subprocess
import time
import argparse
from datetime import datetime

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))

if os.path.join(PROJECT_ROOT, "src") not in sys.path:
    sys.path.append(os.path.join(PROJECT_ROOT, "src"))

from server_monitor.reporter import send_email_core # noqa: E402

def finish_notice(command, exit_code, start_time, end_time, stdout_tail=None, stderr_tail=None):
    
    duration = end_time - start_time

    # 判断状态
    status_icon = "✅ 成功运行" if exit_code == 0 else "❌ 运行失败"

    subject = f"您的任务已经运行完毕: {status_icon} - {exit_code}"

    body = f"""
指定的任务命令
========================
执行命令: {command}

状态: {status_icon}
状态码 (Exit Code): {exit_code} (0 代表正常结束)

开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}
结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}
总耗时: {duration}

------------------------
此邮件由 Server Vitals Monitor (Task Guard) 自动发送。
"""
    if stderr_tail:
        body += f"\n错误输出 (stderr) 最后几行:\n{stderr_tail}\n"

    print(f"\n任务已结束, 正在发送邮件...")

    send_email_core(subject, body)


def run_and_watch(command):
    print(f"=== 任务启动 ===")
    print(f"执行命令: {command}\n")
    start_time = datetime.now()

    try:
        process = subprocess.Popen(command, shell=True)
        process.wait() # 等待结束
        exit_code = process.returncode
    
    except Exception as e:
        print(f"执行异常: {e}")
        exit_code = -999

    end_time = datetime.now()

    finish_notice(command, exit_code, start_time, end_time)

    sys.exit(exit_code)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="运行命令并在结束后发送邮件通知")
    parser.add_argument("command", type=str, help="要运行的完整命令，用引号包起来，例如 'sleep 5'")
    
    args = parser.parse_args()
    
    run_and_watch(args.command)