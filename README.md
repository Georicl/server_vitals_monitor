# Server Vitals Monitor (服务器生命体征监控)

**Server Vitals Monitor** is a automated system monitoring and task notification tool designed for Linux servers (especially for Bioinformatics). It not only tracks system resources (CPU/Memory) in real-time but also monitors long-running tasks and sends email notifications upon completion.

**Server Vitals Monitor** 是一个专为 Linux 服务器（特别是生物信息学环境）设计的自动化的系统监控与任务通知工具。它不仅能实时追踪系统资源（CPU/内存），还能监控长时间运行的任务，并在任务结束时发送邮件通知。

---

## ✨ Features (功能特性)

* **Real-time Monitoring**: Logs CPU and Memory usage every minute to CSV files.
    * **实时监控**：每分钟将 CPU 和内存使用率记录到 CSV 文件。
* **Data Persistence**: Auto-rotates logs daily to prevent file bloating.
    * **数据持久化**：按天自动切割日志，防止文件无限膨胀。
* **Visual Reports**: Generates trend charts (PNG/PDF) for the past 24 hours.
    * **可视化报表**：生成过去 24 小时的趋势图（PNG/PDF）。
* **Smart Alerts**: Sends daily emails with resource usage summaries and Top 5 resource-consuming processes.
    * **智能通知**：发送包含资源使用摘要和资源占用前五名进程的每日邮件。
* **Dual Mode Support**: Supports both modern Systemd (recommended) and traditional Crontab (for restricted environments) deployment.
    * **双模式支持**：支持现代 Systemd（推荐）和传统 Crontab（适用于受限环境）部署。
* **Privacy First**: Configuration is separated via `config.toml`, keeping sensitive credentials safe.
    * **隐私优先**：通过 `config.toml` 分离配置，保护敏感凭证安全。  
* **Task Guard**: Wraps around any shell command, monitors its execution time and exit status, and emails you when it finishes.  
    **守护任务**: 可以包裹任意 Shell 命令，监控其运行时间和退出状态，并在结束后发送邮件通知。  
---

## 🛠 Prerequisites (依赖与要求)

* **OS**: Linux (CentOS 7+, Ubuntu, Debian, etc.)
* **Python**: Version 3.12+ (Developed with 3.13)
* **Package Manager**: `uv` (Recommended) or `pip`

### Python Dependencies (Python 依赖)
The project relies on standard libraries and a few powerful external tools:
本项目依赖标准库以及以下第三方库：

* `psutil`: System monitoring / 系统监控
* `pandas`: Data processing / 数据处理
* `matplotlib`: Chart plotting / 图表绘制
* `tomllib` (Built-in Python 3.11+): Config parsing / 配置解析

**To install dependencies using uv:**
**使用 uv 安装依赖：**

```bash
uv add psutil pandas matplotlib  
```

# 🚀 Installation & Usage (安装与使用)  

## 1. Clone & Configure  
First, clone the repository and prepare the configuration file. 首先，克隆仓库并准备配置文件。  
```bash
git clone [https://github.com/your-username/server-vitals-monitor.git](https://github.com/your-username/server-vitals-monitor.git)
cd server-vitals-monitor

# Create config from template
# 从模板创建配置文件
cp config.example.toml config.toml
```  

## 2. Edit Configuration  

Open `config.toml` and fill in your email settings. 打开 `config.toml` 并填入你的邮箱配置。  
```toml  
[email]
enabled = true

# Example for Gmail / Gmail 示例
smtp_server = "smtp.gmail.com"
smtp_port = 587

# Example for 163 Mail (SSL) / 163邮箱示例 (SSL)
# smtp_server = "smtp.163.com"
# smtp_port = 465

sender_email = "your_email@example.com"
sender_password = "your_auth_code_here"

receiver_email = "admin@example.com"
```  

## 3.Deploy  
Run the one-click installation script. It attempts to set up a User-level Systemd Service. 运行一键安装脚本。它会尝试设置用户级Systemd 服务。  
```bash  
python3 install.py  
```  

## 4. Acitvate Task Guard CLI
The installer adds `~/bin` to your `$PATH`. You must restart your terminal or source your config to make `task_guard` available. 安装程序会自动将 `~/bin` 添加到你的 `$PATH`。你必须重启终端或 source 你的配置文件，才能让 `task_guard` 命令生效。  
```bash
source ~/.zshrc
# OR / 或
source ~/.bashrc
```  

# Usage: Task Guard
Use `task_guard` to run long tasks. You will receive an email with the Status (Success/Fail), Duration, and Exit Code when it finishes. 使用 `task_guard` 来运行长任务。任务结束时，你将收到一封包含状态（成功/失败）、耗时和退出码的邮件。  

```bash
nohup task_guard "command" &
```  


# ⚠️ Troubleshooting: If Systemd Fails (故障排查)

n some environments (e.g., Docker containers, HPC clusters, or other old systems), systemd --user might fail due to permission issues (cgroups error). 在某些环境（如 Docker 容器、HPC 集群或旧版系统）中，`systemd --user` 可能会因为权限问题（cgroups 错误）而无法运行。  

## Solution: Use Nohup + Crontab

If `install.py` reports an error, follow these manual steps: 如果 `install.py` 报错，请执行以下手动步骤：  

## Step 1: Start Monitor in Background (后台启动监控)

```bash
nohup python3 -u src/server_monitor/monitor.py > monitor.log 2>&1 &
```

## Step 2: Setup Daily Report Task (每日任务报表)  

Edit crontab (`crontab -e`) and add the following line (replace paths with your actual paths): 编辑定时任务 (`crontab -e`) 并添加以下内容（请将路径替换为你的实际路径）：  
```
# Run daily report at 00:10
10 0 * * * cd /path/to/server-vitals-monitor && /path/to/python3 src/server_monitor/daily_job.py --yesterday >> daily_job.log 2>&1

# (Optional) Auto-start monitor on reboot
# (可选) 开机自动启动监控
@reboot cd /path/to/server-vitals-monitor && nohup /path/to/python3 -u src/server_monitor/monitor.py > monitor.log 2>&1 &
```

# Management Commands (管理命令)

## Check Status (检查状态)

```bash
# If you used Systemd, use the following command
# Check Monitor Status / 检查监控状态
systemctl --user status vitals_monitor

# Check Daily Job Timer / 检查每日任务定时器
systemctl --user list-timers --all | grep vitals
```  

```bash
# If you used Nohup + Crontab, use the following command
# Check Monitor Process / 检查监控进程
ps -ef | grep monitor.py

# Check Logs / 查看日志
tail -f monitor.log
tail -f daily_job.log
```

## Stop Service(停止服务)

```bash
# If you used Systemd, use the following command
systemctl --user stop vitals_monitor
systemctl --user disable vitals_monitor
```

```bash
# If you used Nohup + Crontab, use the following command
# Kill the process / 杀掉进程
pkill -f monitor.py

# Remove cron job / 移除定时任务
crontab -e
# (Delete the relevant lines / 删除相关行)
```

# 📂 Project Structure (项目结构)

```PlainText
server-vitals-monitor/
├── config.toml              # [Private] Local config / 本地配置
├── config.example.toml      # Config template / 配置模板
├── data/                    # Logs & Reports / 数据存储
├── src/
│   ├── server_monitor/
│   │   ├── monitor.py       # Resource Logger / 资源记录器
│   │   ├── daily_job.py     # Daily Scheduler Entry / 日报入口
│   │   ├── plot_daily.py    # Plotting Logic / 绘图逻辑
│   │   ├── reporter.py      # Email Logic / 邮件发送核心
│   │   └── task_guard.py    # Task Monitor / 任务守卫核心
│   └── install_scripts/
│       ├── install_monitor.py
│       ├── install_plotter.py
│       └── install_cli.py   # CLI Installer / 命令行安装器
└── install.py               # Main Installer / 主安装入口
```

# 如果你喜欢这个项目，请将使用中遇到的问题联系我!