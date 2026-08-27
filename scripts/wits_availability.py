import requests

# SDMX availability 端点确认美国关税数据覆盖
av_url = "https://wits.worldbank.org/API/V1/SDMX/V21/rest/availableconstraint/DF_WITS_Tariff_TRAINS/A.840"
try:
    r = requests.get(av_url, timeout=60, headers={"User-Agent":"Mozilla/5.0"})
    print(f"availability: HTTP {r.status_code} len={len(r.content)}")
    body = r.content.decode("utf-8", "replace")
    print(body[:2000])
except Exception as e:
    print("FAIL", type(e).__name__, str(e)[:80])