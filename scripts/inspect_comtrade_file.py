import pandas as pd, os
OUT = r"C:\Users\26936\wechat_crawl_project\raw_data"

# 抽查一个已下载文件
p = os.path.join(OUT, "comtrade_USA_import_from_CHN_HS55_monthly_2015_2025.csv")
df = pd.read_csv(p)
print("shape:", df.shape)
print("列名:", list(df.columns))
print()
# 看一条记录的关键字段
cols = [c for c in ["period", "cmdCode", "cmdDesc", "qty", "qtyUnitAbbr", "primaryValue", "cifvalue", "fobvalue"] if c in df.columns]
print(df[cols].head(8).to_string())
print()
print("unique period数:", df["period"].nunique())
print("unique cmdCode数:", df["cmdCode"].nunique())
print("period范围:", df["period"].min(), "-", df["period"].max())