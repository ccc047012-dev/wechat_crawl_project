import requests
import xml.etree.ElementTree as ET

# 查看 DF_WITS_Tariff_TRAINS 的数据结构定义 (DSD)
r = requests.get("https://wits.worldbank.org/API/V1/SDMX/V21/rest/dataflow/WBG_WITS/DF_WITS_Tariff_TRAINS/1.1?references=all", timeout=40, headers={"User-Agent":"Mozilla/5.0"})
root = ET.fromstring(r.content)
ns = {"s": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message",
      "st": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure",
      "c": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common"}

txt = r.content.decode("utf-8", "replace")
print("len:", len(txt))
# 查找 dimension
for dim in root.findall(".//st:Dimension", ns):
    dim_id = dim.get("id")
    pos = dim.get("position")
    print(f"Dimension: id={dim_id} position={pos}")
# 也查找 attribute
for attr in root.findall(".//st:Attribute", ns):
    attr_id = attr.get("id")
    print(f"Attribute: id={attr_id}")