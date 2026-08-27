import requests

base = "https://wits.worldbank.org/API/V1/SDMX/V21/rest/data/DF_WITS_Tariff_TRAINS/"
# 测试不同 partner 维度: 000=世界, ALL
variants = [
    ("partner=000 (World)", "A.840.000.2020.610110.Reported"),
    ("partner=000 no time", "A.840.000.610110.Reported?startPeriod=2020&endPeriod=2020"),
    ("partner=ALL", "A.840.ALL.2020.610110.Reported"),
    ("USA MFN World HS61", "A.840.000.2020.610110.MFN"),
]
for name, key in variants:
    u = base + key
    try:
        r = requests.get(u, timeout=45, headers={"User-Agent":"Mozilla/5.0"})
        body = r.content.decode("utf-8", "replace")
        print(f"{name}: HTTP {r.status_code} len={len(r.content)}")
        print("  " + body[:400].replace(chr(10)," "))
    except Exception as e:
        print(f"{name}: FAIL {type(e).__name__}: {str(e)[:80]}")
    print()