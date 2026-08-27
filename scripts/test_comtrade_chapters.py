import requests, csv, io, time
base = "https://comtradeapi.un.org/public/v1/preview/C/M/HS?reporterCode=842&period=202401&partnerCode=156&flowCode=M"
chapters = ["61", "62", "63", "64", "42", "94", "95", "85"]
for ch in chapters:
    u = f"{base}&cmdCode={ch}&maxRecords=500&format=csv"
    try:
        r = requests.get(u, timeout=40)
        rows = list(csv.reader(io.StringIO(r.text)))
        first = rows[1] if len(rows) > 1 else None
        code = first[20] if first and len(first) > 20 else "-"
        val = first[43] if first and len(first) > 43 else "-"
        print(f"chapter {ch}: {len(rows)-1} rows, firstCode={code}, primaryValue={val}")
    except Exception as e:
        print(f"chapter {ch}: FAIL {type(e).__name__}: {e}")
    time.sleep(0.5)