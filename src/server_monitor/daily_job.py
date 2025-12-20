import argparse
import os
import sys
from datetime import datetime, timedelta

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))

if os.path.join(PROJECT_ROOT, "src") not in sys.path:
    sys.path.append(os.path.join(PROJECT_ROOT, "src"))

from server_monitor.plot_daily import plot_logs # noqa: E402
from server_monitor.reporter import send_daily_report # noqa: E402

DATA_DIR = os.path.join(PROJECT_ROOT, 'data')

def run_daily_job(target_date):
    print(f"=== [Daily Job] 开始执行: {target_date} ===")
    plot_logs(target_date)
    png_path = os.path.join(DATA_DIR, f'report_{target_date}.png')

    # 发送邮件
    send_daily_report(target_date, attachment_path=png_path)

    print("=== [Daily Job] 执行结束 ===")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', type=str, help='指定日期 (YYYY-MM-DD)')
    parser.add_argument('--yesterday', action='store_true', help='自动处理昨天的数据')
    
    args = parser.parse_args()
    
    target = args.date
    if args.yesterday:
        target = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    if not target:
        target = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        
    run_daily_job(target)