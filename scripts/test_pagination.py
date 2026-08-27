import requests, csv, io

base = "https://comtradeapi.un.org/public/v1/preview/C/M/HS?reporterCode=842&period=202401&partnerCode=156&flowCode=M"

# 测试各种可能的分页参数
pagination_params = [
    "&page=2",
    "&pageNumber=2",
    "&offset=500",
    "&start=501",
    "&skip=500",
    "&pageNum=2",
    "&pageIndex=2",
    "&cursor=500",
]
for p in pagination_params:
    u = base + "&cmdCode=ALL&maxRecords=500&format=csv" + p
    try:
        r = requests.get(u, timeout=40)
        rows = list(csv.reader(io.StringIO(r.text)))
        data = rows[1:] if len(rows) > 1 else []
        if data:
            first_code = data[0][20] if len(data[0]) > 20 else "?"
            first_val = data[0][43] if len(data[0]) > 43 else "?"
            print(f"{p}: {len(data)} rows, firstCode={first_code}, val={first_val}")
        else:
            print(f"{p}: {len(data)} rows (empty)")
    except Exception as e:
        print(f"{p}: FAIL {type(e).__name__}")