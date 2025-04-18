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


class RF_data:

    def __init__(self, Deaths_data, DALYs_data, Country, year_start, year_end):
        # 此处数据为纯数据
        # 鉴于数据可能会有不同的情况 1.比如多个文件待合并 2.包含IDs 3.不包含IDs
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
            plt.savefig(index + "_" + country + "_" + str(self.year_end) + ".png")

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
        plt.savefig(f"{measure}-{metrics}-{self.year_start}--{self.year_end}.png")

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
            plt.plot(x, female_data, label=f"{country} Male")
        plt.xlabel("year")
        if metrics == "Rate" and age == "Age-standardized":
            plt.ylabel(f"{measure} Rate (per 100,000)")
        elif metrics == "Rate" and age == "All ages":
            plt.ylabel(f"{measure} Rate (per 100,000)")
        elif metrics == "Number":
            plt.ylabel(f"{measure} Case")
        plt.legend()
        plt.grid()
        plt.savefig(f"{measure}-{metrics}_Males&Females.png")