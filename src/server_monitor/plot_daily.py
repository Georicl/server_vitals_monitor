import pandas as pd
import matplotlib.pyplot as plt
import os
import argparse
import sys
from datetime import datetime, timedelta

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")


def plot_logs(target_date):
    csv_path = os.path.join(DATA_DIR, f"server_logs_{target_date}.csv")

    try:
        try:
            df = pd.read_csv(csv_path)

            df["timestamp"] = pd.to_datetime(df["timestamp"])
        except Exception as e:
            print(f"读取 CSV 失败: {e}")
            return

        if df.empty:
            print("empty daily log")
            return

        # draw plot
        plt.style.use("bmh")

        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

        # figure1 - cpu
        ax1.plot(
            df["timestamp"],
            df["cpu_percent"],
            label="CPU Usage (%)",
            color="#e74c3c",
            linewidth=1,
        )
        ax1.set_ylabel("CPU %")
        ax1.set_title(f"Server Vitals - {target_date}", fontsize=16)
        ax1.legend(loc="upper right")
        ax1.grid(True, linestyle="--", alpha=0.7)

        # figure 2&3 - mem
        ax2.plot(
            df["timestamp"],
            df["memory_percent"],
            label="Memory Usage (%)",
            color="#3498db",
            linewidth=1,
        )
        ax2.fill_between(
            df["timestamp"], df["memory_percent"], color="#3498db", alpha=0.2
        )
        ax2.set_ylabel("Memory %")
        ax2.set_ylim(0, 100)  # set mem limit 0-100%
        ax2.legend(loc="upper right")
        ax2.grid(True, linestyle="--", alpha=0.7)

        ax3.plot(
            df["timestamp"],
            df["memory_used_gb"],
            label="Memory Used (GB)",
            color="#2ecc71",
            linewidth=1,
        )
        ax3.set_ylabel("Memory (GB)")
        ax3.set_xlabel("Time")
        ax3.legend(loc="upper right")
        ax3.grid(True, linestyle="--", alpha=0.7)

        # automatic x-axis rotation
        fig.autofmt_xdate(rotation=45)
        plt.tight_layout()

        output_base = os.path.join(DATA_DIR, f"report_{target_date}")

        # save plot
        png_path = output_base + ".png"
        plt.savefig(png_path, dpi=150)

        pdf_path = output_base + ".pdf"
        plt.savefig(pdf_path)

        plt.close(fig)

    except Exception as e:
        print(f"drawing error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", type=str, help="指定日期 (YYYY-MM-DD)")
    parser.add_argument("--yesterday", action="store_true", help="自动分析昨天的数据")

    args = parser.parse_args()

    target = args.date
    if args.yesterday:
        target = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    if not target:
        # 默认也是昨天（符合定时任务逻辑）
        target = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    plot_logs(target)
