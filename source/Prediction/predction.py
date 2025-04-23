#!/user/bin/env python3
# _*_ coding: utf-8 _*_
import pandas as pd
import matplotlib.pyplot as plt

metrics = ["Number", "Rate"]
measures = ["DALYs", "Deaths"]
sexs = ["Male", "Female"]
for measure in measures:
    for sex in sexs:
        rate = pd.read_csv(f"prediction_{measure}_Rate_{sex}.csv")
        case = pd.read_csv(f"prediction_{measure}_Num_{sex}.csv")

        # 创建画布和坐标轴
        fig, ax1 = plt.subplots(figsize=(8, 5))

        # 绘制柱状图（左侧Y轴）
        ax1.bar(list(case.year.values)[:33], list(case["number"])[:33], color='skyblue', width=0.8)
        ax1.bar(list(case.year.values)[32:], list(case["number"])[32:], color='orange', width=0.8)
        ax1.set_xlabel('Year')
        ax1.set_ylabel('Number', color='black')
        ax1.tick_params(axis='y', labelcolor='black')

        # 创建第二个Y轴（右侧Y轴）
        ax2 = ax1.twinx()
        ax2.plot(list(case.year.values)[:33], list(rate["mean"] * 100000)[:33], color='green')
        ax2.plot(list(case.year.values)[32:], list(rate["mean"] * 100000)[32:], '-.', color='red')
        # 检测rate最高
        ax2.set_ylim(0, max(list(rate["mean"] * 100000))*1.1)
        ax2.set_ylabel('Age-standardized Rate (per 100,000)', color='black')
        ax2.tick_params(axis='y', labelcolor='black')
        # 添加垂直线（例如标记2020年）
        ax1.axvline(
            x=2021,  # 垂直线的位置（年份）
            color='black',  # 线条颜色
            linestyle='--',  # 线型（虚线）
            linewidth=2,  # 线宽
            alpha=0.7,  # 透明度
        )
        # 添加标题和图例
        plt.title(f'{sex} DALYs')
        # fig.legend(loc='upper right', bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes)
        plt.tight_layout()
        plt.savefig(f"Prediction_{measure}_{sex}.png")
        plt.show()
