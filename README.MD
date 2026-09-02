Hallazgos Pre-Analisis del dataset.

Hoja Ordenes:
- Diferentes formatos de fecha en fechas inicio y fin.
- fechas de fin en blanco con estado completado y otras en proceso.
- Completado escrito en mayusculas, otras en minusculas, otro solo la inicial en mayusculas, misma situacion con En proceso.
- Estados distintos, no normalizados, hay estados OK, En progreso, pend. completo.
- 516 filas, 13 columnas.
- Columna horas fuera servicio con datos en blanco.
- fila 59 tiene fecha final pero estado pendiente, sin datos en costo mano de obra.
- 40 equipos, 500 OT, 15 tecnicos.

Hoja Equipos:
- Anio-fabricacion.
- 40 equipos, 6 tipos de equipos, 8 marcas, 12 modelos.
- Distintos tipos de equipos con el mismo modelo.
- 41 filas, 8 columnas.

Resumen:
- 516 filas en ordenes, por lo que 515 son de datos, sin embargo se detectan 500 OT's, esto significa ot's duplicadas.
- Tras investigacion de negocio se descubre que Caterpillar fabrica camiones, motoniveladoras y carg. frontales con sus propios tipos de modelos.
- Fila 59 con fecha_fin pero estado Pendiente, corresponde a inconsistencia con decision de negocio: Tecnico cerro fecha antes de actualizar estado o el sistema permitio guardar un estado inconsistente.
- Columnas con costos en blanco, nulos en costo_mano_obra.
- Las fechas con datos en blanco debieran quedar como NaT, no todas son un error. si se eliminaran las filas quedarian Ot's sin analizar, al llegar al punto de visualizarlo en el dashboard se podria analizar cada caso por separado con un apartado de "Inconsistencias".
- Nulos 'horas_fuera_servicio', se mantendrán los datos en blanco (NaT) ya que pandas ignora usando skipna=True. Si se dejara en 0 puede bajar artificialmente el promedio de horas, dejarlo como Sin_Registro arruinaria calculos con pandas al procesar los datos como texto.

<!-- Nota PostgreSQL: Conexión asume autenticación local de PostgreSQL. -->
Consultas SQL:

-- ¿Cuál es el costo total de mantenimiento por tipo?
-- ¿Qué equipo acumuló más horas fuera de servicio?
-- Promedio de horas fuera de servicio por tipo de mantenimiento
-- ¿Qué área de faena genera más OTs correctivas?
-- ¿Qué técnico tiene más OTs de emergencia?
-- Top 5 sistemas con mayor costo acumulado de reparación
