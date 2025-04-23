#!/user/bin/env python3
# _*_ coding: utf-8 _*_

from Utils import dataUtils
from Data import RF_data

country_list = ["Low SDI", "Low-middle SDI", "Middle SDI", "High-middle SDI", "High SDI", "China", "Global"]

# 解压数据
# dataUtils.unzipData()
# 合并数据
all_data = dataUtils.mergeData_with_ageId()

RF_data = RF_data(Deaths_data=all_data[all_data.measure_name == 'Deaths'],
                  DALYs_data=all_data[all_data.measure_name == 'DALYs (Disability-Adjusted Life Years)'],
                  Country=list(all_data.location_name.unique()),
                  year_start=1990,
                  year_end=2021)


####
# 获取dalys ASR和Deaths ASR 用于JP计算AAPC
RF_data.toJPData(["Deaths", "DALYs"], country_list=["High-middle SDI", "China", "Global"])

# # Death
# RF_data.get_table_data(index="Deaths")
# # DALYs
# RF_data.get_table_data(index="DALYs (Disability-Adjusted Life Years)")
#
# RF_data.age_5("Deaths", ["China", "High-middle SDI", "Global"])
# RF_data.age_5("DALYs (Disability-Adjusted Life Years)", ["China", "High-middle SDI", "Global"])
#
# RF_data.Lines(country_list=country_list, measure="Deaths", age="Age-standardized",
#               metrics="Rate", sex="Both")
#
# RF_data.Lines(country_list=["China", "High-middle SDI", "Global"],
#               measure="DALYs",
#               age="Age-standardized",
#               metrics="Rate",
#               sex="Both")
#
# RF_data.Line_sex(country_list=["High-middle SDI","China","Global"],
#                  measure="DALYs",
#                  age="Age-standardized",
#                  metrics="Rate")
#
# RF_data.Line_sex(country_list=["High-middle SDI", "China", "Global"],
#                  measure="Deaths",
#                  age="Age-standardized",
#                  metrics="Rate")
#
# RF_data.Bar_Number(country_list=["High-middle SDI", "China", "Global"],
#                    measure="Deaths",
#                    age="All ages",
#                    metrics="Number")
#
# RF_data.Bar_Number(country_list=["High-middle SDI", "China", "Global"],
#                    measure="DALYs",
#                    age="All ages",
#                    metrics="Number")
#
# # 合成ASXR
# RF_data.Merge_X_ASR("Deaths")
# RF_data.Merge_X_ASR("DALYs")
#
# # 生成散点
# RF_data.Scatter_country("Deaths", 10)
# RF_data.Scatter_country("DALYs", 10)
