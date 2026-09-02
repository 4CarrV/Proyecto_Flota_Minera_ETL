# Análisis de Mantenciones de Flota Minera (2023 - 2024)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Cleaning-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Google BigQuery](https://img.shields.io/badge/SQL-BigQuery-4285F4?logo=googlecloud&logoColor=white)](https://cloud.google.com/bigquery)
[![Looker Studio](https://img.shields.io/badge/BI-Looker%20Studio-F4B400?logo=google&logoColor=white)](https://lookerstudio.google.com/)

---

## Descripción General
Proyecto end-to-end de análisis de datos enfocado en la disponibilidad, confiabilidad y costos operacionales de una flota minera (40 equipos) entre 2023 y 2024. 

El proyecto abarca desde la ingesta y auditoría de calidad de datos crudos (`raw.xlsx`), un pipeline **ETL en Python (Pandas)** para limpieza y normalización, modelado y consultas analíticas en **SQL**, hasta la visualización ejecutiva en un **Dashboard interactivo en Looker Studio**.
## NOTA IMPORTANTE: SE ANONIMIZO EL DATASET ORIGINAL POR MOTIVOS DE PRIVACIDAD DEL CLIENTE DE IGUAL MANERA SE MODIFICARON FECHAS.
---

## Dashboard Ejecutivo (Looker Studio)

![Dashboard Looker Studio](imgs_proyecto/InformeLookerStudio.png)

### KPIs y Métricas Principales del Periodo:
* **Gasto Total en Mantenciones:** $610.535.000 CLP
* **Horas Fuera de Servicio Totales:** 10.176 hrs
* **Promedio de Detención por OT:** 21,47 hrs
* **Tasa de Mantención Reactiva (Correctivo + Emergencia):** 64,8%
* **Órdenes de Trabajo Validadas:** 500 OTs

---

## Stack Tecnológico
* **Lenguaje:** Python
* **Procesamiento y ETL:** Pandas, NumPy, OpenPyXL
* **Almacenamiento y Consultas:** Google BigQuery / SQL (DWH)
* **Visualización & BI:** Looker Studio
* **Control de Versiones:** Git & GitHub

---

## Preguntas de Negocio y Consultas SQL (SQL/consultas.sql)

El repositorio incluye consultas SQL estructuradas para responder interrogantes críticas de confiabilidad operacional:
* **Impacto Financiero por Tipo de Mantención:
Evaluación del gasto acumulado entre mantenimientos Correctivo, Emergencia, Predictivo y Preventivo (evidenciando que el 62,76% del presupuesto se concentró en fallas correctivas).
* **Equipos Críticos con Mayor Indisponibilidad:
Identificación del Top 5 de equipos con mayor impacto en detención (liderado por el equipo EQ-030 - Sandvik con 560 hrs).
* **Distribución Geográfica / Áreas de Faena:
Cuantificación de horas fuera de servicio por sector (Rajo Sur, Chancado, Botadero Norte, Taller Central, Rajo Norte).
* **Sistemas Mecánicos/Eléctricos más Costosos:
Ranking de criticidad por sistema (con Sistema Eléctrico, Frenos y Enfriamiento acumulando las mayores sumas de reparación).
* **Rendimiento y Carga de Trabajo de Técnicos:
Conteo de OTs de emergencia atendidas por cada especialista para balance de turnos.

---

## Hallazgos y Conclusiones del Negocio
* Elevada Reactividad Operacional: El 86,98% de los costos totales provienen de intervenciones reactivas (Correctivo: $383.143.000 CLP + Emergencia: $147.851.000 CLP), mientras que el mantenimiento preventivo y predictivo representan menos del 14% del gasto global.
* Cuello de Botella en Rajo Sur: Es el área operativa con mayor impacto en disponibilidad, acumulando 2.899 horas fuera de servicio.
* Priorización de Repuestos: El Sistema Eléctrico ($81,2M CLP) y el Sistema de Frenos ($76,25M CLP) concentran el mayor costo de recambio/mano de obra, marcando dónde deben orientarse los planes de monitoreo de condición e inventario crítico en bodega.

## Estructura del Repositorio

```text
Caso_02_Flota_Minera/
├── data/
│   ├── duplicados_ots.csv       # Registro histórico de OTs duplicadas extraídas
│   └── raw.xlsx                 # Dataset crudo con hojas 'Ordenes' y 'Equipos'
├── imgs_proyecto/
│   └── InformeLookerStudio.png  # Captura visual del reporte de BI
├── SQL/
│   └── consultas.sql            # Queries analíticas y agregaciones clave
├── src/
│   └── etl_flota.py             # Script de extracción, transformación y carga
└── README.md                    # Documentación del proyecto
