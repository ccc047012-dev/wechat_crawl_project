import requests

key = "A.840.156.2020.61.Reported"
tests = [
    f"https://wits.worldbank.org/API/V1/SDMX/V21/rest/data/DF_WITS_Tariff_TRAINS/{key}",
    f"https://wits.worldbank.org/API/V1/SDMX/V21/rest/data/WBG_WITS,DF_WITS_Tariff_TRAINS,1.1/{key}",
    f"https://wits.worldbank.org/API/V1/SDMX/V21/rest/data/WBG_WITS,DF_WITS_Tariff_TRAINS/{key}",
    f"https://wits.worldbank.org/API/V1/SDMX/V21/rest/data/DF_WITS_Tariff_TRAINS,1.1/{key}",
]
for u in tests:
    try:
        r = requests.get(u, timeout=45, headers={"User-Agent":"Mozilla/5.0"})
        body = r.content.decode("utf-8", "replace")
        print(f"HTTP {r.status_code} len={len(r.content)} ct={r.headers.get('Content-Type','')[:45]}")
        print(u)
        print("  " + body[:300].replace(chr(10), " "))
        print()
    except Exception as e:
        print("FAIL", type(e).__name__, str(e)[:80])