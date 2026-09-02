
-- CONSULTAS SQL — FLOTA MINERA
-- Base de datos: flota_minera

-- ¿Cuál es el costo total de mantenimiento por tipo?
SELECT
	tipo_mantenimiento,
	COUNT(ot_id) AS total_ots,
	SUM(costo_total) AS costo_total_clp
FROM
	ordenes_trabajo
GROUP BY
	tipo_mantenimiento;

-- tipo_mant   total_ots    costo_total_clp
-- Correctivo	    229	        383143000
-- Emergencia	    95	        147851000
-- Predictivo	    91	        40421000
-- Preventivo	    85	        39120000

-- ¿Qué equipo acumuló más horas fuera de servicio?
-- Horas_fuera_servicio tiene NaN
-- PostgreSQL ignora NULL en SUM por defecto
SELECT
	eq.equipo_id,
	eq.tipo,
	eq.marca,
	SUM(ot.horas_fuera_servicio) AS total_horas_detenido
FROM
	ordenes_trabajo AS ot
	INNER JOIN equipos AS eq ON ot.equipo_id = eq.equipo_id
GROUP BY
	eq.equipo_id, eq.tipo, eq.marca
ORDER BY
	total_horas_detenido DESC
LIMIT 1;

-- EQ-030	Perforadora	Sandvik	560

-- Promedio de horas fuera de servicio por tipo de mantenimiento
SELECT
	tipo_mantenimiento,
	COUNT(ot_id) AS total_ots,
	ROUND(AVG(horas_fuera_servicio)::numeric, 0) AS promedio_horas
FROM
	ordenes_trabajo
GROUP BY
	tipo_mantenimiento;

-- tipo_mant   total_ots  promedio_horas
-- Correctivo	229        26
-- Emergencia	95	       43
-- Predictivo	91	        3
-- Preventivo	85	        6

-- ¿Qué área de faena genera más OTs correctivas?
SELECT
	eq.area_asignada,
	ot.tipo_mantenimiento,
	COUNT(ot.ot_id) AS total_ots
FROM
	ordenes_trabajo AS ot
	INNER JOIN equipos AS eq ON ot.equipo_id = eq.equipo_id
WHERE
	ot.tipo_mantenimiento =	'Correctivo'
GROUP BY
	ot.tipo_mantenimiento, eq.area_asignada
ORDER BY
	total_ots DESC
LIMIT 1;

-- area_asignada   tipo_mant   total_ots
-- Rajo Sur	    Correctivo	    66

-- ¿Qué técnico tiene más OTs de emergencia?
-- Columnas esperadas: tecnico_responsable, total_emergencias
SELECT
	tecnico_responsable,
	COUNT(ot_id) AS total_ots_emergencia
FROM
	ordenes_trabajo
WHERE
	tipo_mantenimiento ='Emergencia'
GROUP BY
	tecnico_responsable, tipo_mantenimiento
ORDER BY total_ots_emergencia DESC
LIMIT 1;
-- tec_responsable total_ots_emergencia
-- TEC-14	        12

-- Top 5 sistemas con mayor costo acumulado de reparación
-- Solo contar OTs con estado = 'Completado'
SELECT
	sistema_intervenido,
	SUM(costo_total) as costo_acumulado
FROM
	ordenes_trabajo
WHERE
	estado = 'Completado'
GROUP BY
	sistema_intervenido
ORDER BY costo_acumulado DESC
LIMIT 5;
-- sist_intervenido    costo_acumulado
-- Enfriamiento	58343000
-- Frenos	48005000
-- Sistema Eléctrico	47326000
-- Transmisión	44771000
-- Suspensión	34662000