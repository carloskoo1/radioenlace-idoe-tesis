from __future__ import annotations

from pathlib import Path
import pandas as pd
from scipy import stats

from importlib.machinery import SourceFileLoader

common = SourceFileLoader("common", str(Path(__file__).with_name("00_common.py"))).load_module()


PAIRS = [
    ("RSSI - Data Rate", "dl_rssi_dbm", "dl_rate_mbps", "Positiva muy baja"),
    ("SNR - Data Rate", "dl_snr_db", "dl_rate_mbps", "Positiva baja"),
    ("MCS - Data Rate", "dl_mcs", "dl_rate_mbps", "Positiva alta monotónica"),
]


def fmt_p(p):
    return "< 0.001" if p < 0.001 else round(float(p), 6)


def main():
    input_file = common.DATA_FINAL / "dataset_final_operativo.csv"
    df = pd.read_csv(input_file, low_memory=False)

    rows = []
    for label, xcol, ycol, interpretation in PAIRS:
        sub = df[[xcol, ycol]].dropna()
        pearson_r, pearson_p = stats.pearsonr(sub[xcol], sub[ycol])
        spearman_r, spearman_p = stats.spearmanr(sub[xcol], sub[ycol])

        rows.append({
            "Relación": label,
            "Pearson r": round(float(pearson_r), 4),
            "p-valor Pearson": fmt_p(pearson_p),
            "Spearman rho": round(float(spearman_r), 4),
            "p-valor Spearman": fmt_p(spearman_p),
            "Interpretación": interpretation,
        })

    out = pd.DataFrame(rows)
    common.save_table(out, "03_correlaciones_metricas_vs_rate")
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
