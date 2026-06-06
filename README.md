# Proyecto Grupo 7 — MCDI500
## Factores socioeconómicos y de preparación previa asociados al rendimiento académico

---

## Descripción

Este repositorio contiene el proyecto transversal del curso **MCDI500 — Herramientas de Software Científico** del Magíster en Ciencias de Datos e Inteligencia Artificial (UNAB).

El proyecto analiza el **Student Performance Dataset** (Cortez & Silva, 2008) para identificar qué factores socioeconómicos y de preparación previa explican las diferencias en el rendimiento académico entre estudiantes de dos establecimientos educacionales portugueses.

---

## Integrantes — Grupo 7

| Nombre | Rol |
|---|---|
| Juan de Dios Díaz Ríos | Integrante |
| Francisco Fariña Molina | Integrante |
| Constanza Moreno Giacometto | Integrante |
| Yenne Sepúlveda Jerez | Integrante |

**Docente:** Omar Salinas Silva

---

## Estructura del repositorio
proyecto-grupo7-mcdi500/
├── data/
│   ├── raw/                        # Datos originales sin modificar
│   │   ├── student-mat.csv
│   │   └── student-por.csv
│   └── processed/                  # Datos procesados (se genera en F2)
├── notebooks/
│   └── F1_Definicion.ipynb         # Fase 1: Definición del problema
├── src/                            # Funciones reutilizables
├── docs/                           # Documentación e informes
├── requirements.txt                # Dependencias del entorno
├── .gitignore
└── README.md

---

## Cómo reproducir el entorno

```bash
# 1. Clonar el repositorio
git clone https://github.com/juandiazr513/proyecto-grupo7-mcdi500-JD.git

# 2. Crear entorno virtual
python -m venv .venv

# 3. Activar entorno virtual
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Abrir Jupyter Lab
jupyter lab
```

---

## Dataset

| Campo | Detalle |
|---|---|
| Nombre | Student Performance Dataset |
| Fuente | UCI Machine Learning Repository |
| Autores | Cortez, P., & Silva, A. (2008) |
| URL | https://archive.ics.uci.edu/dataset/320/student+performance |
| Archivos | student-mat.csv · student-por.csv |
| Variables | 33 columnas por archivo |
