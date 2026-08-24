# Diccionario de variables

## Variables principales

| Variable estándar | Descripción | Unidad / escala |
|---|---|---|
| timestamp | Marca temporal del registro | Fecha-hora |
| dl_rssi_dbm | RSSI downlink | dBm |
| dl_snr_db | SNR downlink | dB |
| dl_mcs | MCS downlink | Índice discreto |
| dl_rate_mbps | Tasa de datos downlink | Mbps |

## Índices derivados

| Índice | Descripción |
|---|---|
| IDOE-RF | Índice radioeléctrico no circular construido con RSSI, SNR y MCS normalizados. |
| IDOE-OP | Índice operativo ampliado construido con RSSI, SNR, MCS y tasa de datos. |

## Categorías operativas IDOE-OP

| Rango | Estado |
|---|---|
| IDOE-OP >= 0.80 | Óptimo |
| 0.60 <= IDOE-OP < 0.80 | Estable |
| 0.40 <= IDOE-OP < 0.60 | Degradado |
| IDOE-OP < 0.40 | Crítico |
