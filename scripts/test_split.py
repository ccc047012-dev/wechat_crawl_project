import requests, csv, io

base = "https://comtradeapi.un.org/public/v1/preview/C/M/HS?reporterCode=842&period=202401&partnerCode=156&flowCode=M"

# 测试各种拆分方式
variants = [
    ("wildcard 61*", "&cmdCode=61*&maxRecords=500"),
    ("wildcard 61%", "&cmdCode=61%&maxRecords=500"),
    ("6101 only", "&cmdCode=6101&maxRecords=500"),
    ("6101 + aggrLevel=6", "&cmdCode=6101&aggrLevel=6&maxRecords=500"),
    ("chapter 61 + aggrLevel=6", "&cmdCode=61&aggrLevel=6&maxRecords=500"),
    ("ALL + filter chapter 61", "&cmdCode=ALL&maxRecords=500&f=c1"),  # unlikely
]

for name, extra in variants:
    u = base + extra + "&format=csv"
    try:
        r = requests.get(u, timeout=40)
        rows = list(csv.reader(io.StringIO(r.text)))
        data = rows[1:] if len(rows) > 1 else []
        codes = [d[20] for d in data if len(d) > 20]
        print(f"{name}: {len(data)} rows, codes={codes[:6]}")
    except Exception as e:
        print(f"{name}: FAIL {type(e).__name__}: {str(e)[:60]}")