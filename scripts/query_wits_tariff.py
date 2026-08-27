import requests
import xml.etree.ElementTree as ET

# 构造 SDMX 数据查询 (正确维度顺序)
# FREQ=A, REPORTER=840(美国), PARTNER=156(中国), TIME_PERIOD=2020, PRODUCTCODE=61, DATATYPE=Reported
base = "https://wits.worldbank.org/API/V1/SDMX/V21/rest/data/WBG_WITS/DF_WITS_Tariff_TRAINS/1.1/"
key = "A.840.156.2020.61.Reported"
u = base + key
print("Query:", u)
try:
    r = requests.get(u, timeout=50, headers={"User-Agent":"Mozilla/5.0", "Accept":"application/xml"})
    print(f"HTTP {r.status_code} len={len(r.content)} ct={r.headers.get('Content-Type','')[:60]}")
    txt = r.content.decode("utf-8", "replace")
    print(txt[:900].replace(chr(10)," "))
except Exception as e:
    print("FAIL", type(e).__name__, str(e)[:80])