import smtplib
import psutil
import os
from email.message import EmailMessage
from datetime import datetime
from .config_loader import load_config, get_config_value

def get_top_processes(n=3):
    processes = []

    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
        try:
            p_info = proc.info
            if not p_info['username']:
                p_info['username'] = "?"
            processes.append(p_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    sorted_processes = sorted(processes, key=lambda x: x['memory_percent'], reverse=True)[:n]

    report_str = "\n[当前内存占用 Top 3 进程]\n"
    report_str += f"{'PID':<8} {'用户':<10} {'MEM%':<8} {'进程名'}\n"
    report_str += "-" * 50 + "\n"

    for p in sorted_processes:
        # 防止 None 报错
        mem_val = round(p.get('memory_percent') or 0, 1)
        pid = p.get('pid')
        user = p.get('username')
        name = p.get('name')
        report_str += f"{pid:<8} {user:<10} {mem_val:<8} {name}\n"

    return report_str

def send_daily_report(date_str, attachment_path=None):
    config = load_config()

    if not get_config_value(config, "email", "enabled", False):
        return
    
    email_cfg = config.get("email", {})
    sender = email_cfg.get("sender_email")
    receiver = email_cfg.get("receiver_email")
    smtp_server = email_cfg.get("smtp_server")
    smtp_port = email_cfg.get("smtp_port")
    password = email_cfg.get("sender_password")

    if not all([sender, receiver, smtp_server, smtp_port, password]):
        print("邮件配置不完整，请检查")
        return
    
    print(f"email to {receiver}")

    msg = EmailMessage()
    msg['Subject'] = f"[{date_str}] 服务器运行日报 - Server Vitals"
    msg['From'] = sender
    msg['To'] = receiver

    cpu_now = psutil.cpu_percent(interval=1)
    mem_now = psutil.virtual_memory().percent

    thresholds = config.get("thresholds", {})
    # 默认值50,70
    cpu_warn = thresholds.get("cpu_warning_percent", 50)
    mem_warn = thresholds.get("memory_warning_percent", 70)

    status_str = "正常运行"

    if cpu_now > cpu_warn or mem_now > mem_warn:
        status_str = "高负载"

    top_procs = get_top_processes()

    body = f"""
这是 {date_str} 的服务器运行日报。
附件中包含了详细的 CPU 和内存波动图表。

[当前系统状态] {status_str}
CPU 使用率: {cpu_now}%
内存使用率: {mem_now}%

{top_procs}

此邮件由 Server Vitals Monitor 自动生成。
"""
    msg.set_content(body)

    # 添加附件，配合PNG图发送
    if attachment_path and os.path.exists(attachment_path):
        try:
            with open(attachment_path, 'rb') as f:
                file_data = f.read()
                file_name = os.path.basename(attachment_path)
                msg.add_attachment(file_data, maintype='application', subtype='png', filename=file_name)
        except Exception as e:
            print(f"无附件")
    else:
        print(f"无附件，将发送纯文字邮件")

    try:
        # 如果端口是 465，使用 SMTP_SSL
        if smtp_port == 465:
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.login(sender, password)
                server.send_message(msg)
        else:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls() 
                server.login(sender, password)
                server.send_message(msg)

        print(f"邮件已发送到 {receiver}")
    except Exception as e:
        print(f"邮件发送失败: {e}")