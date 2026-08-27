import requests
import xml.etree.ElementTree as ET

# 获取 NOMENCODE codelist 确认名称
r = requests.get("https://wits.worldbank.org/API/V1/SDMX/V21/rest/dataflow/WBG_WITS/DF_WITS_Tariff_TRAINS/1.1?references=all", timeout=50, headers={"User-Agent":"Mozilla/5.0"})
root = ET.fromstring(r.content)
ns = {"s": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message",
      "st": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure",
      "c": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common"}
for cl in root.findall(".//st:Codelist", ns):
    if cl.get("id") == "CL_NOMENCODE_WITS":
        for code in cl.findall(".//st:Code", ns):
            cid = code.get("id")
            name_el = code.find("c:Name", ns)
            name = name_el.text if name_el is not None else "?"
            print(f"{cid} | {name}")
        break

# 查找 CL_COUNTRY_WITS 中 840 是否是 USA
for cl in root.findall(".//st:Codelist", ns):
    if cl.get("id") == "CL_COUNTRY_WITS":
        print("\nCL_COUNTRY_WITS 部分码:")
        for code in cl.findall(".//st:Code", ns):
            cid = code.get("id")
            if cid in ("840", "842", "156", "152"):
                name_el = code.find("c:Name", ns)
                name = name_el.text if name_el is not None else "?"
                print(f"  {cid} | {name}")
        break