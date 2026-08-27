import requests

base = "https://wits.worldbank.org/API/V1/SDMX/V21/rest/data/DF_WITS_Tariff_TRAINS/"
# 测试美国从中国进口 6101 章的关税数据在不同年份
for year in [2005, 2010, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]:
    u = base + f"A.840.156.610110.Reported?startPeriod={year}&endPeriod={year}"
    try:
        r = requests.get(u, timeout=45, headers={"User-Agent":"Mozilla/5.0"})
        body = r.content.decode("utf-8", "replace")
        print(f"year {year}: HTTP {r.status_code} len={len(r.content)} FIRST: {body[:100].replace(chr(10),' ')}")
    except Exception as e:
        print(f"year {year}: FAIL {type(e).__name__}: {str(e)[:60]}")