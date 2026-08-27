import requests
import xml.etree.ElementTree as ET

r = requests.get("https://wits.worldbank.org/API/V1/SDMX/V21/rest/dataflow/WBG_WITS/DF_WITS_TradeStats_Tariff/1.0?references=all", timeout=50, headers={"User-Agent":"Mozilla/5.0"})
root = ET.fromstring(r.content)
ns = {"s": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message",
      "st": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure",
      "c": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common"}

for cl in root.findall(".//st:Codelist", ns):
    cl_id = cl.get("id")
    if cl_id in ("CL_TS_FREQ_WITS", "CL_TS_INDICATOR_WITS", "CL_TS_DATASOURCE_WITS"):
        print(f"=== {cl_id} ===")
        for code in cl.findall(".//st:Code", ns)[:30]:
            n = code.find("c:Name", ns)
            print(f"  {code.get('id')} | {n.text if n is not None else '?'}")
        print()

# 国家码验证
for cl in root.findall(".//st:Codelist", ns):
    if cl.get("id") == "CL_TS_COUNTRY_WITS":
        for code in cl.findall(".//st:Code", ns):
            if code.get("id") in ("840","842","156","000"):
                n = code.find("c:Name", ns)
                print(f"国家 {code.get('id')} | {n.text if n is not None else '?'}")