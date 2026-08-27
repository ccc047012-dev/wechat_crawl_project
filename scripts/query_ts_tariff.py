import requests

base = "https://wits.worldbank.org/API/V1/SDMX/V21/rest/data/DF_WITS_TradeStats_Tariff/"
# 测试美国从中国进口的 MFN/AHS 加权平均关税
variants = [
    ("USA-China AHS weighted avg", "A.840.156.61.AHS-WGHTD-AVRG?startPeriod=2015&endPeriod=2025"),
    ("USA-China MFN weighted avg", "A.840.156.61.MFN-WGHTD-AVRG?startPeriod=2015&endPeriod=2025"),
    ("USA-China MFN simple avg", "A.840.156.61.MFN-SMPL-AVRG?startPeriod=2015&endPeriod=2025"),
]
for name, key in variants:
    u = base + key
    try:
        r = requests.get(u, timeout=60, headers={"User-Agent":"Mozilla/5.0"})
        body = r.content.decode("utf-8", "replace")
        print(f"{name}: HTTP {r.status_code} len={len(r.content)}")
        if "error" in body.lower():
            print("  " + body[:250])
        else:
            print("  " + body[:500].replace(chr(10)," "))
    except Exception as e:
        print(f"{name}: FAIL {type(e).__name__}: {str(e)[:80]}")
    print()