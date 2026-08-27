import requests
import xml.etree.ElementTree as ET

r = requests.get("https://wits.worldbank.org/API/V1/SDMX/V21/rest/dataflow/WBG_WITS/DF_WITS_Tariff_TRAINS/1.1?references=all", timeout=50, headers={"User-Agent":"Mozilla/5.0"})
root = ET.fromstring(r.content)
ns = {"s": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message",
      "st": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure",
      "c": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common"}

# CL_PRODUCTCODE_WITS 内容
for cl in root.findall(".//st:Codelist", ns):
    if cl.get("id") == "CL_PRODUCTCODE_WITS":
        codes = cl.findall(".//st:Code", ns)
        print(f"CL_PRODUCTCODE_WITS 共 {len(codes)} 个码:")
        for code in codes[:60]:
            cid = code.get("id")
            name_el = code.find("c:Name", ns)
            name = name_el.text if name_el is not None else "?"
            print(f"  {cid} | {name}")
        break