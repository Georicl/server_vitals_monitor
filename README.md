# Server Vitals Monitor (服务器生命体征监控)

**Server Vitals Monitor** is a lightweight and automated system monitoring tool designed for Linux servers. It records resource usage (CPU & Memory) in real-time, generates visual daily reports, and sends email notifications with snapshots of high-load processes.

**Server Vitals Monitor** 是一个轻量且自动化的 Linux 服务器监控工具。它能实时记录资源使用情况（CPU 和内存），生成可视化的每日报表，并发送包含高负载进程快照的邮件通知。

---

## ✨ Features (功能特性)

* **Real-time Monitoring**: Logs CPU and Memory usage every minute to CSV files.
    * **实时监控**：每分钟将 CPU 和内存使用率记录到 CSV 文件。
* **Data Persistence**: Auto-rotates logs daily to prevent file bloating.
    * **数据持久化**：按天自动切割日志，防止文件无限膨胀。
* **Visual Reports**: Generates trend charts (PNG/PDF) for the past 24 hours.
    * **可视化报表**：生成过去 24 小时的趋势图（PNG/PDF）。
* **Smart Alerts**: Sends daily emails with resource usage summaries and Top 3 resource-consuming processes.
    * **智能通知**：发送包含资源使用摘要和资源占用前三名进程的每日邮件。
* **Dual Mode Support**: Supports both modern Systemd (recommended) and traditional Crontab (for restricted environments) deployment.
    * **双模式支持**：支持现代 Systemd（推荐）和传统 Crontab（适用于受限环境）部署。
* **Privacy First**: Configuration is separated via `config.toml`, keeping sensitive credentials safe.
    * **隐私优先**：通过 `config.toml` 分离配置，保护敏感凭证安全。

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
├── config.toml              # [Ignored] Local configuration / 本地配置文件 (不上传)
├── config.example.toml      # Configuration template / 配置模板
├── data/                    # Logs and Reports storage / 日志和报表存储
│   ├── server_logs_YYYY-MM-DD.csv
│   └── report_YYYY-MM-DD.pdf
├── src/
│   ├── server_monitor/      # Core logic / 核心逻辑
│   │   ├── monitor.py       # Data collector / 数据采集
│   │   ├── daily_job.py     # Task entry / 任务入口
│   │   ├── reporter.py      # Email sender / 邮件发送
│   │   └── plot_daily.py    # Visualization / 绘图
│   └── install_scripts/     # Deployment scripts / 部署脚本
└── install.py               # Main installer / 主安装入口
```