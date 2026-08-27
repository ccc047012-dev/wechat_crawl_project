import requests
import xml.etree.ElementTree as ET

# 查找 TimeDimension
r = requests.get("https://wits.worldbank.org/API/V1/SDMX/V21/rest/dataflow/WBG_WITS/DF_WITS_Tariff_TRAINS/1.1?references=all", timeout=40, headers={"User-Agent":"Mozilla/5.0"})
root = ET.fromstring(r.content)
ns = {"s": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message",
      "st": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure",
      "c": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common"}
for td in root.findall(".//st:TimeDimension", ns):
    print("TimeDimension id=", td.get("id"))
    for ref in td:
        print("  ref:", ref.tag, ref.text)
# 打印 dimension list 完整结构
for dl in root.findall(".//st:DimensionList", ns):
    print("\nDimensionList attributes:", dl.attrib)
    for child in dl:
        print(" child:", child.tag, child.attrib)
# 查找 codelist 相关内容
for cl in root.findall(".//st:Codelist", ns):
    print("Codelist:", cl.get("id"))