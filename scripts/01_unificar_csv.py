from __future__ import annotations

import sys
from pathlib import Path
import pandas as pd

from importlib.machinery import SourceFileLoader

common = SourceFileLoader("common", str(Path(__file__).with_name("00_common.py"))).load_module()


def main():
    input_dir = common.DATA_RAW
    output_file = common.DATA_PROCESSED / "01_dataset_unificado.csv"

    files = sorted(input_dir.glob("*.csv"))

    if not files:
        print(f"[ERROR] No se encontraron archivos CSV en: {input_dir}")
        print("[INFO] Copie los CSV crudos en data/raw/ y vuelva a ejecutar.")
        sys.exit(1)

    frames = []
    for file in files:
        try:
            df = pd.read_csv(file, encoding="utf-8", low_memory=False)
        except UnicodeDecodeError:
            df = pd.read_csv(file, encoding="latin1", low_memory=False)

        df = common.standardize_columns(df)
        df["source_file"] = file.name
        frames.append(df)
        print(f"[OK] Leído: {file.name} -> {len(df)} registros")

    out = pd.concat(frames, ignore_index=True)
    out.to_csv(output_file, index=False, encoding="utf-8-sig")

    print(f"[OK] Dataset unificado generado: {output_file}")
    print(f"[OK] Registros totales: {len(out)}")


if __name__ == "__main__":
    main()
