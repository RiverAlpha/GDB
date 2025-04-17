#!/user/bin/env python3
# _*_ coding: utf-8 _*_
# 此类存储data对象
# 根据分析过程主要把数据进行以下分类
# 现基于 risk factor 进行业务数据分类
from paperData import paperData
import pandas as pd


class RF_data:

    def __init__(self, Deaths_data, DALYs_data, Country, year_start, year_end):
        # 此处数据为纯数据
        # 鉴于数据可能会有不同的情况 1.比如多个文件待合并 2.包含IDs 3.不包含IDs
        self.year_end = year_end
        self.year_start = year_start
        self.Country = Country
        self.DALYs_data = DALYs_data
        self.Deaths_data = Deaths_data

    def get_table_data(self, index):
        # 根据指标匹配数据
        if index == "Deaths":
            data = self.Deaths_data
        elif index == "DALYs (Disability-Adjusted Life Years)" or "DALYs":
            data = self.DALYs_data
        else:
            print("指标错误！！！！！")
            return -1
        Country = data.location_name.unique()
        # Number_data
        Numbers_index_data_1990 = data.loc[
            (data.measure_name == index) & (data.year == self.year_start) & (data.sex_name == 'Both') & (
                    data.metric_name == 'Number') & (data.age_name == "All ages")]
        Numbers_index_data_2023 = data.loc[
            (data.measure_name == index) & (data.year == self.year_end) & (data.sex_name == 'Both') & (
                    data.metric_name == 'Number') & (data.age_name == "All ages")]
        # ASR data
        Rate_index_data_1990 = data.loc[
            (data.measure_name == index) & (data.year == self.year_start) & (data.sex_name == 'Both') & (
                    data.metric_name == 'Rate') & (data.age_name == "Age-standardized")]
        Rate_index_data_2023 = data.loc[
            (data.measure_name == index) & (data.year == self.year_end) & (data.sex_name == 'Both') & (
                    data.metric_name == 'Rate') & (data.age_name == "Age-standardized")]
        tabel_data = pd.DataFrame({"country": Country})
        tabel_data[f'Number in {self.year_start} (95% CI)'] = list(
            Numbers_index_data_1990.val.round(2).astype(str) + " (" + Numbers_index_data_1990.lower.round(2).astype(
                str) + "~~" + Numbers_index_data_1990.upper.round(2).astype(str) + ")")
        tabel_data[f'Number in 2023 (95% CI)'] = list(
            Numbers_index_data_2023.val.round(2).astype(str) + " (" + Numbers_index_data_2023.lower.round(2).astype(
                str) + "~~" + Numbers_index_data_2023.upper.round(2).astype(str) + ")")
        tabel_data['Relative_change_of_numbers'] = [(a - b) * 100 / b for a, b in
                                                    zip(Numbers_index_data_2023.val.values,
                                                        Numbers_index_data_1990.val.values)]
        tabel_data[f'ASR in {self.year_start} (95% CI)'] = list(
            Rate_index_data_1990.val.round(2).astype(str) + " (" + Rate_index_data_1990.lower.round(2).astype(
                str) + "~~" + Rate_index_data_1990.upper.round(2).astype(str) + ")")
        tabel_data[f'ASR in {self.year_start} (95% CI)'] = list(
            Rate_index_data_2023.val.round(2).astype(str) + " (" + Rate_index_data_2023.lower.round(2).astype(
                str) + "~~" + Rate_index_data_2023.upper.round(2).astype(str) + ")")
        tabel_data['Relative_change_of_ASR'] = [(a - b) * 100 / b for a, b in
                                                zip(Rate_index_data_2023.val.values, Rate_index_data_1990.val.values)]
        tabel_data.to_csv(index + "_" + str(self.year_start) + "--" + str(self.year_end) + ".csv", index=False)
