import requests

# GitHub API 搜索 301 tariff HTS
queries = [
    ("US 301 tariff list HTS8", "https://api.github.com/search/repositories?q=US+301+tariff+list+HTS&per_page=10"),
    ("trade war tariffs data", "https://api.github.com/search/repositories?q=trade+war+tariffs+data&per_page=10"),
]
for name, u in queries:
    try:
        r = requests.get(u, timeout=40, headers={"User-Agent":"Mozilla/5.0", "Accept":"application/vnd.github+json"})
        print(f"{name}: HTTP {r.status_code} len={len(r.content)}")
        j = r.json()
        items = j.get("items", [])
        print(f"  仓库数: {len(items)}")
        for it in items[:10]:
            print("  -", it.get("full_name", "?"), "|", it.get("html_url", ""))
    except Exception as e:
        print(f"{name}: FAIL {type(e).__name__}: {str(e)[:80]}")