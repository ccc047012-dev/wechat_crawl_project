import requests
import xml.etree.ElementTree as ET

r = requests.get("https://wits.worldbank.org/API/V1/SDMX/V21/rest/dataflow/WBG_WITS/DF_WITS_TradeStats_Tariff/1.0?references=all", timeout=50, headers={"User-Agent":"Mozilla/5.0"})
root = ET.fromstring(r.content)
ns = {"s": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message",
      "st": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure",
      "c": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common"}

for cl in root.findall(".//st:Codelist", ns):
    if cl.get("id") == "CL_TS_COUNTRY_WITS":
        codes = cl.findall(".//st:Code", ns)
        print(f"CL_TS_COUNTRY_WITS 共 {len(codes)} 个码:")
        # 查找美国和中国
        for code in codes:
            cid = code.get("id")
            n = code.find("c:Name", ns)
            name = n.text if n is not None else "?"
            if any(k in name.lower() for k in ["united", "china", "world", "usa"]):
                print(f"  {cid} | {name}")
        # 打印前30个码看格式
        print("\n前30个码:")
        for code in codes[:30]:
            cid = code.get("id")
            n = code.find("c:Name", ns)
            name = n.text if n is not None else "?"
            print(f"  {cid} | {name}")
        break