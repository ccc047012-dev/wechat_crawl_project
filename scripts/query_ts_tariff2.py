import requests

base = "https://wits.worldbank.org/API/V1/SDMX/V21/rest/data/DF_WITS_TradeStats_Tariff/"
variants = [
    ("USA import from CHN MFN weighted avg", "A.USA.CHN.61.MFN-WGHTD-AVRG?startPeriod=2015&endPeriod=2025"),
    ("USA import from CHN AHS weighted avg", "A.USA.CHN.61.AHS-WGHTD-AVRG?startPeriod=2015&endPeriod=2025"),
    ("USA import from CHN MFN simple avg", "A.USA.CHN.61.MFN-SMPL-AVRG?startPeriod=2015&endPeriod=2025"),
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
            print("  " + body[:800].replace(chr(10)," "))
    except Exception as e:
        print(f"{name}: FAIL {type(e).__name__}: {str(e)[:80]}")
    print()