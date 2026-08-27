import requests

# USITC HTS API 需要从浏览器入口拿 token; 但可以先看其开放端点
paths = [
    "https://hts.usitc.gov/reststop/file?source=htsRelease&release=2024HTSRevision10",
    "https://hts.usitc.gov/api/search?q=6104",
    "https://hts.usitc.gov/reststop/search?q=6104",
]
for u in paths:
    try:
        r = requests.get(u, timeout=30, headers={"User-Agent":"Mozilla/5.0"})
        print(f"{u[:80]}: HTTP {r.status_code} len={len(r.content)} ct={r.headers.get('Content-Type','')[:40]}")
        print("  " + r.text[:200].replace(chr(10)," "))
    except Exception as e:
        print(f"{u[:80]}: FAIL {type(e).__name__}: {str(e)[:60]}")