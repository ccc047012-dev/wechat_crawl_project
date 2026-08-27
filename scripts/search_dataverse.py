import requests

# Harvard Dataverse 公开搜索API
queries = [
    ("trade war tariff 301", "https://dataverse.harvard.edu/api/search?q=trade+war+tariff+301&type=dataset&per_page=20"),
    ("US China tariffs HTS", "https://dataverse.harvard.edu/api/search?q=US+China+tariffs+HTS&type=dataset&per_page=20"),
]
for name, u in queries:
    try:
        r = requests.get(u, timeout=40, headers={"User-Agent":"Mozilla/5.0"})
        print(f"{name}: HTTP {r.status_code} len={len(r.content)}")
        j = r.json()
        items = j.get("data", {}).get("items", [])
        print(f"  结果数: {len(items)}")
        for it in items[:5]:
            print("  -", it.get("name", "?")[:100], "|", it.get("url", "")[:100])
    except Exception as e:
        print(f"{name}: FAIL {type(e).__name__}: {str(e)[:80]}")