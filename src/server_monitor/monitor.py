import psutil
import time
import os
import sys
import signal
import csv

from datetime import datetime

# 配置
LOG_DIR = 'data'
INTERVAL = 60

def get_current_log_file():
    today = datetime.now().strftime('%Y-%m-%d')
    return os.path.join(LOG_DIR, f'server_logs_{today}.csv')

def ensure_file_ready(filepath):
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
        
    if not os.path.exists(filepath):
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'cpu_percent', 'memory_percent', 'memory_used_gb'])
            print(f"[{datetime.now()}] Create new log file: {filepath}")

def log_metrics():
    try:
        # 动态获取当前应写入的文件路径
        current_file = get_current_log_file()
        
        ensure_file_ready(current_file)

        # 采集数据
        now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cpu_pct = psutil.cpu_percent()
        mem = psutil.virtual_memory()
        mem_pct = mem.percent
        mem_used_gb = round(mem.used / (1024 ** 3), 2)

        # 写入数据
        with open(current_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([now_str, cpu_pct, mem_pct, mem_used_gb])

        # print(f"[{now_str}] CPU: {cpu_pct}% | Mem: {mem_pct}%")

    except Exception as e:
        print(f"Error logging metrics: {e}")

def signal_handler(sig, frame):
    print("\nStopping server vitals monitor...")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    
    print("=== Server Vitals Monitor Start ===")
    print(f"Gap: {INTERVAL} s")
    print(f"log dir: {os.path.abspath(LOG_DIR)}")
    
    psutil.cpu_percent(interval=None)
    
    while True:
        try:
            time.sleep(INTERVAL)
            log_metrics()
        except KeyboardInterrupt:
            break
    