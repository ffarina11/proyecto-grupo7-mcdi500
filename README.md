#  Proyecto Grupo 7 — MCDI500
### *Factores socioeconómicos y de preparación previa asociados al rendimiento académico*

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Jupyter-Lab-orange?style=for-the-badge&logo=jupyter&logoColor=white" alt="Jupyter">
  <img src="https://img.shields.io/badge/Curso-MCDI500-green?style=for-the-badge" alt="MCDI500">
</p>

---

##  Descripción

Este repositorio contiene el proyecto transversal del curso **MCDI500 — Programación para la ciencia de datos** del **Magíster en Ciencias de Datos e Inteligencia Artificial** de la *Universidad Andrés Bello (UNAB)*.

El objetivo principal de esta investigación es analizar el **Student Performance Dataset** [(Cortez & Silva, 2008)](https://archive.ics.uci.edu/dataset/320/student+performance) para identificar y evaluar qué factores socioeconómicos y de preparación previa explican de mejor manera las diferencias en el rendimiento académico entre estudiantes de dos establecimientos educacionales portugueses.

---

##  Integrantes — Grupo 7

| Nombre | Rol | GitHub / Contacto |
| :--- | :---: | :---: |
| **Juan de Dios Díaz Ríos** | Integrante | [@juandiazr513](https://github.com/juandiazr513) |
| **Francisco Fariña Molina** | Integrante | [@ffarina11](https://github.com/ffarina11)|
| **Constanza Moreno Giacometto** | Integrante | [@ConstanzaM0](https://github.com/ConstanzaM0) |
| **Yenne Sepúlveda Jerez** | Integrante | [@yennesepulveda](https://github.com/yennesepulveda) |

* **Docente:** Omar Salinas Silva

---

##  Estructura del Repositorio

```text
proyecto-grupo7-mcdi500/
├── 📂 data/
│   ├── 📂 raw/                      # Datos originales sin modificar (.csv)
│   │   ├── student-mat.csv
│   │   └── student-por.csv
│   │
│   ├── 📂 processed/               # Datos limpios y transformados (Fase 2)
│   │   ├── student_mat_clean.csv
│   │   ├── student_mat_clean_encode.csv
│   │   ├── student_por_clean.csv
│   │   ├── student_por_clean_encode.csv
│   │   ├──student_union_clean_encode.csv
│   │   ├── fig_distribucion_g3.png 
│   │   └── 📂 F3                        # Archivos generados por métodos de la clase
│   │   
│   └── 📂 development/             # Figuras y outputs exploratorios 
│       
│
├── 📂 notebooks/
│   ├── F1_Definicion.ipynb                  # Fase 1: Definición del problema y EDA inicial
│   └── F2_limpieza.ipynb                    # Fase 2: Limpieza, transformación y validación
│   └── F3_Nucleo_Algoritmico_POO.ipynb      # Fase 3: Núcleo algorítmico y POO
│   └── F4_Integracion_Cierre_Tecnico.ipynb       # Fase 4: Integración, Análisis de Resultados y Cierre Técnico
│
├── 📂 src/                        # Scripts reutilizables
│   ├── functions.py               # Pipeline funcional (Fase 2)
│   ├── librerias.py           
│   └── clases.py                   # Clases POO: PreprocesadorAsignatura y subclases (Fase 3)
│   
│    
├── 📂 docs/                       # Documentación complementaria e informes
├── 📄 .gitignore                  # Archivos ignorados por Git
├── 📄 README.md                   # Descripción general del proyecto
└── 📄 requirements.txt            # Dependencias del entorno de desarrollo
```

---

##  Cómo Reproducir el Entorno

Sigue estos pasos en tu terminal (por ejemplo, **Git Bash**) para clonar el repositorio e instalar todas las dependencias necesarias:

### 1. Clonar el repositorio
```bash
git clone https://github.com/ffarina11/proyecto-grupo7-mcdi500
cd proyecto-grupo7-mcdi500
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
## Preparación de Datos

En la Fase 1 del proyecto se realizó la preparación inicial de los datos con los siguientes pasos:

### 1. Descarga de datos

Los archivos originales se obtuvieron desde el [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/320/student+performance):

- `student-mat.csv` (Matemáticas)
- `student-por.csv` (Portugués)

Se almacenaron en:
data/raw


### 2. Carga y organización inicial

- Ambos datasets se cargan por separado para preservar la integridad de los datos originales.  
- Las celdas Markdown de los notebooks documentan el proceso de carga y la ubicación de los archivos.  
- No se realizan modificaciones sobre los archivos crudos (`raw`).

### 3. Exploración preliminar

- Inspección básica: primeras filas, tipos de variables y detección de valores ausentes.  
- El análisis exploratorio completo, limpieza y preprocesamiento se realizará en la **Fase 2** del proyecto.

> Nota: Esta sección asegura la reproducibilidad de la carga inicial de datos y la estructura de carpetas, siguiendo las buenas prácticas de manejo de datos.
---


## Limpieza, Transformación y Validación

En la Fase 2 del proyecto se implementó un pipeline reproducible de limpieza, transformación y validación de datos, con el objetivo de asegurar la calidad del dataset antes de las etapas de modelado predictivo.

### 1. Ejecución del notebook

Con el entorno virtual activo, desde la raíz del repositorio:

```bash
jupyter lab 
```

Luego abrir:

```bash
notebooks/F2_limpieza.ipynb
```

> Ejecutar con **Kernel → Restart & Run All** para garantizar la reproducibilidad completa.



### 2. Organización de datos procesados

Los datos procesados se exportan automáticamente a `data/processed/`, mientras que las visualizaciones generadas durante el análisis exploratorio se almacenan en `data/development/`.

```text
data/processed/
├── student_mat_clean.csv            # Dataset limpio (Matemáticas)
├── student_mat_clean_encode.csv     # Dataset limpio + transformaciones (Matemáticas)
├── student_por_clean.csv            # Dataset limpio (Portugués)
├── student_por_clean_encode.csv     # Dataset limpio + transformaciones (Portugués)
├── student_union_clean_encode.csv   # Dataset combinado (Matemáticas + Portugués)
└── fig_distribucion_g3.png          # Distribución de la variable objetivo G3
data/development/                    # Archivos intermedios y de exploración
```



## Núcleo Algorítmico y Programación Orientada a Objetos
La Fase 3 consolida el pipeline de la Fase 2 dentro de un núcleo algorítmico orientado a objetos, incorporando principios de POO, algoritmos recursivos y análisis de eficiencia computacional.

### 1. Ejecución del notebook

Con el entorno virtual activo, desde la raíz del repositorio:

```bash
jupyter lab 
```

Luego abrir:

```bash
notebooks/F3_Nucleo_Algoritmico_POO.ipynb
```
y ejecutar con Kernel → Restart & Run All.



### 2. Arquitectura modular

La Fase 3 incorpora nuevos módulos reutilizables dentro de src/:
| Módulo | Responsabilidad |
| :--- | :--- |
| `librerias.py` | Contiene las librerias necesarias para desarrollar el proyecto. |
| `clases.py` | Define la clase base `PreprocesadorAsignatura` y las subclases `PreprocesadorMatematicas` y `PreprocesadorPortugues`. |
| `functions.py` | Contiene las funciones del pipeline desarrollado en la Fase 2, reutilizadas por los métodos de las clases de preprocesamiento. |

### 3. Funcionalidades implementadas
- Encapsulación del pipeline de preprocesamiento mediante Programación Orientada a Objetos.
- Aplicación de herencia y polimorfismo mediante clases especializadas por asignatura.
- Implementación y validación de algoritmos recursivos para el procesamiento de datos.
- Comparación de eficiencia entre enfoques iterativos y vectorizados.
- Validación automática de la integridad de los datasets procesados.
- Exportación de datasets limpios y transformados para etapas posteriores del proyecto.


## Integración, Análisis de Resultados y Cierre Técnico

La Fase 4 consolida los componentes desarrollados en las etapas anteriores del proyecto, integrando el pipeline de preprocesamiento, la arquitectura orientada a objetos y los mecanismos de validación implementados previamente. Además, se realiza el análisis final de resultados, la generación de visualizaciones interpretativas y la documentación técnica de cierre del proyecto.

### 1. Ejecución del notebook

Con el entorno virtual activo, desde la raíz del repositorio:

```bash
jupyter lab 
```

Luego abrir:

```bash
notebooks/F4_Integracion_Cierre_Tecnico.ipynb
```
y ejecutar con Kernel → Restart & Run All.

### 2. Integración de componentes

La Fase 4 articula los desarrollos implementados en las fases anteriores dentro de un flujo de trabajo unificado:

| Componente | Descripción |
| :--- | :--- |
| Pipeline funcional (F2) | Reutilización de las funciones de limpieza, transformación y validación de datos. |
| Arquitectura POO (F3) | Uso de clases especializadas para el procesamiento de los datasets de Matemáticas y Portugués. |
| Validación técnica | Verificación de consistencia, integridad y reproducibilidad de los resultados obtenidos. |
| Análisis de resultados | Evaluación de relaciones entre variables y rendimiento académico mediante métricas y visualizaciones. |
| Documentación final | Consolidación de evidencias técnicas y trazabilidad del proyecto. |

### 3. Funcionalidades implementadas

- Integración completa de los componentes desarrollados en las fases anteriores.
- Ejecución automatizada del flujo de procesamiento de datos mediante clases reutilizables.
- Validación de resultados mediante pruebas de consistencia e integridad de los datasets.
- Generación de estadísticas descriptivas y análisis comparativos entre asignaturas.
- Construcción de visualizaciones para apoyar la interpretación de los hallazgos obtenidos.
- Consolidación de resultados y evidencias para la documentación final del proyecto.
- Verificación de reproducibilidad mediante ejecución completa del notebook sin intervención manual.

### 4. Resultados generados

La ejecución de la Fase 4 genera visualizaciones exploratorias, gráficos comparativos y evidencias utilizadas para el análisis final de los datos. Estos resultados permiten interpretar las relaciones entre las variables estudiadas, respaldar los hallazgos obtenidos durante el proyecto y facilitar la comunicación de resultados mediante representaciones visuales claras y reproducibles.


### 5. Cierre técnico

Como parte del cierre técnico del proyecto se verifica que:

- Todos los notebooks son ejecutables de principio a fin mediante **Restart & Run All**.
- Las dependencias del proyecto se encuentran documentadas en `requirements.txt`.
- Los resultados son reproducibles utilizando los datos originales almacenados en `data/raw`.
- La estructura del repositorio mantiene trazabilidad entre código, datos, documentación y resultados.
- Las decisiones técnicas implementadas durante el desarrollo quedan documentadas en los notebooks y en el repositorio GitHub.



##  Información del Dataset

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
