import requests

base = "https://wits.worldbank.org/API/V1/SDMX/V21/rest/data/DF_WITS_TradeStats_Tariff/"
variants = [
    ("USA-CHN 纺织品服装 MFN简均", "A.USA.CHN.50-63_TextCloth.MFN-SMPL-AVRG?startPeriod=2015&endPeriod=2025"),
    ("USA-CHN 纺织品服装 MFN加权", "A.USA.CHN.50-63_TextCloth.MFN-WGHTD-AVRG?startPeriod=2015&endPeriod=2025"),
    ("USA-CHN 鞋类 MFN简均", "A.USA.CHN.64-67_Footwear.MFN-SMPL-AVRG?startPeriod=2015&endPeriod=2025"),
]
for name, key in variants:
    u = base + key
    try:
        r = requests.get(u, timeout=60, headers={"User-Agent":"Mozilla/5.0"})
        body = r.content.decode("utf-8", "replace")
        print(f"{name}: HTTP {r.status_code} len={len(r.content)}")
        if "error" in body.lower() or "invalid" in body.lower():
            print("  " + body[:300])
        else:
            print("  " + body[:1000].replace(chr(10)," "))
    except Exception as e:
        print(f"{name}: FAIL {type(e).__name__}: {str(e)[:80]}")
    print()