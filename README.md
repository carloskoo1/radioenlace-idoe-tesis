# Modelo IDOE para diagnóstico operacional de radioenlace

Repositorio asociado a la investigación sobre la correspondencia entre métricas de señal radioeléctrica y desempeño de un radioenlace punto a punto en condiciones reales de operación.

El proyecto implementa un pipeline de procesamiento de datos para calcular estadísticos descriptivos, prueba de normalidad, correlaciones, el índice radioeléctrico no circular IDOE-RF y el índice operativo ampliado IDOE-OP.

## Índices implementados

- **IDOE-RF**: índice radioeléctrico no circular construido con RSSI, SNR y MCS normalizados.
- **IDOE-OP**: índice operativo ampliado construido con RSSI, SNR, MCS y tasa de datos.

## Estructura del repositorio

- scripts/: scripts de procesamiento y análisis.
- data/raw/: ubicación local de archivos CSV crudos. No se suben al repositorio.
- data/processed/: archivos procesados intermedios. No se suben al repositorio.
- data/final/: dataset final operativo. No se sube al repositorio.
- outputs/tablas/: tablas generadas por el análisis.
- outputs/figuras/: figuras generadas por el análisis.
- outputs/logs/: registros de ejecución.
- docs/: documentación metodológica del pipeline.

## Flujo general

1. Unificación de CSV.
2. Limpieza y validación del dataset.
3. Estadísticos descriptivos.
4. Prueba de normalidad.
5. Correlaciones Pearson y Spearman.
6. Cálculo del IDOE-RF.
7. Cálculo del IDOE-OP y clasificación operativa.
8. Análisis de sensibilidad de pesos.
9. Regresión lineal.
10. Generación de figuras.

## Nota sobre datos

Los datos crudos no se incluyen en el repositorio por contener información operativa del radioenlace. Para reproducibilidad, puede utilizarse una muestra anonimizada.
