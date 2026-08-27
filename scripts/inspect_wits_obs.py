import requests
import xml.etree.ElementTree as ET

base = "https://wits.worldbank.org/API/V1/SDMX/V21/rest/data/DF_WITS_TradeStats_Tariff/"
u = base + "A.USA.CHN.50-63_TextCloth.MFN-SMPL-AVRG?startPeriod=2015&endPeriod=2025"
r = requests.get(u, timeout=60, headers={"User-Agent":"Mozilla/5.0"})
root = ET.fromstring(r.content)

ns = {"g": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic",
      "c": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common",
      "m": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message"}

for series in root.findall(".//g:Series", ns)[:1]:
    for obs in series.findall("g:Obs", ns):
        print("Obs XML:", ET.tostring(obs, encoding='unicode')[:400])
        print()