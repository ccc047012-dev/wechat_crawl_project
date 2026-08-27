import requests

# 下载 BEA NIPA Section1 Excel
u = "https://apps.bea.gov/national/Release/XLS/Survey/Section1All_xls.xlsx"
r = requests.get(u, timeout=90)
path = r"C:\Users\26936\wechat_crawl_project\raw_data\BEA_NIPA_Section1All.xlsx"
open(path, "wb").write(r.content)
print(f"saved {len(r.content)} bytes -> {path}")

# BEA API 测试
r2 = requests.get("https://apps.bea.gov/api/data/?&UserID=BEA-KEY&method=GetData&DataSetName=NIPA&TableName=T10101&Frequency=Q&Year=ALL&ResultFormat=JSON", timeout=40)
print("BEA API:", r2.status_code, r2.text[:600])