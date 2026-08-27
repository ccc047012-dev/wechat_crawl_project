# -*- coding: utf-8 -*-
import pandas as pd

path = r"C:\Users\26936\wechat_crawl_project\raw_data\BEA_NIPA_Section1All.xlsx"
for sheet in ["T10105-A", "T10105-Q"]:
    try:
        df = pd.read_excel(path, sheet_name=sheet, skiprows=7)
        print("=", sheet, "shape=", df.shape)
        print("  Line列头3行:")
        print(df.iloc[:3, :6].to_string())
        print()
    except Exception as e:
        print(sheet, "FAIL", e)