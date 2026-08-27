# -*- coding: utf-8 -*-
import pandas as pd, os
from pathlib import Path

BASE = Path(__file__).resolve().parent
path = BASE / "raw_data" / "BEA_NIPA_Section1All.xlsx"
OUT = BASE / "processed_data"
os.makedirs(OUT, exist_ok=True)

if not path.exists():
    print("BEA file not found:", path)
else:
    df = pd.read_excel(path, sheet_name="T10105-Q", skiprows=7)
    gdp_row = df[df["Line"] == 1].iloc[0]
    q_cols = [c for c in df.columns if isinstance(c, str) and c[:4].isdigit() and "Q" in c]
    series = gdp_row[q_cols]
    series.index = [c for c in q_cols]
    series_2015_2025 = series[[c for c in q_cols if 2015 <= int(c[:4]) <= 2025]]
    result = pd.DataFrame({
        "Quarter": series_2015_2025.index,
        "USA_GDP_nominal_millions": series_2015_2025.values
    })
    result.to_csv(OUT / "processed_USA_GDP_quarterly.csv", index=False, encoding="utf-8-sig")
    print(result.shape)
    print(result.head(5).to_string())
    print(result.tail(5).to_string())