# Changelog

## [F4] - Semana 3 Junio 2026
### Added
- Patrón de diseño Strategy para imputación de nulos (EstrategiaImputacion, ImputarMediana, ImputarMedia)
- Batería de pruebas técnicas: 9 casos (normal, límite, excepción) con aserciones explícitas
- Benchmark merge_sort vs sorted() con análisis de complejidad y conteo de llamadas recursivas
- Benchmark vectorizado extendido a ambos datasets (Matemáticas y Portugués)
- 5 visualizaciones analíticas que responden a las preguntas de investigación de F1
- Trazabilidad completa del pipeline en tabla comparativa F1-F4

## [F3] - Semana 3 Junio 2026
### Added
- Clase PreprocesadorAsignatura (src/clases.py): encapsula el pipeline F2 en objetos
- Clases hijas PreprocesadorMatematicas y PreprocesadorPortugues: herencia + polimorfismo
- Método interpretar_resultados() como contrato de implementación (NotImplementedError en base)
- Algoritmo recursivo merge_sort aplicado a notas G3
- Comparativa de eficiencia bucle vs. vectorizado con timeit
- Método __repr__ para inspección del estado del objeto

## [F2] - Semana 2 Junio 2026
### Added
- Pipeline funcional completo en src/functions.py (12 funciones encapsuladas)
- Winsorización p95 para variable absences
- Flag 'desercion' (G2=0 y G3=0) para análisis diferenciado
- Codificación binaria (yes/no → 1/0) y One-Hot Encoding (Mjob, Fjob, reason, guardian)
- Variables derivadas: aprobado, progreso_g1_g3, nivel_alcohol, edu_familiar_media
- Función validar_dataset_final() con 7 asserts de integridad

## [F1] - Semana 1 Junio 2026
### Added
- Configuración del entorno reproducible (.venv, requirements.txt, README.md)
- Repositorio GitHub con estructura modular (data/, notebooks/, src/)
- Carga inicial y exploración preliminar del Student Performance Dataset
- Definición formal del problema, preguntas de investigación y objetivos
