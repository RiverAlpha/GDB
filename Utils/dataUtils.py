#!/user/bin/env python3
# _*_ coding: utf-8 _*_
# 此类用于预处理原始文件
import math
import zipfile
import os
import pandas as pd

# 压缩包所在位置
zip_folder = "../source/zip"
# 解压缩之后文件所在文件夹
extract_folder = "../source/CsvData"


def unzipData():
    # 确保解压目录存在
    os.makedirs(extract_folder, exist_ok=True)

    # 遍历文件夹下所有的文件
    for filename in os.listdir(zip_folder):
        if filename.endswith(".zip"):
            zip_path = os.path.join(zip_folder, filename)

            # 解压Zip
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_folder)
                print(f"已解压：{filename}->{extract_folder}")
    print("解压完成")


# 读取文件下所有csv文件然后合并
# 根据国家进行排序
def mergeData_with_ageId():
    df_list = []
    for filename in os.listdir(extract_folder):
        if filename.endswith(".csv"):
            df_list.append(pd.read_csv(extract_folder + "/" + filename))

    alldata = pd.concat(df_list, axis=0)
    # 去掉多余的id
    alldata.drop(['measure_id', "location_id", "sex_id", "cause_id", "rei_id", "metric_id"], axis=1,
                 inplace=True)
    return alldata.sort_values(by="location_name")


# 输入两个数 a,b a向上增加得到d 得到最小的d能整除b
def smallest_divisible_d(a, b):
    return math.ceil(a / b) * b


