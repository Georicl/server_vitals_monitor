library(tidyverse)
library(lubridate)


# 输入地址
file_path <- "/Users/georicl/Documents/python_program/server_vitals_monitor/data/monitor/server_logs.csv"

if (!file.exists(file_path)) {
  stop("错误：找不到日志文件。请先运行 rsync 同步数据。")
}

data = read_csv(file_path, show_col_types = FALSE) %>%
    mutate(timestamp = ymd_hms(timestamp))

# 只画一天
plot_data = data %>%
   filter(timestamp >= (max(timestamp) - hours(24)))

# 绘图
p <- ggplot(plot_data, aes(x = timestamp, y = memory_percent)) +
  # 绘制线条
  geom_line(color = "#2c3e50", linewidth = 1) +
  # 填充线下区域，增加可视性
  geom_area(fill = "#3498db", alpha = 0.2) +
  # 添加平滑趋势线 (可选)
  geom_smooth(method = "loess", span = 0.1, color = "red", se = FALSE, linetype = "dashed") +
  # 设置标题和标签
  labs(
    title = "服务器内存使用率波动 (过去24小时)",
    subtitle = paste("最后更新:", max(plot_data$timestamp)),
    x = "时间",
    y = "内存使用率 (%)"
  ) +
  # 优化坐标轴：y轴范围固定 0-100，x轴时间格式
  scale_y_continuous(limits = c(0, 100)) +
  scale_x_datetime(date_labels = "%H:%M", date_breaks = "2 hours") +
  # 使用简洁主题
  theme_minimal() +
  theme(
    plot.title = element_text(face = "bold", size = 16),
    axis.text.x = element_text(angle = 45, hjust = 1)
  )

# 保存
print(p)
ggsave("memory_usage_24h.png", p, width = 10, height = 6)
print("图表已生成：memory_usage_24h.png")