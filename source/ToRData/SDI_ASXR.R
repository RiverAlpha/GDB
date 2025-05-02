setwd('D:\\PythonCode\\GDB\\source\\ToRData')
library(dplyr)
# 确保使用抗锯齿图形设备
options(bitmapType = "cairo")

DALYS <- read.csv('SDI_dalys_ASR.csv',header = T)  
# 筛选出2021年的数据
DALYS <- subset(DALYS,DALYS$year == 2021)
DALYS <- DALYS[,c(2,3,4,5)]
colnames(DALYS) <- c("location_name","year","val","SDI")

p1 <- ggplot(DALYS, aes(x = SDI, y = log(val+1))) +
  geom_point(alpha = 0.6, color = "black") +  # 黑色散点
  geom_smooth(
    method = "loess", 
    formula = y ~ x,
    se = TRUE,
    color = "blue",          # 蓝色曲线
    fill = "grey70",         # 灰色置信区间
    linewidth = 1.2,           # 加粗曲线
    alpha = 0.2              # 置信区间透明度
  ) +
  coord_cartesian(
    xlim = c(0.1, 0.9),    # 保持原图x轴范围
    ylim = c(0.32, 7)           # 强制y轴从0开始
  ) +
  scale_y_continuous(
    breaks = seq(0, 6, 2)    # 设置刻度(0,2,4,6)
  ) +
  labs(
    x = "SDI",
    y = expression(log(DALYs~ASR + 1))  # 修正数学符号显示
  ) +
  theme_minimal() +
  theme(
    panel.grid.major = element_line(color = "black"),  # 白色主网格线
    panel.grid.minor = element_blank(),                # 移除次要网格线
    panel.background = element_rect(fill = "white")    # 纯白背景
  )

p1

# 专业级输出（消除所有锯齿）
ggsave(
  "D:\\PythonCode\\GDB\\source\\ToRData\\DALYs_vs_SDI.tiff",
  device = "tiff",
  bg = "white",  # 显式设置背景色
  dpi = 1200,                  # 超高分辨率
  compression = "lzw",         # 无损压缩
  width = 8.27,                # A4纸宽度(英寸)
  height = 6,
  units = "in",
  type = "cairo"               # 强制启用抗锯齿
)

Deaths <- read.csv('SDI_deaths_ASR.csv',header = T)  
# 筛选出2021年的数据
Deaths <- subset(Deaths,Deaths$year == 2021)
Deaths <- Deaths[,c(2,3,4,5)]
colnames(Deaths) <- c("location_name","year","val","SDI")

p2 <- ggplot(Deaths, aes(x = SDI, y = log(val+1))) +
  geom_point(alpha = 0.6, color = "black") +  # 黑色散点
  geom_smooth(
    method = "loess", 
    formula = y ~ x,
    se = TRUE,
    color = "blue",          # 蓝色曲线
    fill = "grey70",         # 灰色置信区间
    linewidth = 1.2,           # 加粗曲线
    alpha = 0.2              # 置信区间透明度
  ) +
  coord_cartesian(
    xlim = c(0.1, 0.9),    # 保持原图x轴范围
    ylim = c(0, 2.8)           # 强制y轴从0开始
  ) +
  scale_y_continuous(
    breaks = seq(0, 6, 2)    # 设置刻度(0,2,4,6)
  ) +
  labs(
    x = "SDI",
    y = expression(log(Deaths~ASR + 1))  # 修正数学符号显示
  ) +
  theme_minimal() +
  theme(
    panel.grid.major = element_line(color = "black"),  # 白色主网格线
    panel.grid.minor = element_blank(),                # 移除次要网格线
    panel.background = element_rect(fill = "white")    # 纯白背景
  )

p2

# 专业级输出（消除所有锯齿）
ggsave(
  "D:\\PythonCode\\GDB\\source\\ToRData\\Deaths_vs_SDI.tiff",
  device = "tiff",
  bg = "white",  # 显式设置背景色
  dpi = 1200,                  # 超高分辨率
  compression = "lzw",         # 无损压缩
  width = 8.27,                # A4纸宽度(英寸)
  height = 6,
  units = "in",
  type = "cairo"               # 强制启用抗锯齿
)
