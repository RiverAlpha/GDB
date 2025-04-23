#!/user/bin/env python3
# _*_ coding: utf-8 _*_
import pandas as pd
country_list = ["Low SDI", "Low-middle SDI", "Middle SDI", "High-middle SDI", "High SDI", "China", "Global"]
aapc_dalys = pd.read_csv("DALYs_AAPC.csv")
aapc_deatsh = pd.read_csv("deaths_aapc.csv")
print(aapc_deatsh[aapc_deatsh.location_name.isin(country_list)])
print(aapc_dalys[aapc_dalys.location_name.isin(country_list)])
