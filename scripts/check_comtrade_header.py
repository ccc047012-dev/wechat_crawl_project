import requests

u = ("https://comtradeapi.un.org/public/v1/preview/C/M/HS"
     "?reporterCode=842&period=201501&partnerCode=156&flowCode=M&cmdCode=55*&maxRecords=3&format=csv")
r = requests.get(u, timeout=50)
print("HTTP", r.status_code)
print("--- 原始响应前3行 ---")
lines = r.text.splitlines()
print(lines[0])
print(lines[1] if len(lines) > 1 else "")
print()
print("响应头字段数:", len(lines[0].split(",")))
print("数据行字段数:", len(lines[1].split(",")) if len(lines) > 1 else 0)