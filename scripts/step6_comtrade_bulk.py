# -*- coding: utf-8 -*-
"""
后台下载：UN Comtrade 月度 HS6 数据
- 美国从中国进口 (reporter=842, partner=156, flow=M)
- 中国对美国出口 (reporter=156, partner=842, flow=X)
- 劳动密集型产品章节: 42,43,50-63,65-67,94,95,96  (共23章)
- 时间: 2015-01 至 2025-12  (132个月)
- 每章多码通配符下行 + 逐月循环, 每请求一行日志
- 渐进式保存: 每个章节一个CSV
"""
import requests, csv, io, os, time, sys, json
from pathlib import Path

OUT = str(Path(__file__).resolve().parent.parent / "raw_data")
LOG = os.path.join(OUT, "download_log.txt")
os.makedirs(OUT, exist_ok=True)

LABOR_CHAPTERS = ["42","43","50","51","52","53","54","55","56","57","58","59","60","61","62","63","64","65","66","67","94","95","96"]
MONTHS = []
for y in range(2015, 2026):
    for m in range(1, 13):
        MONTHS.append(f"{y}{m:02d}")

def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")

HEADER = ["typeCode","freqCode","refPeriodId","refYear","refMonth","period","reporterCode","reporterISO","reporterDesc",
          "flowCode","flowDesc","partnerCode","partnerISO","partnerDesc","partner2Code","classificationCode",
          "classificationSearchCode","isOriginalClassification","cmdCode","cmdDesc","aggrLevel","isLeaf",
          "customsCode","customsDesc","mosCode","motCode","motDesc","qtyUnitCode","qtyUnitAbbr","qty",
          "isQtyEstimated","altQtyUnitCode","altQtyUnitAbbr","altQty","isAltQtyEstimated","netWgt","isNetWgtEstimated",
          "grossWgt","isGrossWgtEstimated","cifvalue","fobvalue","primaryValue","legacyEstimationFlag",
          "isReported","isAggregate"]

# 初始化日志
open(LOG, "w", encoding="utf-8").close()
log(f"START bulk download: reporters US-China, chapters={LABOR_CHAPTERS}, months={MONTHS[0]}..{MONTHS[-1]}")

TASKS = [
    ("USA_import_from_CHN", "842", "156", "M"),
    ("CHN_export_to_USA", "156", "842", "X"),
]

for task_name, rep, part, flow in TASKS:
    log(f"=== TASK {task_name} ===")
    for ch in LABOR_CHAPTERS:
        out_file = os.path.join(OUT, f"comtrade_{task_name}_HS{ch}_monthly_2015_2025.csv")
        f_out = open(out_file, "w", newline="", encoding="utf-8-sig")
        writer = csv.writer(f_out)
        writer.writerow(HEADER)
        row_count = 0
        for period in MONTHS:
            url = (f"https://comtradeapi.un.org/public/v1/preview/C/M/HS"
                   f"?reporterCode={rep}&period={period}&partnerCode={part}"
                   f"&flowCode={flow}&cmdCode={ch}*&maxRecords=500&format=csv")
            ok = False
            for attempt in range(3):
                try:
                    r = requests.get(url, timeout=45)
                    if r.status_code == 200:
                        rows = list(csv.reader(io.StringIO(r.text)))
                        data = rows[1:]
                        for d in data:
                            # 对齐列数
                            if len(d) < len(HEADER):
                                d = d + [""] * (len(HEADER) - len(d))
                            writer.writerow(d[:len(HEADER)])
                        row_count += len(data)
                        ok = True
                        break
                    else:
                        log(f"  {task_name} {ch} {period} attempt{attempt+1} HTTP {r.status_code}")
                        time.sleep(2)
                except Exception as e:
                    log(f"  {task_name} {ch} {period} attempt{attempt+1} ERR {type(e).__name__}: {str(e)[:60]}")
                    time.sleep(2)
            if not ok:
                log(f"  FAIL {task_name} {ch} {period}")
            time.sleep(0.22)
        f_out.close()
        log(f"  DONE chapter HS{ch}: {row_count} rows -> {out_file}")
    log(f"=== TASK {task_name} FINISHED ===")
log("ALL TASKS FINISHED")