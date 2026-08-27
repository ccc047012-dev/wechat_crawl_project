# -*- coding: utf-8 -*-
import requests, csv, io, time, os, json

OUT = r"C:\Users\26936\wechat_crawl_project\raw_data"
os.makedirs(OUT, exist_ok=True)
base = "https://comtradeapi.un.org/public/v1/preview/C/M/HS?reporterCode=842&period=202401&partnerCode=156&flowCode=M"

all_rows = []
for ch in range(1, 98):
    ch_s = f"{ch:02d}"
    u = f"{base}&cmdCode={ch_s}*&maxRecords=500&format=csv"
    try:
        r = requests.get(u, timeout=40)
        rows = list(csv.reader(io.StringIO(r.text)))
        data = rows[1:] if len(rows) > 1 else []
        if data:
            for d in data:
                all_rows.append(d)
            print(f"ch {ch_s}: {len(data)} codes (total={len(all_rows)})", flush=True)
        time.sleep(0.3)
    except Exception as e:
        print(f"ch {ch_s}: FAIL {type(e).__name__}: {str(e)[:50]}", flush=True)

# 保存 2024-01 的美国从中国进口全部 HS6 商品（金额、数量）
if all_rows:
    header = ["typeCode","freqCode","refPeriodId","refYear","refMonth","period","reporterCode",
              "flowCode","partnerCode","classificationCode","cmdCode","cmdDesc","aggrLevel",
              "isLeaf","customsCode","customsDesc","motCode","motDesc","qtyUnitCode","qtyUnitAbbr",
              "qty","isQtyEstimated","altQtyUnitCode","altQtyUnitAbbr","altQty","isAltQtyEstimated",
              "netWgt","isNetWgtEstimated","grossWgt","isGrossWgtEstimated","cifvalue","fobvalue",
              "primaryValue","legacyEstimationFlag","isReported","isAggregate"]
    out_path = os.path.join(OUT, "comtrade_USA_import_from_CHN_202401_HS6_ALL.csv")
    with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(all_rows)
    print(f"\nSAVED {len(all_rows)} rows -> {out_path}")
else:
    print("NO DATA")