from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

from importlib.machinery import SourceFileLoader

common = SourceFileLoader("common", str(Path(__file__).with_name("00_common.py"))).load_module()


def fmt_p(p):
    return "< 0.001" if p < 0.001 else round(float(p), 6)


def regression_metrics(x, y):
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    return slope, intercept, r_value ** 2, p_value


def corr_row(label, x, y):
    pearson_r, pearson_p = stats.pearsonr(x, y)
    spearman_r, spearman_p = stats.spearmanr(x, y)
    slope, intercept, r2, p_reg = regression_metrics(x, y)

    return {
        "Relación": label,
        "Pearson r": round(float(pearson_r), 4),
        "p-valor Pearson": fmt_p(pearson_p),
        "Spearman rho": round(float(spearman_r), 4),
        "p-valor Spearman": fmt_p(spearman_p),
        "R2 lineal": round(float(r2), 4),
        "Pendiente": round(float(slope), 4),
        "Intercepto": round(float(intercept), 4),
    }


def build_weighted_index(df, weights):
    return (
        weights["rssi"] * df["rssi_norm"] +
        weights["snr"] * df["snr_norm"] +
        weights["mcs"] * df["mcs_norm"] +
        weights["rate"] * df["rate_norm"]
    )


def main():
    input_file = common.DATA_FINAL / "dataset_final_con_indices.csv"
    df = pd.read_csv(input_file, low_memory=False)

    rows = [
        corr_row("IDOE-RF - Data Rate", df["IDOE_RF"], df["dl_rate_mbps"]),
        corr_row("IDOE-OP - Data Rate", df["IDOE_OP"], df["dl_rate_mbps"]),
    ]
    common.save_table(pd.DataFrame(rows), "06_correlacion_indices_vs_rate")

    scenarios = {
        "Original": {"rssi": 0.10, "snr": 0.25, "mcs": 0.25, "rate": 0.40},
        "SNR dominante": {"rssi": 0.10, "snr": 0.55, "mcs": 0.20, "rate": 0.15},
        "Rate dominante": {"rssi": 0.05, "snr": 0.10, "mcs": 0.10, "rate": 0.75},
        "Equilibrado": {"rssi": 0.25, "snr": 0.25, "mcs": 0.25, "rate": 0.25},
        "RSSI dominante": {"rssi": 0.55, "snr": 0.15, "mcs": 0.15, "rate": 0.15},
        "MCS dominante": {"rssi": 0.10, "snr": 0.15, "mcs": 0.60, "rate": 0.15},
    }

    sens_rows = []
    for name, weights in scenarios.items():
        idx = build_weighted_index(df, weights)
        pearson_r, _ = stats.pearsonr(idx, df["dl_rate_mbps"])
        spearman_r, _ = stats.spearmanr(idx, df["dl_rate_mbps"])
        _, _, r2, _ = regression_metrics(idx, df["dl_rate_mbps"])

        sens_rows.append({
            "Escenario": name,
            "Pearson r": round(float(pearson_r), 4),
            "Spearman rho": round(float(spearman_r), 4),
            "R2": round(float(r2), 4),
        })

    common.save_table(pd.DataFrame(sens_rows), "07_sensibilidad_pesos_idoe_op")

    print("[OK] Análisis de índices, regresión y sensibilidad finalizado.")


if __name__ == "__main__":
    main()
