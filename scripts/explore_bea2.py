# -*- coding: utf-8 -*-
import pandas as pd

path = r"C:\Users\26936\wechat_crawl_project\raw_data\BEA_NIPA_Section1All.xlsx"
# 解析 T10101-Q = 美国GDP (current dollars, quarterly)
df = pd.read_excel(path, sheet_name="T10101-Q", skiprows=7)
print("shape:", df.shape)
print("前几行:")
print(df.head(8).to_string())
print("\n列名:", list(df.columns))