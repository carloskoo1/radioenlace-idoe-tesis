from __future__ import annotations

from pathlib import Path
import pandas as pd
import numpy as np

from importlib.machinery import SourceFileLoader

common = SourceFileLoader("common", str(Path(__file__).with_name("00_common.py"))).load_module()


REQUIRED = ["dl_rssi_dbm", "dl_snr_db", "dl_mcs", "dl_rate_mbps"]


def main():
    input_file = common.DATA_PROCESSED / "01_dataset_unificado.csv"
    output_file = common.DATA_FINAL / "dataset_final_operativo.csv"

    if not input_file.exists():
        raise FileNotFoundError(f"No existe {input_file}. Ejecute primero 01_unificar_csv.py")

    df = pd.read_csv(input_file, low_memory=False)
    df = common.standardize_columns(df)

    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"Faltan columnas requeridas: {missing}. Columnas disponibles: {list(df.columns)}")

    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df = df[df["timestamp"].notna()]
        df = df.sort_values("timestamp")

    if "device_role" in df.columns:
        role = df["device_role"].astype(str).str.upper()
        df = df[role.str.contains("AP|ACCESS", regex=True, na=False) | ~role.str.contains("SM|SUB", regex=True, na=False)]

    df["dl_rssi_dbm"] = common.to_numeric(df["dl_rssi_dbm"])
    df["dl_snr_db"] = common.to_numeric(df["dl_snr_db"])
    df["dl_mcs"] = common.to_numeric(df["dl_mcs"])
    df["dl_rate_mbps"] = df["dl_rate_mbps"].apply(common.parse_rate_to_mbps)

    before_complete = len(df)
    df = df.dropna(subset=REQUIRED)
    after_complete = len(df)

    before_operational = len(df)
    df = df[
        (df["dl_rssi_dbm"] != 0) &
        (df["dl_snr_db"] != 0) &
        (df["dl_mcs"] != 0) &
        (df["dl_rate_mbps"] != 0)
    ]
    after_operational = len(df)

    before_dups = len(df)
    subset = ["timestamp"] + REQUIRED if "timestamp" in df.columns else REQUIRED
    df = df.drop_duplicates(subset=subset)
    after_dups = len(df)

    df.to_csv(output_file, index=False, encoding="utf-8-sig")

    log = {
        "registros_entrada": before_complete,
        "registros_con_variables_completas": after_complete,
        "excluidos_por_incompletos": before_complete - after_complete,
        "registros_operativos": after_operational,
        "excluidos_no_operativos": before_operational - after_operational,
        "registros_finales": after_dups,
        "duplicados_eliminados": before_dups - after_dups,
    }

    log_df = pd.DataFrame([log])
    common.save_table(log_df, "00_log_limpieza_dataset")

    print(f"[OK] Dataset final operativo: {output_file}")
    print(log_df.to_string(index=False))


if __name__ == "__main__":
    main()
