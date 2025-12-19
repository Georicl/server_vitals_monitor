import psutil
import time
import os
import sys
import signal
import csv

from datetime import datetime

# 配置
LOG_FILE = 'data/server_logs.csv'
INTERVAL = 60

def write_header():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'cpu_percent', 'memory_percent', 'memory_used_gb'])
            print(f"[{datetime.now()}] 初始化日志文件: {LOG_FILE}")

def log_metrics():
    try:
        # 获取时间
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 获取CPU使用率
        cpu_pct = psutil.cpu_percent()

        # 获取内存使用率
        mem = psutil.virtual_memory()
        mem_pct = mem.percent
        mem_used_gb = round(mem.used / (1024 ** 3), 2)

        with open(LOG_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([now, cpu_pct, mem_pct, mem_used_gb])

        print(f"[{now}] CPU使用率: {cpu_pct}% | 内存使用率: {mem_pct}% | 内存使用量: {mem_used_gb}GB")

    except Exception as e:
        print(f"Error logging metrics: {e}")

def signal_handler(sig, frame):
    """优雅处理退出信号 (Ctrl+C)"""
    print("\n监控已停止。")
    sys.exit(0)

if __name__ == "__main__":
    # 注册退出信号
    signal.signal(signal.SIGINT, signal_handler)
    
    print("=== Server Vitals Monitor 启动 ===")
    print(f"监控间隔: {INTERVAL} 秒")
    print("按 Ctrl+C 停止监控")
    
    write_header()
    
    # 初次调用 cpu_percent 往往是 0，先预热一下
    psutil.cpu_percent(interval=None)
    
    while True:
        try:
            time.sleep(INTERVAL) # 等待
            log_metrics()        # 记录
        except KeyboardInterrupt:
            # 再次捕获以防万一
            break
