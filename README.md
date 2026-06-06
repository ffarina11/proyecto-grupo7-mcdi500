# 🎓 Proyecto Grupo 7 — MCDI500
### *Factores socioeconómicos y de preparación previa asociados al rendimiento académico*

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Jupyter-Lab-orange?style=for-the-badge&logo=jupyter&logoColor=white" alt="Jupyter">
  <img src="https://img.shields.io/badge/Curso-MCDI500-green?style=for-the-badge" alt="MCDI500">
</p>

---

## 📝 Descripción

Este repositorio contiene el proyecto transversal del curso **MCDI500 — Herramientas de Software Científico** del **Magíster en Ciencias de Datos e Inteligencia Artificial** de la *Universidad Andrés Bello (UNAB)*.

El objetivo principal de esta investigación es analizar el **Student Performance Dataset** [(Cortez & Silva, 2008)](https://archive.ics.uci.edu/dataset/320/student+performance) para identificar y evaluar qué factores socioeconómicos y de preparación previa explican de mejor manera las diferencias en el rendimiento académico entre estudiantes de dos establecimientos educacionales portugueses.

---

## 👥 Integrantes — Grupo 7

| Nombre | Rol | GitHub / Contacto |
| :--- | :---: | :---: |
| **Juan de Dios Díaz Ríos** | Integrante | [@juandiazr513](https://github.com/juandiazr513) |
| **Francisco Fariña Molina** | Integrante | [@ffarina11](https://github.com/ffarina11)|
| **Constanza Moreno Giacometto** | Integrante | [Contacto](#) |
| **Yenne Sepúlveda Jerez** | Integrante | [Contacto](#) |

* **Docente:** Omar Salinas Silva

---

## 📁 Estructura del Repositorio

```text
proyecto-grupo7-mcdi500/
├── 📂 data/
│   ├── 📂 raw/                      # Datos originales sin modificar (.csv)
│   │   ├── student-mat.csv
│   │   └── student-por.csv
│   └── 📂 processed/                # Datos limpios y procesados (Fase 2)
├── 📂 notebooks/
│   └── 📓 F1_Definicion.ipynb       # Fase 1: Definición del problema y EDA inicial
├── 📂 src/                          # Scripts y funciones modulares reutilizables
├── 📂 docs/                         # Documentación complementaria e informes
├── 📄 .gitignore                    # Archivos ignorados por Git
├── 📄 README.md                     # Descripción general del proyecto
└── 📄 requirements.txt              # Dependencias del entorno de desarrollo
```

---

## 🚀 Cómo Reproducir el Entorno

Sigue estos pasos en tu terminal (por ejemplo, **Git Bash**) para clonar el repositorio e instalar todas las dependencias necesarias:

### 1. Clonar el repositorio
```bash
git clone https://github.com/ffarina11/proyecto-grupo7-mcdi500-FF.git
cd proyecto-grupo7-mcdi500-JD
```

### 2. Configurar el entorno virtual
```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# En Windows (Git Bash):
source .venv/Scripts/activate

# En macOS/Linux:
source .venv/bin/activate
```

### 3. Instalar dependencias e iniciar
```bash
# Actualizar pip e instalar librerías
pip install --upgrade pip
pip install -r requirements.txt

# Abrir el entorno de Jupyter
jupyter lab
```

---

## 📊 Información del Dataset

| Atributo | Detalle |
| :--- | :--- |
| **Nombre** | Student Performance Dataset |
| **Fuente** | UCI Machine Learning Repository |
| **Autores** | Cortez, P., & Silva, A. (2008) |
| **URL Oficial** | [🔗 Acceder al Dataset](https://archive.ics.uci.edu/dataset/320/student+performance) |
| **Archivos Incluidos** | `student-mat.csv` (Matemáticas) · `student-por.csv` (Portugués) |
| **Dimensiones** | 33 variables socioeconómicas, demográficas y académicas |

---
<p align="center"><sub>Magíster en Ciencias de Datos e Inteligencia Artificial • UNAB • 2026</sub></p>
