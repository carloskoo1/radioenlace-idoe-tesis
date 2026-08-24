# Metodología del pipeline de procesamiento

El pipeline implementado procesa registros de telemetría del radioenlace ePMP obtenidos en formato CSV. El procedimiento incluye la unificación de archivos, estandarización de nombres de variables, limpieza de registros, validación de valores operativos, análisis estadístico y construcción de índices.

## Etapas

1. **Adquisición de datos:** archivos CSV obtenidos desde el sistema de monitoreo.
2. **Estandarización:** conversión de columnas originales a nombres normalizados.
3. **Limpieza:** eliminación de registros incompletos, duplicados o no operativos.
4. **Análisis descriptivo:** cálculo de mínimo, máximo, media, desviación estándar y mediana.
5. **Normalidad:** aplicación de prueba D'Agostino-Pearson.
6. **Correlación:** cálculo de Pearson y Spearman.
7. **IDOE-RF:** índice no circular basado en RSSI, SNR y MCS.
8. **IDOE-OP:** índice ampliado basado en RSSI, SNR, MCS y tasa de datos.
9. **Clasificación:** asignación de estados crítico, degradado, estable y óptimo.
10. **Sensibilidad:** evaluación de diferentes configuraciones de pesos.
