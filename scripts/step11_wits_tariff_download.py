# -*- coding: utf-8 -*-
import requests, xml.etree.ElementTree as ET, csv, os

OUT = r"C:\Users\26936\wechat_crawl_project\raw_data"
BASE = "https://wits.worldbank.org/API/V1/SDMX/V21/rest/data/DF_WITS_TradeStats_Tariff/"
NS = {"g": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic"}

GROUPS = [
    ("HidesSkin_41-43", "41-43_HidesSkin", ["42","43"]),
    ("TextCloth_50-63", "50-63_TextCloth", ["50","51","52","53","54","55","56","57","58","59","60","61","62","63"]),
    ("Footwear_64-67", "64-67_Footwear", ["64","65","66","67"]),
    ("Miscellan_90-99", "90-99_Miscellan", ["94","95","96"]),
]
INDICATORS = [
    ("MFN-SMPL-AVRG", "MFN_simple_avg_pct"),
    ("MFN-WGHTD-AVRG", "MFN_weighted_avg_pct"),
    ("AHS-SMPL-AVRG", "AHS_simple_avg_pct"),
    ("AHS-WGHTD-AVRG", "AHS_weighted_avg_pct"),
]

def fetch_tariff(product_code, indicator):
    key = f"A.USA.CHN.{product_code}.{indicator}?startPeriod=2015&endPeriod=2025"
    r = requests.get(BASE + key, timeout=60, headers={"User-Agent":"Mozilla/5.0"})
    if r.status_code != 200:
        return None
    root = ET.fromstring(r.content)
    rows = []
    for series in root.findall(".//g:Series", NS):
        for obs in series.findall("g:Obs", NS):
            dim = obs.find("g:ObsDimension", NS)
            val = obs.find("g:ObsValue", NS)
            if dim is not None and val is not None:
                rows.append((dim.get("value"), float(val.get("value"))))
    return rows

result_path = os.path.join(OUT, "WITS_USA_import_tariff_from_CHN_annual.csv")
with open(result_path, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["Year", "Group", "ProductCode", "Indicator", "Value_pct"])
    for group_name, pc, chapters in GROUPS:
        for ind, ind_name in INDICATORS:
            rows = fetch_tariff(pc, ind)
            print(f"{group_name} {ind_name}: {len(rows) if rows else 0}行")
            if rows:
                for year, v in rows:
                    w.writerow([year, group_name, pc, ind_name, v])
print("saved ->", result_path)