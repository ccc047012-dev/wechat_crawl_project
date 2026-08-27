# -*- coding: utf-8 -*-
"""Comtrade HS6 月度数据稳健下载（断点续传 + 429指数退避）"""
import requests, csv, io, os, time, random, sys, json

OUT = r"C:\Users\26936\wechat_crawl_project\raw_data"
LOG = os.path.join(OUT, "download_log_v2.txt")
os.makedirs(OUT, exist_ok=True)

LABOR_CHAPTERS = ["42","43","50","51","52","53","54","55","56","57","58","59","60","61","62","63","64","65","66","67","94","95","96"]
MONTHS = [f"{y}{m:02d}" for y in range(2015,2026) for m in range(1,13)]
HEADER = ["typeCode","freqCode","refPeriodId","refYear","refMonth","period","reporterCode","reporterISO","reporterDesc","flowCode","flowDesc","partnerCode","partnerISO","partnerDesc","partner2Code","classificationCode","classificationSearchCode","isOriginalClassification","cmdCode","cmdDesc","aggrLevel","isLeaf","customsCode","customsDesc","mosCode","motCode","motDesc","qtyUnitCode","qtyUnitAbbr","qty","isQtyEstimated","altQtyUnitCode","altQtyUnitAbbr","altQty","isAltQtyEstimated","netWgt","isNetWgtEstimated","grossWgt","isGrossWgtEstimated","cifvalue","fobvalue","primaryValue","legacyEstimationFlag","isReported","isAggregate"]

TASKS = [
    ("USA_import_from_CHN", "842", "156", "M"),
    ("CHN_export_to_USA", "156", "842", "X"),
]

def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def already_done(path):
    """读取既有文件，返回已完成的 period 集合"""
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return set()
    done = set()
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            rd = csv.DictReader(f)
            for row in rd:
                p = row.get("period") or ""
                if p:
                    done.add(p.strip())
    except Exception:
        pass
    return done

def fetch(rep, part, flow, chapter, period, timeout=50):
    url = (f"https://comtradeapi.un.org/public/v1/preview/C/M/HS"
           f"?reporterCode={rep}&period={period}&partnerCode={part}"
           f"&flowCode={flow}&cmdCode={chapter}*&maxRecords=500&format=csv")
    return requests.get(url, timeout=timeout)

open(LOG, "w", encoding="utf-8").close()
log("START v2 (resume, exponential backoff)")

for task_name, rep, part, flow in TASKS:
    log(f"=== TASK {task_name} ===")
    for ch in LABOR_CHAPTERS:
        path = os.path.join(OUT, f"comtrade_{task_name}_HS{ch}_monthly_2015_2025.csv")
        done = already_done(path)
        pending = [p for p in MONTHS if p not in done]
        if not pending:
            log(f"  HS{ch}: 全部完成(跳过)")
            continue
        fout = open(path, "a", newline="", encoding="utf-8-sig")
        if os.path.getsize(path) == 0:
            w = csv.writer(fout)
            w.writerow(HEADER)
        n_ok = 0; n_fail = 0
        log(f"  HS{ch}: 待下载{len(pending)}个月 已完成{len(done)}个月")
        batch = 0
        for period in pending:
            success = False
            for attempt in range(6):
                try:
                    r = fetch(rep, part, flow, ch, period)
                    if r.status_code == 200:
                        rows = list(csv.reader(io.StringIO(r.text)))[1:]
                        w = csv.writer(fout)
                        for d in rows:
                            ext = d + [""] * (len(HEADER)-len(d))
                            w.writerow(ext[:len(HEADER)])
                        fout.flush()
                        n_ok += 1; success = True
                        break
                    elif r.status_code == 429:
                        wait = [15,30,60,90,120,180][attempt]
                        log(f"    HS{ch} {period} 429 -> 等{wait}s (attempt{attempt+1}/6)")
                        time.sleep(wait)
                    else:
                        log(f"    HS{ch} {period} HTTP{r.status_code} attempt{attempt+1}")
                        time.sleep([8,15,30,60,90,120][attempt])
                except Exception as e:
                    wait = [8,15,30,60,90,120][attempt]
                    log(f"    HS{ch} {period} ERR {type(e).__name__} {str(e)[:50]} -> 等{wait}s")
                    time.sleep(wait)
            if not success:
                n_fail += 1
                log(f"    !! HS{ch} {period} 放弃(6次失败)")
            batch += 1
            if batch % 15 == 0:
                time.sleep(random.uniform(4, 7))
            else:
                time.sleep(random.uniform(0.45, 0.9))
        fout.close()
        log(f"  HS{ch} 完成新下载: 成功{n_ok} 失败{n_fail} -> {path}")
    log(f"=== TASK {task_name} FINISHED ===")
log("ALL FINISHED")
print("SCRIPT END", flush=True)