import pandas as pd
from pathlib import Path

# Seleccionamos la carpeta donde está el script (src/)
# .resolve() equivale a os.path.abspath y .parent sube un nivel de carpeta
base_dir = Path(__file__).resolve().parent.parent
# Generamos la ruta apuntando a la carpeta data
# El operador '/' reemplaza de forma segura a os.path.join
ruta = base_dir / "data" / "raw.xlsx"

# ETL
# 1. CARGA
equipos = pd.read_excel(ruta, sheet_name="Equipos")
ots     = pd.read_excel(ruta, sheet_name="Ordenes_Trabajo")
reps    = pd.read_excel(ruta, sheet_name="Repuestos")

# 2. DIAGNÓSTICO INICIAL
# for nombre, df in [("Equipos", equipos), ("Ordenes_Trabajo", ots), ("Repuestos", reps)]:
#     print(f"\n{'='*50}")
#     print(f"  {nombre}")
#     print(f"{'='*50}")
#     print(f"Shape          : {df.shape}")
#     print(f"Duplicados     : {df.duplicated().sum()}")
#     print(f"\nNulos por columna:")
#     print(df.isnull().sum())
#     print(f"\nTipos de datos:")
#     print(df.dtypes)

# 3. LIMPIEZA
# 3.1 Guardar duplicados antes de eliminar
# Definimos la ruta de salida usando el objeto base_dir
ruta_duplicados = base_dir / "data" / "duplicados_ots.csv"
# Extraemos la copia de las filas duplicadas
duplicados = ots[ots.duplicated(keep='first')].copy()
# Exportamos usando el objeto Path directo
duplicados.to_csv(ruta_duplicados, index=False)
# Eliminar duplicados de ots dejando el primero y reiniciando los indices
ots_limpio = ots.drop_duplicates(keep='first').reset_index(drop=True)

# 3.2 Normalizar columna 'estado'
# Revisamos las variantes existentes para crear el diccionario en base a las presentes
print(ots_limpio['estado'].unique())
# Resultado:
# [  'Pendiente',  'Completado',  'En Proceso',   'Cancelado',   'pendiente',
#        'Pend.',    'Completo',  'COMPLETADO',  'completado',  'EN PROCESO',
#    'cancelado',   'CANCELADO',          'OK',  'En proceso', 'En progreso',
#    'PENDIENTE']
# Con las variantes creamos el diccionario de mapeo
mapeo_estados = {
    'pendiente':'Pendiente',
    'Pend.':'Pendiente',
    'PENDIENTE': 'Pendiente',
    'Completo': 'Completado',
    'COMPLETADO': 'Completado',
    'completado': 'Completado',
    'cancelado': 'Cancelado',
    'CANCELADO': 'Cancelado',
    'OK': 'Completado',
    'EN PROCESO': 'En Proceso',
    'En proceso': 'En Proceso',
    'En Progreso': 'En Proceso',
    'En progreso': 'En Proceso'
}
# Aplicamos un replace para reemplazar errores por valores normalizados
ots_limpio['estado'] = ots_limpio['estado'].replace(mapeo_estados)
# Incluimos los NaN que no son detectados por el unique para reemplazarlos con Sin Registro
ots_limpio['estado'] = ots_limpio['estado'].fillna('Sin Registro')
# Comprobamos limpieza
print(ots_limpio['estado'].unique())
# Resultados:
# ['Pendiente', 'Completado', 'En Proceso', 'Cancelado'] Length: 4, dtype: str

# 3.3 Parsear fechas
# Convertir fecha_inicio y fecha_fin a datetime con los parámetros previamente decididos
# Limpieza de fecha_inicio
ots_limpio['fecha_inicio'] = pd.to_datetime(
    ots_limpio['fecha_inicio'],
    dayfirst=True,
    errors='coerce',
    format='mixed'
    )
# Limpieza de fecha_fin
ots_limpio['fecha_fin'] = pd.to_datetime(
    ots_limpio['fecha_fin'],
    dayfirst=True,
    errors='coerce',
    format='mixed'
    )

# 3.4 Manejar nulos según las decisiones previas
# Verificamos cuantas filas quedaron en NaT - Nulas
total_nat0 = ots_limpio['fecha_inicio'].isna().sum()
print(f"Cantidad de fechas NA en inicio (NaT): {total_nat0}")
total_nat1 = ots_limpio['fecha_fin'].isna().sum()
print(f"Cantidad de fechas NA en fin (NaT): {total_nat1}")
total_nat2 = ots_limpio['horas_fuera_servicio'].isna().sum()
print(f"Cantidad de filas NA en Horas Fuera Servicio (NaT): {total_nat2}")
total_nat3 = ots_limpio['costo_mano_obra'].isna().sum()
print(f"Cantidad de filas NA en Costo Mano Obra (NaT): {total_nat3}")
# Resultados:
# Cantidad de fechas fallidas en inicio (NaT): 0
# Cantidad de fechas fallidas en fin (NaT): 20
# Cantidad de filas fallidas en fin Fuera Servicio (NaT): 26
# Cantidad de filas NA en Costo Mano Obra (NaT): 12
# Siguiendo nuestras decisiones pre-analisis horas_fuera_servicio las dejamos NaN y el costo_mano_obra lo rellenamos con 0
ots_limpio['costo_mano_obra'] = ots_limpio['costo_mano_obra'].fillna(0)

# 3.5 Crear columna costo_total
# Creamos columna costo_total realizando el calculo de costo_mano_obra + costo_repuestos
ots_limpio['costo_total'] = ots_limpio['costo_mano_obra'] + ots_limpio['costo_repuestos']

# 4. VALIDACIÓN POST-LIMPIEZA
# Finamente realizamos validacion final Post-Limpieza
# Verificamos nuevo shape del DataFrame
print(" REPORTE DE VALIDACIÓN DEL DATAFRAME ")
print(f"Shape: {ots_limpio.shape[0]} filas y {ots_limpio.shape[1]} columnas.\n")
# Verificamos datos duplicados
print(" VERIFICACIÓN DE DUPLICADOS ")
suma_duplicados = ots_limpio.duplicated().sum()
print(f"Cantidad de filas duplicadas en el DataFrame: {suma_duplicados}\n")
# Verificamos valores nulos para cada columna
print(" DETALLE DE VALORES NULOS POR COLUMNA ")
nulos_por_columna = ots_limpio.isna().sum()
print(nulos_por_columna[nulos_por_columna > 0])

# 5. CARGA A POSTGRESQL
from sqlalchemy import create_engine

engine = create_engine("postgresql://localhost/flota_minera")

# Cargamos la tabla de equipos a SQL
equipos.to_sql(
    name='equipos',              # Nombre que tendrá la tabla en PostgreSQL
    con=engine,                  # Conexion con sqlalchemy
    if_exists='replace',         # Qué hacer si la tabla ya existe ('fail', 'replace' o 'append')
    index=False,                 # Evita que el índice de pandas se guarde como una columna
)
# Cargamos la tabla de repuestos a SQL
reps.to_sql(
    name='repuestos',
    con=engine,
    if_exists='replace',
    index=False,
)
# Cargamos la tabla de OT's a SQL
ots_limpio.to_sql(
    name='ordenes_trabajo',
    con=engine,
    if_exists='replace',
    index=False,
)

print("Datos cargados en PostgreSQL")

# 6.CARGA A BIGQUERY
import pandas_gbq
from google.oauth2 import service_account

# Credenciales y configuración
PROJECT_ID   = "flota-minera"
DATASET      = "flota_minera"
RUTA_CREDS   = base_dir / "data" / "credenciales_gcp.json"

credentials = service_account.Credentials.from_service_account_file(
    RUTA_CREDS,
    scopes=["https://www.googleapis.com/auth/bigquery"]
)

# Función auxiliar para no repetir parámetros
def cargar_bigquery(df, nombre_tabla):
    pandas_gbq.to_gbq(
        df,
        destination_table=f"{DATASET}.{nombre_tabla}",
        project_id=PROJECT_ID,
        credentials=credentials,
        if_exists="replace",
        progress_bar=False
    )
    print(f"  → {nombre_tabla} cargada en BigQuery ({len(df)} filas)")

print("\nCargando tablas en BigQuery...")
cargar_bigquery(equipos,    "equipos")
cargar_bigquery(reps,       "repuestos")
cargar_bigquery(ots_limpio, "ordenes_trabajo")
print("Carga BigQuery completada.")