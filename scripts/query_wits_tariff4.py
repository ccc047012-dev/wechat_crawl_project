import requests
import xml.etree.ElementTree as ET

# 先用 DSD 中合法的产品码（从 CL_PRODUCTCODE_WITS 找 61 章 HS6 码）
r = requests.get("https://wits.worldbank.org/API/V1/SDMX/V21/rest/dataflow/WBG_WITS/DF_WITS_Tariff_TRAINS/1.1?references=all", timeout=50, headers={"User-Agent":"Mozilla/5.0"})
root = ET.fromstring(r.content)
ns = {"s": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message",
      "st": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure",
      "c": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common"}

ch61_codes = []
for cl in root.findall(".//st:Codelist", ns):
    if cl.get("id") == "CL_PRODUCTCODE_WITS":
        for code in cl.findall(".//st:Code", ns):
            cid = code.get("id")
            if cid.startswith("61"):
                ch61_codes.append(cid)
print("61章 HS6码示例:", ch61_codes[:20])
print("共", len(ch61_codes), "个码")

# 测试用第一个61章HS6码
if ch61_codes:
    test_code = ch61_codes[0]
    base = "https://wits.worldbank.org/API/V1/SDMX/V21/rest/data/DF_WITS_Tariff_TRAINS/"
    for key in [f"A.840.156.2020.{test_code}.Reported", f"A.840.156.2020.{test_code}.AVEEstimated"]:
        u = base + key
        r2 = requests.get(u, timeout=50, headers={"User-Agent":"Mozilla/5.0"})
        body = r2.content.decode("utf-8", "replace")
        print(f"\n查询 {key} -> HTTP {r2.status_code} len={len(r2.content)}")
        print(body[:800].replace(chr(10)," "))