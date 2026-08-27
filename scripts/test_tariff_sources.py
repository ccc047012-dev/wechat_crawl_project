import requests

# 美国海关与边境保护局 CBP 或 Census 关税相关公开数据
# 1) USITC public 下载端点 (已知格式)
paths = [
    "https://www.usitc.gov/publications/tariff_affairs/pub_tariffs.htm",
]
for u in paths:
    try:
        r = requests.get(u, timeout=25)
        print(u, "->", r.status_code, len(r.content))
    except Exception as e:
        print(u, "FAIL", str(e)[:70])

# 2) 世界银行 WITS TRAINS 的批量下载公共端点
wits_urls = [
    "https://wits.worldbank.org/data/public/WITSAPI/public/REST/country/ALL/partner/ALL/product/42/indicator/MPRT-TARF/year/2020/datasource/trn/format/json",
    "https://wits.worldbank.org/wits/wits/witshelp/Content/Data_Retrieval/T_and_T/Intro_T2.htm",
]
for u in wits_urls:
    try:
        r = requests.get(u, timeout=25)
        print("WITS", u, "->", r.status_code, len(r.content), r.headers.get("Content-Type","")[:40])
        print("  ", r.text[:200].replace(chr(10)," "))
    except Exception as e:
        print("WITS FAIL", str(e)[:70])