import requests
import xml.etree.ElementTree as ET

# 检查 DF_WITS_TradeStats_Tariff 数据流结构
r = requests.get("https://wits.worldbank.org/API/V1/SDMX/V21/rest/dataflow/WBG_WITS/DF_WITS_TradeStats_Tariff/1.0?references=all", timeout=50, headers={"User-Agent":"Mozilla/5.0"})
print("HTTP", r.status_code, "len", len(r.content))
if r.status_code == 200:
    root = ET.fromstring(r.content)
    ns = {"s": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message",
          "st": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure",
          "c": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common"}
    for dim in root.findall(".//st:Dimension", ns):
        print(f"Dimension: id={dim.get('id')} position={dim.get('position')}")
    for td in root.findall(".//st:TimeDimension", ns):
        print(f"TimeDimension: id={td.get('id')}")
    for cl in root.findall(".//st:Codelist", ns):
        print("Codelist:", cl.get("id"))
    # 列出 datatype codelist 内容
    for cl in root.findall(".//st:Codelist", ns):
        if cl.get("id") in ("CL_DATATYPE_WITS", "CL_FREQ_WITS"):
            print(f"=== {cl.get('id')} ===")
            for code in cl.findall(".//st:Code", ns)[:15]:
                n = code.find("c:Name", ns)
                print(f"  {code.get('id')} | {n.text if n is not None else '?'}")
else:
    print(r.text[:500])