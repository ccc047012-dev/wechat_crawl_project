import requests
import xml.etree.ElementTree as ET

# 测试有效 HS6 码查询 WITS 关税数据
base = "https://wits.worldbank.org/API/V1/SDMX/V21/rest/data/DF_WITS_Tariff_TRAINS/"
kines = [
    ("US import from China chap61 6101", "A.840.156.2020.6101.Reported"),
    ("US import from China chap61 ALL", "A.840.156.2020.61.Reported"),
    ("US import from China chap42 HS6", "A.840.156.2020.4201.Reported"),
]
for name, key in kines:
    u = base + key
    try:
        r = requests.get(u, timeout=50, headers={"User-Agent":"Mozilla/5.0"})
        body = r.content.decode("utf-8", "replace")
        print(f"{name}: HTTP {r.status_code} len={len(r.content)}")
        if "error" in body.lower() or "invalid" in body.lower():
            print("  ERROR MSG:", body[:300])
        else:
            print("  OK! 前300字符: " + body[:300].replace(chr(10), " "))
    except Exception as e:
        print(f"{name}: FAIL {type(e).__name__}: {str(e)[:80]}")
    print()