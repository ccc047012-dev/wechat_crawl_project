# -*- coding: utf-8 -*-
import pandas as pd

path = r"C:\Users\26936\wechat_crawl_project\raw_data\BEA_NIPA_Section1All.xlsx"
xls = pd.ExcelFile(path)
print("sheet数量:", len(xls.sheet_names))
print("前20个sheet:", xls.sheet_names[:20])