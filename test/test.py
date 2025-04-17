#!/user/bin/env python3
# _*_ coding: utf-8 _*_

from Utils import dataUtils
from Data import RF_data

# 解压数据
# dataUtils.unzipData()
# 合并数据
all_data = dataUtils.mergeData_with_ageId()

RF_data = RF_data(Deaths_data=all_data[all_data.measure_name == 'Deaths'],
                  DALYs_data=all_data[all_data.measure_name == 'DALYs (Disability-Adjusted Life Years)'],
                  Country=list(all_data.location_name.unique()),
                  year_start=1990,
                  year_end=2021)

RF_data.get_table_data(index="Deaths")
