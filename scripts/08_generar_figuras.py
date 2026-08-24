from __future__ import annotations

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from importlib.machinery import SourceFileLoader

common = SourceFileLoader("common", str(Path(__file__).with_name("00_common.py"))).load_module()


def savefig(name):
    path = common.OUT_FIGURAS / name
    plt.tight_layout()
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[OK] Figura generada: {path}")


def main():
    input_file = common.DATA_FINAL / "dataset_final_con_indices.csv"
    df = pd.read_csv(input_file, low_memory=False)

    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df_time = df.dropna(subset=["timestamp"]).copy()
        df_time = df_time.set_index("timestamp").sort_index()

        med = df_time[["dl_rssi_dbm", "dl_snr_db", "dl_mcs", "dl_rate_mbps"]].resample("6h").median()

        for col, label in [
            ("dl_rssi_dbm", "RSSI downlink (dBm)"),
            ("dl_snr_db", "SNR downlink (dB)"),
            ("dl_mcs", "MCS downlink"),
            ("dl_rate_mbps", "Data Rate downlink (Mbps)"),
        ]:
            plt.figure(figsize=(10, 4))
            plt.plot(med.index, med[col])
            plt.title(f"Comportamiento temporal de {label}")
            plt.xlabel("Tiempo")
            plt.ylabel(label)
            savefig(f"temporal_{col}.png")

    for col, label in [
        ("dl_rssi_dbm", "RSSI downlink (dBm)"),
        ("dl_snr_db", "SNR downlink (dB)"),
        ("dl_mcs", "MCS downlink"),
        ("dl_rate_mbps", "Data Rate downlink (Mbps)"),
        ("IDOE_OP", "IDOE-OP"),
    ]:
        plt.figure(figsize=(7, 4))
        plt.hist(df[col].dropna(), bins=40)
        plt.title(f"Distribución de {label}")
        plt.xlabel(label)
        plt.ylabel("Frecuencia")
        savefig(f"hist_{col}.png")

    for col, label in [
        ("dl_rssi_dbm", "RSSI"),
        ("dl_snr_db", "SNR"),
        ("dl_mcs", "MCS"),
        ("IDOE_RF", "IDOE-RF"),
        ("IDOE_OP", "IDOE-OP"),
    ]:
        plt.figure(figsize=(7, 4))
        plt.scatter(df[col], df["dl_rate_mbps"], s=4, alpha=0.25)
        plt.title(f"{label} vs Data Rate")
        plt.xlabel(label)
        plt.ylabel("Data Rate (Mbps)")
        savefig(f"scatter_{col}_vs_rate.png")

    corr_cols = ["dl_rssi_dbm", "dl_snr_db", "dl_mcs", "dl_rate_mbps", "IDOE_RF", "IDOE_OP"]
    corr = df[corr_cols].corr(method="spearman")

    plt.figure(figsize=(8, 6))
    plt.imshow(corr, aspect="auto")
    plt.colorbar(label="Spearman rho")
    plt.xticks(range(len(corr_cols)), corr_cols, rotation=45, ha="right")
    plt.yticks(range(len(corr_cols)), corr_cols)
    plt.title("Matriz de correlación de Spearman")

    for i in range(len(corr_cols)):
        for j in range(len(corr_cols)):
            plt.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center")

    savefig("matriz_spearman.png")

    classif = df["estado_operativo"].value_counts()
    plt.figure(figsize=(7, 4))
    classif.plot(kind="bar")
    plt.title("Clasificación operativa mediante IDOE-OP")
    plt.xlabel("Estado operativo")
    plt.ylabel("Frecuencia")
    savefig("clasificacion_operativa_idoe_op.png")

    print("[OK] Generación de figuras finalizada.")


if __name__ == "__main__":
    main()
