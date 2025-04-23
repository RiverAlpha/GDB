#!/user/bin/env python3
# _*_ coding: utf-8 _*_
import pandas as pd
import matplotlib.pyplot as plt

country_list = ["Low SDI", "Low-middle SDI", "Middle SDI", "High-middle SDI", "High SDI"]

aapc_dalys = pd.read_csv("DALYs_AAPC.csv")[["location_name", "AAPC", "P-Value"]]
aapc_dalys = aapc_dalys[aapc_dalys.location_name.isin(country_list)]
print(aapc_dalys.location_name.values)
aapc_dalys['location_name'] = pd.Categorical(aapc_dalys['location_name'], categories=country_list, ordered=True)
aapc_dalys = aapc_dalys.sort_values('location_name')

aapc_deatsh = pd.read_csv("deaths_aapc.csv")[["location_name", "AAPC", "P-Value"]]
aapc_deatsh = aapc_deatsh[aapc_deatsh.location_name.isin(country_list)]
aapc_deatsh['location_name'] = pd.Categorical(aapc_deatsh['location_name'], categories=country_list, ordered=True)
aapc_deatsh = aapc_deatsh.sort_values('location_name')

plt.plot(country_list, aapc_deatsh.AAPC.values, label="aapc_deaths")
plt.plot(country_list, aapc_dalys.AAPC.values, label="aapc_dalys")
plt.xlabel("SDI")
plt.ylabel("AAPC")
plt.grid()
plt.legend()
plt.tight_layout(pad=0.1)  # 默认pad=1.08，减小这个值可以缩小边距
plt.savefig("AAPC_SDI.png")
plt.show()
