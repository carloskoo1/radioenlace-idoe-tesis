from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

from importlib.machinery import SourceFileLoader

common = SourceFileLoader("common", str(Path(__file__).with_name("00_common.py"))).load_module()


def main():
    input_file = common.DATA_FINAL / "dataset_final_operativo.csv"
    output_file = common.DATA_FINAL / "dataset_final_con_indices.csv"

    df = pd.read_csv(input_file, low_memory=False)

    df["rssi_norm"] = common.minmax(df["dl_rssi_dbm"])
    df["snr_norm"] = common.minmax(df["dl_snr_db"])
    df["mcs_norm"] = common.minmax(df["dl_mcs"])
    df["rate_norm"] = common.minmax(df["dl_rate_mbps"])

    df["IDOE_RF"] = np.cbrt(df["rssi_norm"] * df["snr_norm"] * df["mcs_norm"])

    df["IDOE_OP"] = (
        0.10 * df["rssi_norm"] +
        0.25 * df["snr_norm"] +
        0.25 * df["mcs_norm"] +
        0.40 * df["rate_norm"]
    )

    df["estado_operativo"] = df["IDOE_OP"].apply(common.classify_idoe_op)

    df.to_csv(output_file, index=False, encoding="utf-8-sig")

    desc = pd.DataFrame([{
        "Indicador": "IDOE-OP",
        "N": int(df["IDOE_OP"].count()),
        "Mínimo": round(df["IDOE_OP"].min(), 4),
        "Máximo": round(df["IDOE_OP"].max(), 4),
        "Media": round(df["IDOE_OP"].mean(), 4),
        "Desviación estándar": round(df["IDOE_OP"].std(), 4),
    }])
    common.save_table(desc, "04_descriptivos_idoe_op")

    classif = (
        df["estado_operativo"]
        .value_counts()
        .rename_axis("Estado")
        .reset_index(name="Frecuencia")
    )
    classif["Porcentaje (%)"] = (classif["Frecuencia"] / classif["Frecuencia"].sum() * 100).round(2)

    order = ["Crítico", "Degradado", "Estable", "Óptimo"]
    classif["orden"] = classif["Estado"].apply(lambda x: order.index(x) if x in order else 99)
    classif = classif.sort_values("orden").drop(columns="orden")

    common.save_table(classif, "05_clasificacion_operativa_idoe_op")

    print(f"[OK] Dataset con índices: {output_file}")
    print(desc.to_string(index=False))
    print(classif.to_string(index=False))


if __name__ == "__main__":
    main()
