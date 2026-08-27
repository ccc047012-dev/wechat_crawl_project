import requests, csv, io

# US Census CBSA/关税公开数据直连
# 尝试官方 HTS (Harmonized Tariff Schedule) 公开下载
urls = [
    ("USITC HTS 2025 Rev.1 full CSV", "https://hts.usitc.gov/reststop/file?source=htsRelease&release=2025HTSRevision1&filename=htsData.csv"),
    ("USITC HTS 2025 full CSV", "https://hts.usitc.gov/reststop/file?source=htsRelease&release=2025HTS&filename=htsData.csv"),
    ("USITC HTS 2024 CSV", "https://hts.usitc.gov/reststop/file?source=htsRelease&release=2024HTS&filename=htsData.csv"),
]
for name, u in urls:
    try:
        r = requests.get(u, timeout=30)
        print(f"{name}: HTTP {r.status_code} len={len(r.content)} ct={r.headers.get('Content-Type','')[:50]}")
        if r.status_code == 200 and len(r.content) > 1000:
            txt = r.content[:300].decode("utf-8", "replace")
            print("  HEADER: " + txt[:200].replace(chr(10), " "))
    except Exception as e:
        print(f"{name}: FAIL {type(e).__name__}: {str(e)[:70]}")