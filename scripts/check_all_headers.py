import pandas as pd, os, glob

OUT = r"C:\Users\26936\wechat_crawl_project\raw_data"
for f in sorted(glob.glob(os.path.join(OUT, "comtrade_*monthly*.csv"))):
    name = os.path.basename(f)
    try:
        with open(f, "r", encoding="utf-8-sig") as fh:
            header = fh.readline().strip()
        ncols = len(header.split(","))
        print(f"{name}: 表头{len(header.split(','))}列")
    except Exception as e:
        print(f"{name}: 读取失败 {e}")