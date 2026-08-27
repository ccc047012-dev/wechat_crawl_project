import requests

print("=== DBnomics (FRED镜像, 无需key) ===")
tests = [
    ("DBnomics FRED DEXCHUS 搜索", "https://api.db.nomics.world/v22/series/FRED/DEXCHUS?observations=1"),
    ("DBnomics FRED GDP 搜索", "https://api.db.nomics.world/v22/series/FRED/GDP?observations=1"),
    ("DBnomics root", "https://api.db.nomics.world/v22/series/FRED/GDP"),
]
for name, u in tests:
    try:
        r = requests.get(u, timeout=30)
        ct = r.headers.get("Content-Type", "")
        print(f"{name}: HTTP {r.status_code} ct={ct[:40]} len={len(r.content)}")
        print("  " + r.text[:220].replace(chr(10), " "))
    except Exception as e:
        print(f"{name}: FAIL {type(e).__name__}: {str(e)[:70]}")

print()
print("=== WTO 关税数据库 ===")
tests2 = [
    ("WTO tariff main", "http://tariffdata.wto.org/ReportersAndProducts.aspx"),
    ("WTO tariff reporter USA", "http://tariffdata.wto.org/DataByReporter.aspx?Reporter=840"),
    ("WTO API?", "https://api.wto.org/timeseries/v1/tariff?i=840&pc=156&p=61&y=2020"),
]
for name, u in tests2:
    try:
        r = requests.get(u, timeout=25)
        print(f"{name}: HTTP {r.status_code} ct={r.headers.get('Content-Type','')[:30]} len={len(r.content)}")
        print("  " + r.text[:150].replace(chr(10), " "))
    except Exception as e:
        print(f"{name}: FAIL {type(e).__name__}: {str(e)[:70]}")

print()
print("=== BEA 静态Excel ===")
tests3 = [
    ("BEA NIPA Section1", "https://apps.bea.gov/national/Release/XLS/Survey/Section1All_xls.xlsx"),
    ("BEA API GDP nominal Q", "https://apps.bea.gov/api/data/?&UserID=bea-key&method=GetData&DataSetName=NIPA&TableName=T10101&Frequency=Q&Year=ALL&ResultFormat=CSV"),
]
for name, u in tests3:
    try:
        r = requests.get(u, timeout=30)
        print(f"{name}: HTTP {r.status_code} ct={r.headers.get('Content-Type','')[:40]} len={len(r.content)}")
        print("  " + r.text[:180].replace(chr(10), " "))
    except Exception as e:
        print(f"{name}: FAIL {type(e).__name__}: {str(e)[:70]}")