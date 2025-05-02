#!/user/bin/env python3
# _*_ coding: utf-8 _*_
# 此类存储data对象
# 根据分析过程主要把数据进行以下分类
# 现基于 risk factor 进行业务数据分类
from paperData import paperData
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from Utils import dataUtils
from adjustText import adjust_text


class RF_data:

    def __init__(self, Deaths_data, DALYs_data, Country, year_start, year_end, SDI_ASR_DEATH=None, SDI_ASR_DALYs=None,
                 AAPC_DATA=None):
        # 此处数据为纯数据
        # 鉴于数据可能会有不同的情况 1.比如多个文件待合并 2.包含IDs 3.不包含IDs
        self.AAPC_DATA = AAPC_DATA
        self.SDI_ASR_DALYs = SDI_ASR_DALYs
        self.SDI_ASR_DEATH = SDI_ASR_DEATH
        self.year_end = year_end
        self.year_start = year_start
        self.Country = Country
        self.DALYs_data = DALYs_data
        self.Deaths_data = Deaths_data

    # 获取变化表
    def get_table_data(self, index):
        # 根据指标匹配数据
        if index == "Deaths":
            data = self.Deaths_data
        elif index == "DALYs (Disability-Adjusted Life Years)" or "DALYs":
            data = self.DALYs_data
        else:
            print("指标错误！！！！！")
            return -1
        Ndata = data.loc[(data.measure_name == index)
                         & (data.year.isin([self.year_start, self.year_end]))
                         & (data.sex_name == 'Both')
                         & (data.metric_name == 'Number')
                         & (data.age_name == "All ages")][["location_name", "year", "val", "lower", "upper"]]

        Ndata = pd.merge(Ndata[Ndata.year == self.year_start], Ndata[Ndata.year == self.year_end], on=["location_name"])
        Ndata[f'Number in {self.year_start} (95% CI)'] = Ndata.val_x.round(2).astype(str) + "(" + Ndata.lower_x.round(
            2).astype(str) + "---" + Ndata.upper_x.round(2).astype(str) + ")"
        Ndata[f'Number in {self.year_end} (95% CI)'] = Ndata.val_y.round(2).astype(str) + "(" + Ndata.lower_y.round(
            2).astype(str) + "---" + Ndata.upper_y.round(2).astype(str) + ")"
        Ndata['Relative_change_of_numbers(%)'] = round(
            (Ndata.val_y - Ndata.val_x) * 100 / (self.year_end - self.year_start), 2)
        Ndata = Ndata[["location_name", f'Number in {self.year_start} (95% CI)', f'Number in {self.year_end} (95% CI)',
                       "Relative_change_of_numbers(%)"]]
        Rdata = data.loc[(data.measure_name == index)
                         & (data.year.isin([self.year_start, self.year_end]))
                         & (data.sex_name == 'Both')
                         & (data.metric_name == 'Rate')
                         & (data.age_name == "Age-standardized")][["location_name", "year", "val", "lower", "upper"]]
        Rdata = pd.merge(Rdata[Rdata.year == self.year_start], Rdata[Rdata.year == self.year_end], on=["location_name"])
        Rdata[f'Rate in {self.year_start} (95% CI)'] = Rdata.val_x.round(2).astype(str) + "(" + Rdata.lower_x.round(
            2).astype(str) + "---" + Rdata.upper_x.round(2).astype(str) + ")"
        Rdata[f'Rate in {self.year_end} (95% CI)'] = Rdata.val_y.round(2).astype(str) + "(" + Rdata.lower_y.round(
            2).astype(
            str) + "---" + Rdata.upper_y.round(2).astype(str) + ")"
        Rdata['Relative_change_of_Rate(%)'] = round(
            (Rdata.val_y - Rdata.val_x) * 100 / (self.year_end - self.year_start), 2)
        Rdata = Rdata[["location_name", f'Rate in {self.year_start} (95% CI)', f'Rate in {self.year_end} (95% CI)',
                       "Relative_change_of_Rate(%)"]]

        csv_data = pd.merge(Ndata, Rdata, on="location_name")
        plt.tight_layout()
        csv_data.to_csv(index + "_" + str(self.year_start) + "--" + str(self.year_end) + ".csv")

    # 某一指标下年龄段图像
    def age_5(self, index, country_list):
        # 根据指标匹配数据
        if index == "Deaths":
            data = self.Deaths_data
        elif index == "DALYs (Disability-Adjusted Life Years)" or "DALYs":
            index = "DALYs (Disability-Adjusted Life Years)"
            data = self.DALYs_data
        else:
            print("暂未收录该指标！")
            return -1
        # 筛选数据
        data = data[(data.location_name.isin(country_list))
                    & (data.year == self.year_end)
                    & (data.sex_name != "Both")
                    & (data.metric_name == "Rate")
                    & ~(data.age_name.isin(["All ages", "Age-standardized"]))].sort_values(
            by=['location_name', 'age_id'])

        for country in country_list:
            country_data = data[data.location_name == country]
            # 数据
            age_groups = country_data.loc[country_data.sex_name == 'Female'].age_name.unique()
            age_groups = [i.replace(" years", "") for i in age_groups]
            male_rates = country_data.loc[country_data.sex_name == 'Male'].val.values
            female_rates = country_data.loc[country_data.sex_name == 'Female'].val.values

            # 置信区间的上限和下限
            male_upper = country_data.loc[country_data.sex_name == 'Male'].upper.values
            male_lower = country_data.loc[country_data.sex_name == 'Male'].lower.values
            female_upper = country_data.loc[country_data.sex_name == 'Female'].upper.values
            female_lower = country_data.loc[country_data.sex_name == 'Female'].lower.values

            # 计算误差范围
            male_xerr = np.array(
                [np.array(male_rates) - np.array(male_lower), np.array(male_upper) - np.array(male_rates)])
            female_xerr = np.array(
                [np.array(female_rates) - np.array(female_lower), np.array(female_upper) - np.array(female_rates)])

            female_xerr_corrected = np.array([
                np.array(female_upper) - np.array(female_rates),  # 左误差（向正方向）
                np.array(female_rates) - np.array(female_lower)  # 右误差（向负方向）
            ])

            # 创建图表
            plt.figure(figsize=(10, 6))

            # 绘制男性患病率柱状图（右侧）
            plt.barh(age_groups, male_rates, xerr=male_xerr, color='blue', label='Male', capsize=5)

            # 绘制女性患病率柱状图（左侧）
            plt.barh(age_groups, [-rate for rate in female_rates], xerr=female_xerr_corrected, color='red',
                     label='Female',
                     capsize=5)
            # 添加零刻度线（黑色虚线）
            plt.axvline(0, color='black', linewidth=1, linestyle='--')

            # 显示网格
            plt.grid(True, alpha=0.7)
            # 添加标题和标签
            # plt.title(f'{index} Rate by Age Group and Sex', fontsize=16)
            plt.xlabel(f'{index} Rate (per 100,000 population)', fontsize=12)
            plt.ylabel('Age Group', fontsize=12)

            ## 自适应刻度 大于40间隔为2 大于100 间隔为10 大于400 间隔为50
            interval_max = max(max(male_upper), max(female_upper))
            if interval_max < 40:
                interval = 1
            elif interval_max < 100:
                interval = 5
            elif interval_max < 400:
                interval = 10
            elif interval_max < 1000:
                interval = 50
            else:
                interval = 100

            print(-math.ceil(max(female_upper)) - interval, math.ceil(max(male_upper)) + interval, interval)
            # 设置横坐标刻度和标签
            x_left = -dataUtils.smallest_divisible_d(abs(-math.ceil(max(female_upper)) - interval), interval)

            plt.xticks(np.arange(x_left, math.ceil(max(male_upper)) + interval, interval),
                       [str(abs(x)) for x in
                        np.arange(x_left, math.ceil(max(male_upper)) + interval, interval)],
                       fontsize=10)

            # 显示图例
            plt.legend(loc='upper left',  # 初始位置
                       bbox_to_anchor=(1.02, 1),  # 移到右侧图外（x=1.02 表示图外右侧）
                       borderaxespad=0)

            # 调整布局
            plt.tight_layout()
            plt.savefig("Age_group_" + index + "_" + country + "_" + str(self.year_end) + ".png")

    # 性别不共图
    def Lines(self, country_list, measure, age, metrics, sex):
        # 根据指标匹配数据
        if measure == "Deaths":
            data = self.Deaths_data
        elif measure == "DALYs (Disability-Adjusted Life Years)" or "DALYs":
            measure = "DALYs (Disability-Adjusted Life Years)"
            data = self.DALYs_data
        else:
            print("暂未收录该指标！")
            return -1
        #
        data = data[(data.location_name.isin(country_list))
                    & (data.sex_name == sex)
                    & (data.metric_name == metrics)
                    & (data.age_name == age)].sort_values(
            by=["location_name", "year"])
        plt.figure(figsize=(12, 8))
        x = list(data.year.unique())
        for country in country_list:
            plt.plot(x, list(data[data.location_name == country].val.values), label=country)
        plt.xlabel("year")
        if metrics == "Rate" and age == "Age-standardized":
            plt.ylabel(f"{measure} Rate (per 100,000)")
        elif metrics == "Rate" and age == "All ages":
            plt.ylabel(f"{measure} Rate (per 100,000)")
        elif metrics == "Number":
            plt.ylabel(f"{measure} Case")

        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.savefig(f"Line_{measure}-{metrics}-{self.year_start}--{self.year_end}.png")

    # 某指标下不同性别
    def Line_sex(self, country_list, measure, age, metrics):
        # 根据指标匹配数据
        if measure == "Deaths":
            data = self.Deaths_data
        elif measure == "DALYs (Disability-Adjusted Life Years)" or "DALYs":
            measure = "DALYs (Disability-Adjusted Life Years)"
            data = self.DALYs_data
        else:
            print("暂未收录该指标！")
            return -1
        #
        data = data[(data.location_name.isin(country_list))
                    & (data.sex_name != "Both")
                    & (data.metric_name == metrics)
                    & (data.age_name == age)].sort_values(
            by=["location_name", "year"])
        plt.figure(figsize=(12, 8))
        x = list(data.year.unique())
        for country in country_list:
            male_data = list(data[(data.sex_name == "Male") & (data.location_name == country)].val.values)
            female_data = list(data[(data.sex_name == "Female") & (data.location_name == country)].val.values)
            plt.plot(x, male_data, label=f"{country} Male", linestyle='-.')
            plt.plot(x, female_data, label=f"{country} Female")
        plt.xlabel("year")
        if metrics == "Rate" and age == "Age-standardized":
            plt.ylabel(f"{measure} Rate (per 100,000)")
        elif metrics == "Rate" and age == "All ages":
            plt.ylabel(f"{measure} Rate (per 100,000)")
        elif metrics == "Number":
            plt.ylabel(f"{measure} Case")
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.savefig(f"Line_sex_{measure}-{metrics}_Males&Females.png")

    # 柱状图（Number）
    def Bar_Number(self, country_list, measure, age, metrics):
        # 根据指标匹配数据
        if measure == "Deaths":
            data = self.Deaths_data
        elif measure == "DALYs (Disability-Adjusted Life Years)" or "DALYs":
            measure = "DALYs (Disability-Adjusted Life Years)"
            data = self.DALYs_data
        else:
            print("暂未收录该指标！")
            return -1
        data = data[(data.location_name.isin(country_list))
                    & (data.sex_name != "Both")
                    & (data.metric_name == metrics)
                    & (data.age_name == age)].sort_values(by=["location_name", "sex_name", "year"])

        year = list(data.year.unique())
        # 根据输入的国家进行绘制图的数量 并排描绘
        # 如果需要男女比例图 pie = True
        fig, axes = plt.subplots(len(country_list), 2, figsize=(15, 5 * len(country_list)))

        # 如果只有一个位置 调整axes的形状
        if len(country_list) == 1:
            axes = axes.reshape(1, -1)

        # 循环遍历每个位置
        for i, location in enumerate(country_list):
            # 获取当前位置的男性和女性数据
            male_data = list(data[(data['sex_name'] == "Male") &
                                  (data['location_name'] == location)].val.values)
            female_data = list(data[(data['sex_name'] == "Female") &
                                    (data['location_name'] == location)].val.values)
            # 绘制柱状图
            ax_bar = axes[i, 0]
            ax_bar.bar(year, male_data, label='Male')
            ax_bar.bar(year, female_data, bottom=male_data, label='Female')
            ax_bar.set_xlabel('year')
            ax_bar.set_ylabel('case (per 100,000)')
            ax_bar.set_title(f'{location} - {measure} by Year')
            ax_bar.legend()
            ax_bar.grid(True)

            # 绘制饼图
            ax_pie = axes[i, 1]
            sizes = [sum(male_data), sum(female_data)]
            labels = ['Male', 'Female']
            ax_pie.pie(sizes, labels=labels, autopct='%.1f%%')
            ax_pie.set_title(f'{location} - Gender Distribution')

        # 调整布局
        plt.tight_layout()
        # plt.suptitle("DALYs Number & Ratio by Location and Gender", y=1.02, fontsize=14)

        plt.savefig(f"Bar_{measure}_{metrics}_bar.png")

    # 合并ASXR数据 和SDI
    # num： 图中标注显示的国家数量（前几位）
    def Merge_X_ASR(self, measure):
        # 根据指标匹配数据
        if measure == "Deaths":
            data = self.Deaths_data
        elif measure == "DALYs (Disability-Adjusted Life Years)" or "DALYs":
            data = self.DALYs_data
        else:
            print("指标错误！！！！！")
            return -1
        # ASR趋势文件
        data = data[(data.sex_name == "Both")
                    & (data.metric_name == "Rate")
                    & (data.age_name.isin(["Age-standardized"]))].sort_values(
            by=['location_name', 'year'])
        data = data[["location_name", "year", "val"]]
        SDI_data = pd.read_csv("../source/comon_data/IHME_GBD_SDI_2021_SDI_1950_2021_Y2024M05D16.csv")
        SDI_data = SDI_data.rename(columns={"year_id": "year"})[["location_name", "year", "mean_value"]]
        SDI_data.sort_values(by=['location_name', 'year'])
        merged_df = pd.merge(data, SDI_data, on=['location_name', 'year'], how='inner')
        merged_df = merged_df[merged_df.year.isin([self.year_start, self.year_end])]
        # 去掉重复行
        merged_df[merged_df.duplicated(subset=['location_name', 'year'], keep=False)]
        # 处理重复值（取平均值）
        merged_df = merged_df.groupby(['location_name', 'year'], as_index=False).mean()

        if measure == "Deaths":
            self.SDI_ASR_DEATH = merged_df
        elif measure == "DALYs (Disability-Adjusted Life Years)" or "DALYs":
            self.SDI_ASR_DALYs = merged_df

    # 全球国家散点
    def Scatter_country(self, measure, num):
        # 根据指标匹配数据
        if measure == "Deaths":
            data = self.SDI_ASR_DEATH
        elif measure == "DALYs (Disability-Adjusted Life Years)" or "DALYs":
            data = self.SDI_ASR_DALYs
        else:
            print("指标错误！！！！！")
            return -1

        label_country = data[data.year == self.year_end].sort_values(by="val", ascending=False).head(
            num).location_name.unique()

        df_wide = data.pivot(index='location_name', columns='year', values=['mean_value', 'val'])
        # 计算 ASR 变化
        df_wide['ASR_Change'] = df_wide['val'][self.year_end] - df_wide['val'][self.year_start]
        df_wide['Increase'] = np.where(df_wide['ASR_Change'] > 0, 1, 0)

        # 重置索引
        df_wide = df_wide.reset_index()
        # 扁平化列名（解决多级列名问题）
        df_wide.columns = ['_'.join(map(str, col)) for col in df_wide.columns]

        # 计算值变化
        df_wide['val_Change'] = df_wide[f'val_{self.year_end}'] - df_wide[f'val_{self.year_start}']
        # 设置颜色
        df_wide['Color'] = np.where(df_wide['val_Change'] > 0, 'red', 'green')
        # 清理 location_name
        df_wide['location_name_'] = df_wide['location_name_'].str.strip().str.replace('\n', ' ')

        # 绘制散点图
        plt.figure(figsize=(12, 8))
        scatter = plt.scatter(df_wide[f'mean_value_{self.year_end}'],
                              df_wide[f'val_{self.year_end}'],
                              c=df_wide['Color'],
                              alpha=0.7)

        for color, label in zip(['red', 'green'], ['Increase', 'Decrease/No Change']):
            subset = df_wide[df_wide['Increase_'] == (1 if label == 'Increase' else 0)]
            plt.scatter(subset[f'mean_value_{self.year_end}'], subset[f'val_{self.year_end}'], color=color, label=label,
                        alpha=0.7)

        # 准备需要标注的国家列表
        countries_to_label = label_country

        # 使用adjust_text自动调整注释位置
        texts = []
        for i, row in df_wide.iterrows():
            if row['location_name_'] in countries_to_label:
                texts.append(plt.text(row[f'mean_value_{self.year_end}'],
                                      row[f'val_{self.year_end}'],
                                      row['location_name_'],
                                      fontsize=10,
                                      ha='center',
                                      va='center'))

        ## 自动调整注释位置避免重叠
        # adjust_text(texts,
        #             arrowprops=dict(arrowstyle='->', color='black', lw=0.5, alpha=0.5,  # 透明度
        #                             shrinkA=10,  # 起点收缩距离
        #                             shrinkB=10),
        #             expand_points=(1.5, 1.5),  # 扩大搜索空间
        #             expand_text=(1.2, 1.2),  # 扩大文本间距
        #             force_text=(0.5, 0.5),  # 调整文本间的排斥力
        #             only_move={'points': 'y', 'text': 'xy'})  # 限制移动方向

        # 自动调整注释位置避免重叠
        adjust_text(texts,
                    expand_points=(1.5, 1.5),  # 扩大搜索空间
                    expand_text=(1.2, 1.2),  # 扩大文本间距
                    force_text=(0.5, 0.5),  # 调整文本间的排斥力
                    only_move={'points': 'y', 'text': 'xy'})  # 限制移动方向

        # 添加标题和标签
        plt.title(f'{measure} ASR in {self.year_end} vs SDI (Compared to {self.year_start})', fontsize=16)
        plt.xlabel(f'SDI ({self.year_end})', fontsize=12)
        plt.ylabel(f'{measure} ASR ({self.year_end})', fontsize=12)

        # 添加网格
        plt.grid(True, alpha=0.3)
        plt.legend()

        plt.tight_layout()
        plt.savefig(f"Scatter_{measure}_{self.year_start}_{self.year_end}_Scatter.png")

    # 获取dalys ASR和Deaths ASR 用于JP计算AAPC
    def toJPData(self, measure_list, country_list):
        for measure in measure_list:
            # 根据指标匹配数据
            if measure == "Deaths":
                data = self.Deaths_data
            elif measure == "DALYs (Disability-Adjusted Life Years)" or "DALYs":
                data = self.DALYs_data
            else:
                print("指标错误！！！！！")
                return -1
            data = data[(data["age_name"] == "Age-standardized")
                        & (data["metric_name"] == "Rate")
                        & (data["sex_name"] == "Both")
                        & (data["location_name"].isin(country_list))].sort_values(
                by=["location_name", "year"])
            # 计算标准误差
            data["SE"] = (data.upper - data.lower) / (2 * 1.96)
            data = data[['location_name', 'year', 'val', 'SE']]
            data.rename(columns={"val": "AAPC"}, inplace=True)
            data.to_csv(f"../source/toJPData/{measure}_AAPC.csv")
