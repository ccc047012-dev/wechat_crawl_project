import requests
import xml.etree.ElementTree as ET

# 获取完整 dataflow 列表并解析
r = requests.get("https://wits.worldbank.org/API/V1/SDMX/V21/rest/dataflow/ALL/latest", timeout=40, headers={"User-Agent":"Mozilla/5.0"})
root = ET.fromstring(r.content)
ns = {"s": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message",
      "st": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure",
      "c": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common"}
for df in root.findall(".//st:Dataflow", ns):
    df_id = df.get("id")
    agency = df.get("agencyID")
    name_el = df.find("c:Name", ns)
    name = name_el.text if name_el is not None else "?"
    print(f"{df_id} | {agency} | {name}")