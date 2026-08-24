# Modelo IDOE para diagnóstico operacional de radioenlace

Repositorio asociado a la investigación sobre la correspondencia entre métricas de señal radioeléctrica y desempeño de un radioenlace punto a punto en condiciones reales de operación.

El proyecto implementa un pipeline de procesamiento de datos para calcular estadísticos descriptivos, prueba de normalidad, correlaciones, el índice radioeléctrico no circular IDOE-RF y el índice operativo ampliado IDOE-OP.

## Índices implementados

- IDOE-RF: índice radioeléctrico no circular construido con RSSI, SNR y MCS.
- IDOE-OP: índice operativo ampliado construido con RSSI, SNR, MCS y tasa de datos.

## Estructura

- scripts/: scripts de procesamiento y análisis.
- data/: datasets locales no incluidos en el repositorio.
- outputs/: tablas, figuras y resultados generados.
- docs/: documentación metodológica del pipeline.

## Nota sobre datos

Los datos crudos no se incluyen por contener información operativa del radioenlace.
