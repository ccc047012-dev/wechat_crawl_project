import requests

# 学术数据集反向工程
urls = [
    ("Fajgelbaum data page", "https://doi.org/10.1093/qje/qjz024"),
    ("NBER SI 2019 tariffs", "https://www.nber.org/system/files/working_papers/w25638/w25638.zip"),
    ("Amiti Redding Weinstein data", "https://www.princeton.edu/~reddings/tradepolicy/data.htm"),
]
for name, u in urls:
    try:
        r = requests.get(u, timeout=30, headers={"User-Agent":"Mozilla/5.0"})
        print(f"{name}: HTTP {r.status_code} len={len(r.content)} ct={r.headers.get('Content-Type','')[:40]}")
    except Exception as e:
        print(f"{name}: FAIL {type(e).__name__}: {str(e)[:70]}")