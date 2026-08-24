from __future__ import annotations

from pathlib import Path
import pandas as pd
from scipy import stats

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

        stat, p_value = stats.normaltest(s)

        rows.append({
            "Variable": label,
            "Prueba aplicada": "D'Agostino-Pearson",
            "Estadístico": round(float(stat), 4),
            "p-valor": "< 0.001" if p_value < 0.001 else round(float(p_value), 6),
            "Decisión": "No normal" if p_value < 0.05 else "Normal",
        })

    out = pd.DataFrame(rows)
    common.save_table(out, "02_prueba_normalidad")
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
