import requests
import xml.etree.ElementTree as ET

r = requests.get("https://wits.worldbank.org/API/V1/SDMX/V21/rest/dataflow/WBG_WITS/DF_WITS_Tariff_TRAINS/1.1?references=all", timeout=50, headers={"User-Agent":"Mozilla/5.0"})
root = ET.fromstring(r.content)
ns = {"s": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message",
      "st": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure",
      "c": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common"}

for dim in root.findall(".//st:Dimension", ns):
    dim_id = dim.get("id")
    print(f"\n=== Dimension {dim_id} ===")
    for child in dim:
        print(f"  {child.tag}: {child.attrib}")
        for sub in child:
            print(f"    {sub.tag}: {sub.attrib} text={sub.text}")

# 也找 PRODUCTCODE dimension 的 representation 的 enum ref