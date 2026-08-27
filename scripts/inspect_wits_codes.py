import requests
import xml.etree.ElementTree as ET

# 获取 DATAFLOW 的 DSD 中 FREQ 和 DATATYPE codelist 的内容
r = requests.get("https://wits.worldbank.org/API/V1/SDMX/V21/rest/dataflow/WBG_WITS/DF_WITS_Tariff_TRAINS/1.1?references=all", timeout=40, headers={"User-Agent":"Mozilla/5.0"})
root = ET.fromstring(r.content)
ns = {"s": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message",
      "st": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure",
      "c": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common"}

# 找到 FREQ 相关的 Code 列表
for cl in root.findall(".//st:Codelist", ns):
    cl_id = cl.get("id")
    if cl_id in ("CL_FREQ_WITS", "CL_DATATYPE_WITS", "CL_TARIFFTYPE_WITS"):
        print(f"=== {cl_id} ===")
        for code in cl.findall(".//st:Code", ns)[:20]:
            cid = code.get("id")
            name_el = code.find("c:Name", ns)
            name = name_el.text if name_el is not None else "?"
            print(f"  code={cid} | name={name}")