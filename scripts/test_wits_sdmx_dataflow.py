import requests

# WITS SDMX API 标准入口：列出可用 Dataflows
urls = [
    "https://wits.worldbank.org/API/V1/SDMX/V21/rest/dataflow/",
    "https://wits.worldbank.org/API/V1/SDMX/V21/rest/dataflow/ALL/latest",
]
for u in urls:
    try:
        r = requests.get(u, timeout=40, headers={"User-Agent":"Mozilla/5.0", "Accept":"application/xml"})
        print(f"{u}: HTTP {r.status_code} len={len(r.content)} ct={r.headers.get('Content-Type','')[:50]}")
        txt = r.content.decode("utf-8", "replace")
        print(txt[:800].replace(chr(10), " "))
        print()
    except Exception as e:
        print(f"{u}: FAIL {type(e).__name__}: {str(e)[:80]}")