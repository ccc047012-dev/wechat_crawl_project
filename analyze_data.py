# -*- coding: utf-8 -*-
"""Cloud-ready analysis: works on Windows / Codespaces / Actions - no absolute paths."""
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent
RAW = BASE / "raw_data"
PROC = BASE / "processed_data"
OUT = BASE / "output"
PROC.mkdir(exist_ok=True)
OUT.mkdir(exist_ok=True)


def read_csv_any(path, **kwargs):
    for enc in ("utf-8-sig", "utf-8", "gbk"):
        try:
            return pd.read_csv(path, encoding=enc, **kwargs)
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"cannot read {path}")


def main():
    logs = []

    trade_paths = sorted(RAW.glob("comtrade_USA_import_from_CHN_HS*_monthly_2015_2025.csv"))
    frames = []
    for p in trade_paths:
        chapter = p.stem.split("_HS")[1].split("_")[0]
        df = read_csv_any(p)
        if "period" not in df.columns or "cifvalue" not in df.columns:
            logs.append(f"[skip] {p.name}: missing period/cifvalue")
            continue
        grp = df.groupby("period", as_index=False).agg(
            cifvalue_usd=("cifvalue", "sum"),
            hs6_codes=("cmdCode", "nunique"),
            records=("cmdCode", "size"),
        )
        grp.insert(0, "chapter", chapter)
        frames.append(grp)

    if frames:
        trade = pd.concat(frames, ignore_index=True).sort_values(["chapter", "period"])
        trade.to_csv(OUT / "trade_monthly_by_chapter.csv", index=False, encoding="utf-8-sig")
        logs.append(f"trade by chapter: {trade.shape[0]} rows, {trade['chapter'].nunique()} chapters")
        total = trade.groupby("period", as_index=False)["cifvalue_usd"].sum()
        total.columns = ["period", "total_cifvalue_usd"]
    else:
        total = pd.DataFrame(columns=["period", "total_cifvalue_usd"])

    fx_path = PROC / "processed_exchange_rate_monthly.csv"
    if not fx_path.exists():
        dfx = read_csv_any(RAW / "akshare_CNYUSD_daily_boc.csv")
        dfx["日期"] = pd.to_datetime(dfx["日期"])
        dfx["YearMonth"] = dfx["日期"].dt.strftime("%Y%m")
        fx = dfx.groupby("YearMonth", as_index=False)["央行中间价"].mean()
        fx.columns = ["YearMonth", "CNY_per_USD"]
        fx["CNY_per_USD"] = (fx["CNY_per_USD"] / 100).round(6)
        fx.to_csv(fx_path, index=False, encoding="utf-8-sig")
    else:
        fx = read_csv_any(fx_path)
    logs.append(f"fx monthly: {fx.shape[0]} months")

    if not total.empty and not fx.empty:
        merged = total.merge(fx, left_on="period", right_on="YearMonth", how="left")
        merged["total_cifvalue_million_usd"] = (merged["total_cifvalue_usd"] / 1e6).round(3)
        keep = ["period", "total_cifvalue_usd", "total_cifvalue_million_usd", "CNY_per_USD"]
        merged = merged[[c for c in keep if c in merged.columns]]
        merged.to_csv(OUT / "trade_total_monthly.csv", index=False, encoding="utf-8-sig")
        logs.append(f"merged panel: {merged.shape[0]} rows, {merged['period'].min()}..{merged['period'].max()}")
    else:
        total.to_csv(OUT / "trade_total_monthly.csv", index=False, encoding="utf-8-sig")

    hs6_file = RAW / "comtrade_USA_import_from_CHN_202401_HS6_ALL.csv"
    if hs6_file.exists():
        hs6 = read_csv_any(hs6_file)
        if "cifvalue" in hs6.columns:
            top = hs6.sort_values("cifvalue", ascending=False).head(20)
            cols = [c for c in ["cmdCode", "cmdDesc", "cifvalue", "qty"] if c in top.columns]
            top[cols].to_csv(OUT / "top20_hs6_202401.csv", index=False, encoding="utf-8-sig")
            logs.append(f"2024-01 HS6: {hs6.shape[0]} codes, top20 saved")
    else:
        logs.append("[info] 202401 HS6 file not found")

    gdp_cn = PROC / "processed_China_GDP_quarterly.csv"
    if not gdp_cn.exists():
        src = RAW / "akshare_China_GDP_quarterly.csv"
        if src.exists():
            df = read_csv_any(src)
            df = df.rename(columns=lambda c: c.replace("-", "").replace(" ", ""))
            df.to_csv(gdp_cn, index=False, encoding="utf-8-sig")

    gdp_us = PROC / "processed_USA_GDP_quarterly.csv"
    if not gdp_us.exists():
        bea = RAW / "BEA_NIPA_Section1All.xlsx"
        if bea.exists():
            try:
                df = pd.read_excel(bea, sheet_name="T10105-Q", skiprows=7)
                gdp_row = df[df["Line"] == 1].iloc[0]
                q_cols = [c for c in df.columns if isinstance(c, str) and c[:4].isdigit() and "Q" in c]
                s = gdp_row[q_cols]
                s = s[[c for c in q_cols if 2015 <= int(c[:4]) <= 2025]]
                result = pd.DataFrame({"Quarter": s.index, "USA_GDP_nominal_millions": s.values})
                result.to_csv(gdp_us, index=False, encoding="utf-8-sig")
            except Exception as e:
                logs.append(f"[info] BEA extract failed: {type(e).__name__}: {e}")

    for name, p in [("China GDP", gdp_cn), ("USA GDP", gdp_us)]:
        if p.exists():
            logs.append(f"{name}: {read_csv_any(p).shape[0]} rows -> {p.name}")

    (OUT / "analysis_report.txt").write_text("\n".join(logs), encoding="utf-8")
    print("\n".join(logs))
    print("\n[done] outputs in", OUT)


if __name__ == "__main__":
    main()