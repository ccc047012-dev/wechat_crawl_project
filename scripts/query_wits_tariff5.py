import requests

base = "https://wits.worldbank.org/API/V1/SDMX/V21/rest/data/DF_WITS_Tariff_TRAINS/"
# 尝试用 ALL 替代各维度，加上 startPeriod 参数
variants = [
    ("v1", base + "A.840.156.610110.Reported?startPeriod=2020&endPeriod=2020"),
    ("v2", base + "A.840.156.610110.Reported/all?startPeriod=2020&endPeriod=2020"),
    ("v3", base + "A.840.156.2020.610110.Reported/all"),
    ("v4 ALL key", base + "A.840.156.2020.ALL.Reported"),
    ("v5 product only", base + "A.840.156.2020.610110"),
]
for name, u in variants:
    try:
        r = requests.get(u, timeout=45, headers={"User-Agent":"Mozilla/5.0"})
        body = r.content.decode("utf-8", "replace")
        print(f"{name}: HTTP {r.status_code} len={len(r.content)}")
        if "Invalid" in body or "error" in body.lower():
            print("  " + body[:200])
        else:
            print("  FIRST300: " + body[:300].replace(chr(10)," "))
    except Exception as e:
        print(f"{name}: FAIL {type(e).__name__}: {str(e)[:80]}")
    print()