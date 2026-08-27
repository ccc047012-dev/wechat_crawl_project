import requests

print("=== WTO Tariff Download Facility ===")
# 官方下载设施端点, 支持 POST 生成 CSV
tests = [
    ("Wto Tariff Home", "https://tariffdata.wto.org/"),
    ("Wto Download Page", "https://tariffdata.wto.org/download.aspx"),
    ("Wto ApplyForm", "https://tariffdata.wto.org/applyforms.aspx"),
]
for name, u in tests:
    try:
        r = requests.get(u, timeout=25, headers={"User-Agent":"Mozilla/5.0"})
        print(f"{name}: HTTP {r.status_code} len={len(r.content)} ct={r.headers.get('Content-Type','')[:40]}")
        print("  "+r.text[:220].replace(chr(10)," "))
    except Exception as e:
        print(f"{name}: FAIL {type(e).__name__}: {str(e)[:60]}")

print()
print("=== 海关统计在线查询平台 ===")
tests2 = [
    ("海关平台root", "http://43.248.49.97/"),
]
for name, u in tests2:
    try:
        r = requests.get(u, timeout=25, headers={"User-Agent":"Mozilla/5.0"})
        print(f"{name}: HTTP {r.status_code} len={len(r.content)} ct={r.headers.get('Content-Type','')[:40]}")
        print("  "+r.text[:220].replace(chr(10)," "))
    except Exception as e:
        print(f"{name}: FAIL {type(e).__name__}: {str(e)[:60]}")