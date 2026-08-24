# ============================================================
# Ejecutar pipeline completo IDOE
# ============================================================

python scripts\01_unificar_csv.py
python scripts\02_limpiar_validar_dataset.py
python scripts\03_estadisticos_descriptivos.py
python scripts\04_prueba_normalidad.py
python scripts\05_correlaciones.py
python scripts\06_calcular_indices.py
python scripts\07_idoe_rf_regresion_sensibilidad.py
python scripts\08_generar_figuras.py

Write-Host "Pipeline IDOE finalizado."
