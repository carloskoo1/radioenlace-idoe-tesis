from __future__ import annotations

from pathlib import Path
import re
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
DATA_FINAL = ROOT / "data" / "final"
OUT_TABLAS = ROOT / "outputs" / "tablas"
OUT_FIGURAS = ROOT / "outputs" / "figuras"
OUT_LOGS = ROOT / "outputs" / "logs"

for p in [DATA_RAW, DATA_PROCESSED, DATA_FINAL, OUT_TABLAS, OUT_FIGURAS, OUT_LOGS]:
    p.mkdir(parents=True, exist_ok=True)


COLUMN_CANDIDATES = {
    "timestamp": [
        "timestamp", "time", "datetime", "date_time", "fecha_hora",
        "radio_timestamp_local", "created_at"
    ],
    "dl_rssi_dbm": [
        "dl_rssi_dbm", "rssi_dl", "dl_rssi", "sta_dl_rssi",
        "radio_rssi_dl", "radio_rssi", "rssi"
    ],
    "dl_snr_db": [
        "dl_snr_db", "snr_dl", "dl_snr", "radio_snr_dl",
        "radio_snr", "snr"
    ],
    "dl_mcs": [
        "dl_mcs", "mcs_dl", "radio_mcs_dl", "radio_mcs", "mcs"
    ],
    "dl_rate_mbps": [
        "dl_rate_mbps", "data_rate", "datarate", "data_rate_dl",
        "dl_data_rate", "radio_data_rate_dl", "radio_data_rate",
        "rate", "throughput", "throughput_dl"
    ],
    "device_role": [
        "device_role", "role", "tipo_equipo", "radio_role", "device_type"
    ],
}


def normalize_colname(name: str) -> str:
    name = str(name).strip().lower()
    name = name.replace(" ", "_").replace("-", "_")
    name = re.sub(r"[^a-z0-9_]+", "", name)
    return name


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    original_cols = list(df.columns)
    normalized_map = {col: normalize_colname(col) for col in original_cols}
    df = df.rename(columns=normalized_map)

    rename = {}
    cols = set(df.columns)

    for standard, candidates in COLUMN_CANDIDATES.items():
        for candidate in candidates:
            candidate = normalize_colname(candidate)
            if candidate in cols:
                rename[candidate] = standard
                break

    df = df.rename(columns=rename)
    return df


def parse_rate_to_mbps(value):
    if pd.isna(value):
        return np.nan

    if isinstance(value, (int, float, np.integer, np.floating)):
        return float(value)

    text = str(value).strip().upper()
    text = text.replace("MBPS", "M").replace("MB/S", "M")
    text = text.replace(" ", "")

    match = re.search(r"[-+]?\d*\.?\d+", text)
    if not match:
        return np.nan

    number = float(match.group(0))

    if "G" in text:
        return number * 1000.0
    if "K" in text:
        return number / 1000.0
    return number


def to_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(
        series.astype(str)
        .str.replace("dBm", "", case=False, regex=False)
        .str.replace("dB", "", case=False, regex=False)
        .str.replace("M", "", case=False, regex=False)
        .str.strip(),
        errors="coerce"
    )


def minmax(series: pd.Series) -> pd.Series:
    s = series.astype(float)
    s_min = s.min()
    s_max = s.max()
    if pd.isna(s_min) or pd.isna(s_max) or s_max == s_min:
        return pd.Series(np.zeros(len(s)), index=s.index)
    return (s - s_min) / (s_max - s_min)


def classify_idoe_op(x: float) -> str:
    if pd.isna(x):
        return np.nan
    if x >= 0.80:
        return "Óptimo"
    if x >= 0.60:
        return "Estable"
    if x >= 0.40:
        return "Degradado"
    return "Crítico"


def save_table(df: pd.DataFrame, name: str) -> None:
    csv_path = OUT_TABLAS / f"{name}.csv"
    xlsx_path = OUT_TABLAS / f"{name}.xlsx"
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    df.to_excel(xlsx_path, index=False)
    print(f"[OK] Tabla generada: {csv_path}")
    print(f"[OK] Tabla generada: {xlsx_path}")
