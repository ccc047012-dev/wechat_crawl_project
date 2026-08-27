import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# 抓取 USTR 301 页面里的文件链接
r = requests.get("https://ustr.gov/issue-areas/enforcement/section-301-investigations/tariff-actions", timeout=35, headers={"User-Agent":"Mozilla/5.0"})
soup = BeautifulSoup(r.text, "html.parser")
print("USTR页面标题:", soup.title.string if soup.title else "")
for a in soup.find_all("a", href=True):
    href = a["href"].lower()
    if any(k in href for k in [".pdf", ".xls", ".xlsx", ".csv", "file", "download"]):
        print("FILE LINK:", urljoin("https://ustr.gov", a["href"]), "|", a.get_text(strip=True)[:80])