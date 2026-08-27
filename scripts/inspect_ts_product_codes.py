import requests
import xml.etree.ElementTree as ET

r = requests.get("https://wits.worldbank.org/API/V1/SDMX/V21/rest/dataflow/WBG_WITS/DF_WITS_TradeStats_Tariff/1.0?references=all", timeout=50, headers={"User-Agent":"Mozilla/5.0"})
root = ET.fromstring(r.content)
ns = {"s": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message",
      "st": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure",
      "c": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common"}

for cl in root.findall(".//st:Codelist", ns):
    if cl.get("id") == "CL_TS_PRODUCTCODE_WITS":
        codes = cl.findall(".//st:Code", ns)
        print(f"共 {len(codes)} 个产品码:")
        for code in codes[:40]:
            cid = code.get("id")
            n = code.find("c:Name", ns)
            name = n.text if n is not None else "?"
            print(f"  {cid} | {name}")
        # 查找61章相关
        print("\n61章相关:")
        for code in codes:
            cid = code.get("id")
            if "61" in cid[:4] or (n := code.find("c:Name", ns)) is not None and "61" in (n.text or "")[:10]:
                n = code.find("c:Name", ns)
                print(f"  {cid} | {n.text if n is not None else '?'}")
        break