from __future__ import annotations

from pathlib import Path
import pandas as pd

from importlib.machinery import SourceFileLoader

common = SourceFileLoader("common", str(Path(__file__).with_name("00_common.py"))).load_module()


VARIABLES = {
    "RSSI downlink (dBm)": "dl_rssi_dbm",
    "SNR downlink (dB)": "dl_snr_db",
    "MCS downlink": "dl_mcs",
    "Data Rate downlink (Mbps)": "dl_rate_mbps",
}


def main():
    input_file = common.DATA_FINAL / "dataset_final_operativo.csv"
    df = pd.read_csv(input_file, low_memory=False)

    rows = []
    for label, col in VARIABLES.items():
        s = pd.to_numeric(df[col], errors="coerce").dropna()
        rows.append({
            "Variable": label,
            "N": int(s.count()),
            "Mínimo": round(s.min(), 4),
            "Máximo": round(s.max(), 4),
            "Media": round(s.mean(), 4),
            "Desv. estándar": round(s.std(), 4),
            "Mediana": round(s.median(), 4),
        })

    out = pd.DataFrame(rows)
    common.save_table(out, "01_estadisticos_descriptivos")
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
