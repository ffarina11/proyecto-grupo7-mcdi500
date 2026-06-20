import math
import sys
import os
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
sys.path.append(os.path.abspath("../src"))

from librerias import *
###

def cargar_dataset(ruta):
    """
    Carga un archivo CSV y devuelve un DataFrame.
    Maneja errores comunes durante la carga del archivo.
    """
    try:
        df = pd.read_csv(ruta, sep=";")
        return df

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta '{ruta}'.")
    except pd.errors.EmptyDataError:
        print("Error: El archivo está vacío.")
    except pd.errors.ParserError:
        print("Error: Hubo un problema al parsear el archivo. Verifica el separador o el formato.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

    return None
 
def resumen_dataset(df, nombre="Dataset"):

    """
    Muestra un resumen básico del DataFrame.
    """

    print("=" * 60)

    print(f"RESUMEN: {nombre}")

    print("=" * 60)

    print(f"Filas: {df.shape[0]}")

    print(f"Columnas: {df.shape[1]}")

    print(f"Duplicados: {df.duplicated().sum()}")

    print(f"Valores nulos: {df.isnull().sum().sum()}")

    print("\nTipos de datos:")

    print(df.dtypes)

    print("=" * 60)
 
 
def mostrar_primeras_filas(df, n=5):

    """
    Muestra las primeras filas del DataFrame.
    """

    return df.head(n)
 
 # ============================================================
# FUNCIÓN: validar_rangos
# Verifica que las variables numéricas estén dentro de los
# rangos válidos según Cortez & Silva (2008).
# Parámetros: df (DataFrame), nombre (str)
# Retorna: pd.DataFrame con resumen de validación
# ============================================================
def validar_rangos(df: pd.DataFrame, nombre: str) -> pd.DataFrame:
    """Verifica rangos válidos de variables numéricas según el diccionario de datos."""
    RANGOS = {
        'age': (15, 22), 'Medu': (0, 4), 'Fedu': (0, 4),
        'traveltime': (1, 4), 'studytime': (1, 4), 'failures': (0, 3),
        'famrel': (1, 5), 'freetime': (1, 5), 'goout': (1, 5),
        'Dalc': (1, 5), 'Walc': (1, 5), 'health': (1, 5),
        'absences': (0, 93), 'G1': (0, 20), 'G2': (0, 20), 'G3': (0, 20)
    }
    print(f"\n{'='*58}")
    print(f"  VALIDACIÓN DE RANGOS — {nombre}")
    print(f"{'='*58}")
    rows = []
    for col, (lo, hi) in RANGOS.items():
        if col not in df.columns:
            continue
        n_fuera = ((df[col] < lo) | (df[col] > hi)).sum()
        estado = '✓' if n_fuera == 0 else '⚠'
        print(f"  {estado} {col:<12} [{lo:>2},{hi:>2}]  fuera de rango: {n_fuera}")
        rows.append({'variable': col, 'rango': f'[{lo},{hi}]', 'n_fuera_rango': n_fuera})
    return pd.DataFrame(rows)

# ============================================================
# FUNCIÓN: detectar_outliers_iqr
# Detecta outliers en variables numéricas continuas usando
# el criterio IQR (Tukey, 1977).
# Parámetros: df, columnas (list), nombre (str)
# Retorna: pd.DataFrame con conteo de outliers por columna
# ============================================================
def detectar_outliers_iqr(df: pd.DataFrame, columnas: list, nombre: str) -> pd.DataFrame:
    """Detecta outliers estadísticos con criterio IQR: fuera de [Q1-1.5*IQR, Q3+1.5*IQR]."""
    print(f"\n{'='*58}")
    print(f"  DETECCIÓN OUTLIERS (IQR) — {nombre}")
    print(f"{'='*58}")
    rows = []
    for col in columnas:
        Q1, Q3 = df[col].quantile(0.25), df[col].quantile(0.75)
        IQR = Q3 - Q1
        li, ls = Q1 - 1.5*IQR, Q3 + 1.5*IQR
        n_out = ((df[col] < li) | (df[col] > ls)).sum()
        pct = n_out / len(df) * 100
        estado = '⚠' if n_out > 0 else '✓'
        print(f"  {estado} {col:<10} Q1={Q1:.1f} Q3={Q3:.1f} IQR={IQR:.1f} "
              f"límites=[{li:.1f},{ls:.1f}] outliers={n_out} ({pct:.1f}%)")
        rows.append({'col': col, 'Q1': Q1, 'Q3': Q3, 'IQR': IQR,
                     'lim_inf': li, 'lim_sup': ls, 'n_outliers': n_out, '%': round(pct,2)})
    return pd.DataFrame(rows)

# ============================================================
# FUNCIÓN: detectar_correlaciones
# Analiza correlaciones entre variables numéricas del dataset.
# ============================================================

def analizar_correlaciones(df, nombre_dataset="Dataset", columnas_excluir=None, guardar_figura=False, ruta_salida=None):
    """
    Analiza correlaciones entre variables numéricas del dataset.
 
    Parámetros:
        df (DataFrame): dataset a analizar.
        nombre_dataset (str): nombre descriptivo del dataset.
        columnas_excluir (list): columnas numéricas que se desean excluir.
        guardar_figura (bool): indica si se guarda la matriz como imagen.
        ruta_salida (str): ruta donde se guardará la figura.
 
    Retorna:
        DataFrame con matriz de correlaciones.
    """
 
    if columnas_excluir is None:
        columnas_excluir = []
 
    df_num = df.select_dtypes(include="number").copy()
 
    if columnas_excluir:
        df_num = df_num.drop(columns=columnas_excluir, errors="ignore")
 
    print(f"\n{'='*70}")
    print(f"ANÁLISIS DE CORRELACIONES — {nombre_dataset}")
    print(f"{'='*70}")
 
    if df_num.shape[1] < 2:
        print("No hay suficientes variables numéricas para calcular correlaciones.")
        return None
 
    matriz_corr = df_num.corr()
 
    print(f"\nVariables numéricas consideradas: {df_num.shape[1]}")
    print("\nCorrelaciones con nota final G3:")
 
    if "G3" in matriz_corr.columns:
        corr_g3 = matriz_corr["G3"].sort_values(ascending=False)
        print(corr_g3)
    else:
        print("La variable G3 no está disponible en el dataset.")
 
    plt.figure(figsize=(12, 8))
    sns.heatmap(
        matriz_corr,
        annot=True,
        cmap="coolwarm",
        fmt=".2f",
        linewidths=0.5
    )
 
    plt.title(f"Matriz de correlación — {nombre_dataset}")
    plt.tight_layout()
 
    if guardar_figura and ruta_salida is not None:
        plt.savefig(ruta_salida, dpi=300, bbox_inches="tight")
        print(f"\nFigura guardada en: {ruta_salida}")
 
    plt.show()
 
    return matriz_corr


# ============================================================
# ANÁLISIS: Variable objetivo G3
# Se analizan los casos G3=0 para decidir si corresponden
# a deserciones o simplemente a reprobados.
# ============================================================
def analizar_g3_cero(df: pd.DataFrame, nombre: str) -> None:
    """Clasifica los registros G3=0 en deserciones (G2=0) vs reprobados (G2>0)."""
    print("\n=== Análisis G3 = 0 ===")
    g3_0    = (df['G3'] == 0).sum()
    deserc  = ((df['G2'] == 0) & (df['G3'] == 0)).sum()
    reprobad= g3_0 - deserc
    print(f"  {nombre}: G3=0 total={g3_0} | G2=0 y G3=0 (deserción)={deserc} | G2>0 y G3=0 (reprobado)={reprobad}")
    return None


# ============================================================
# FUNCIÓN: limpiar_dataset
# Aplica el pipeline completo de limpieza:
#   1. Elimina duplicados (si existen)
#   2. Estandariza texto categórico (strip) #elimina espacios en blanco
#   3. Crea flag 'desercion'
#   4. Agrega columna 'asignatura'
# Parámetros: df (DataFrame), nombre (str: 'mat' o 'por')
# Retorna: pd.DataFrame limpio
# ============================================================
def limpiar_dataset(df: pd.DataFrame, nombre: str) -> pd.DataFrame:
    """Aplica el pipeline de limpieza. Trabaja sobre una copia para no alterar el original."""
    df_c = df.copy()
    n0 = len(df_c)
    print(f"\n  Pipeline de limpieza — {nombre.upper()}")

    # 1. Duplicados
    nd = df_c.duplicated().sum()
    df_c = df_c.drop_duplicates().reset_index(drop=True)
    print(f"  [1] Duplicados eliminados : {nd}  ({'ninguno' if nd==0 else nd})")

    # 2. Strip de espacios en columnas de texto
    cols_str = df_c.select_dtypes(include=['object']).columns
    for col in cols_str:
        df_c[col] = df_c[col].str.strip()
    print(f"  [2] Strip en {len(cols_str)} columnas de texto ✓")

    # 3. Flag de deserción
    df_c['desercion'] = ((df_c['G2'] == 0) & (df_c['G3'] == 0)).astype(int)
    print(f"  [3] Flag 'desercion' creado: {df_c['desercion'].sum()} casos")

    # 4. Identificador de asignatura
    df_c['asignatura'] = nombre
    print(f"  [4] Columna 'asignatura' = '{nombre}' ✓")
    print(f"  Resultado: {n0} → {len(df_c)} filas")
    return df_c


# ============================================================
# FUNCIÓN: winsorizacion
# Aplica capping al percentil superior para reducir el
# impacto de outliers extremos. Preserva valores originales.
# Parámetros: df, columna (str), p_sup (float, default=0.95)
# Retorna: pd.DataFrame con columna ajustada y '{col}_original'
# ============================================================
def winsorizacion(df: pd.DataFrame, columna: str, p_sup: float = 0.95) -> pd.DataFrame:
    """Winsorización (capping superior) al percentil indicado. Preserva valores originales."""
    df_w = df.copy()
    cap = df_w[columna].quantile(p_sup)
    n_afect = (df_w[columna] > cap).sum()
    df_w[f'{columna}_original'] = df_w[columna]      # respaldo
    df_w[columna] = df_w[columna].clip(upper=cap)
    print(f"  Winsorización '{columna}': cap p{int(p_sup*100)}={cap:.0f} → {n_afect} valores ajustados")
    return df_w


# ============================================================
# FUNCIÓN: exportar_dataset
# Exporta un DataFrame a CSV en data/processed/.
# Crea el directorio si no existe.
# Parámetros: df, ruta (str), descripcion (str)
# ============================================================
def exportar_dataset(df: pd.DataFrame, ruta: str, descripcion: str = '') -> None:
    """Guarda el DataFrame en CSV con separador ';'. Crea el directorio si es necesario."""
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    df.to_csv(ruta, index=False, sep=';', encoding='utf-8')
    kb = os.path.getsize(ruta) / 1024
    print(f"  ✓ {os.path.basename(ruta):<42} {df.shape[0]:>4}f × {df.shape[1]:>3}c  ({kb:.1f} KB)")
    if descripcion:
        print(f"    → {descripcion}")



  # ============================================================
# FUNCIÓN: codificar_binarias
# Convierte variables yes/no a 1/0 y crea versiones binarias
# de variables de dos categorías.
# Parámetros: df (DataFrame)
# Retorna: pd.DataFrame con codificación aplicada
# ============================================================
def codificar_binarias(df: pd.DataFrame) -> pd.DataFrame:
    """Codifica variables binarias yes/no a 1/0 y crea features binarias explícitas."""
    df_e = df.copy()

    # Variables yes/no → 1/0
    cols_yn = ['schoolsup','famsup','paid','activities','nursery','higher','internet','romantic']
    for col in cols_yn:
        df_e[col] = df_e[col].map({'yes': 1, 'no': 0})

    # Variables binarias propias con etiqueta explícita
    df_e['sex_F']        = (df_e['sex']     == 'F').astype(int)   # 1=Femenino
    df_e['address_U']    = (df_e['address'] == 'U').astype(int)   # 1=Urbano
    df_e['famsize_GT3']  = (df_e['famsize'] == 'GT3').astype(int) # 1=Familia>3
    df_e['Pstatus_T']    = (df_e['Pstatus'] == 'T').astype(int)   # 1=Juntos
    df_e['school_GP']    = (df_e['school']  == 'GP').astype(int)  # 1=Gabriel Pereira

    print(f"  Codificación binaria: {len(cols_yn)} vars yes/no + 5 vars propias")
    return df_e      


# ============================================================
# FUNCIÓN: codificar_ohe
# Aplica One-Hot Encoding a variables nominales con >2 categorías.
# Se usa drop_first=True para evitar multicolinealidad.
# Parámetros: df (DataFrame)
# Retorna: pd.DataFrame con dummies incorporadas
# ============================================================
def codificar_ohe(df: pd.DataFrame) -> pd.DataFrame:
    """One-Hot Encoding para variables nominales (Mjob, Fjob, reason, guardian)."""
    cols_ohe = [c for c in ['Mjob','Fjob','reason','guardian'] if c in df.columns]
    df_ohe = pd.get_dummies(df, columns=cols_ohe, prefix=cols_ohe,
                             drop_first=True, dtype=int)
    nuevas = df_ohe.shape[1] - df.shape[1]
    print(f"  OHE aplicado en {cols_ohe} → {nuevas} nuevas columnas")
    return df_ohe


# ============================================================
# FUNCIÓN: crear_variables_derivadas
# Genera nuevas variables con valor analítico directo:
#   nota_promedio, aprobado, progreso_g1_g3,
#   nivel_alcohol, edu_familiar_media
# Parámetros: df (DataFrame)
# Retorna: pd.DataFrame con variables derivadas
# ============================================================
def crear_variables_derivadas(df: pd.DataFrame) -> pd.DataFrame:
    """Crea variables derivadas para enriquecer el EDA y el modelado."""
    df_d = df.copy()    
    df_d['aprobado']           = (df_d['G3'] >= 10).astype(int)     # umbral Portugal
    df_d['progreso_g1_g3']     = df_d['G3'] - df_d['G1']           # evolución académica
    df_d['nivel_alcohol']      = ((df_d['Dalc'] + df_d['Walc']) / 2).round(2)
    df_d['edu_familiar_media'] = ((df_d['Medu'] + df_d['Fedu']) / 2).round(2)
    nuevas = ['aprobado','progreso_g1_g3','nivel_alcohol','edu_familiar_media']
    print(f"  Variables derivadas creadas: {nuevas}")
    return df_d


# ============================================================
# FUNCIÓN: validar_dataset_final
# Ejecuta asserts para verificar integridad post-procesamiento.
# Parámetros: df_orig, df_proc (DataFrames), nombre (str)
# Retorna: True si todas las pruebas pasan
# ============================================================
def validar_dataset_final(df_orig: pd.DataFrame, df_proc: pd.DataFrame, nombre: str) -> bool:
    """Valida integridad del dataset procesado vs el original."""
    print(f"\n  Validando: {nombre}")
    ok = True
    try:
        # 1. Sin pérdida de filas
        assert len(df_proc) == len(df_orig), \
            f"Pérdida de filas: orig={len(df_orig)} proc={len(df_proc)}"
        print(f"  ✓ Filas conservadas: {len(df_proc)}")

        # 2. Sin nulos introducidos en columnas originales
        cols_orig = [c for c in df_orig.columns if c in df_proc.columns]
        nulos_proc = df_proc[cols_orig].isnull().sum().sum()
        assert nulos_proc == 0, f"Nulos introducidos: {nulos_proc}"
        print(f"  ✓ Sin nulos en columnas originales")

        # 3. G1, G2, G3 no modificados
        for col in ['G1','G2','G3']:
            assert (df_proc[col].values == df_orig[col].values).all(), \
                f"Columna {col} modificada"
        print(f"  ✓ G1, G2, G3 intactos")

        # 4. Flag aprobado coherente con G3
        if 'aprobado' in df_proc.columns:
            assert (df_proc['aprobado'] == (df_proc['G3'] >= 10).astype(int)).all(), \
                "Flag 'aprobado' inconsistente con G3"
            print(f"  ✓ Flag 'aprobado' coherente ({df_proc['aprobado'].sum()} aprobados)")

        # 5. Flag desercion coherente
        if 'desercion' in df_proc.columns:
            esperado = ((df_proc['G2'] == 0) & (df_proc['G3'] == 0)).astype(int)
            assert (df_proc['desercion'] == esperado).all(), \
                "Flag 'desercion' inconsistente"
            print(f"  ✓ Flag 'desercion' coherente ({df_proc['desercion'].sum()} casos)")

        # 6. Sin duplicados
        assert not df_proc.duplicated().any(), "Hay filas duplicadas"
        print(f"  ✓ Sin filas duplicadas")

        # 7. Rangos de calificaciones
        for col in ['G1','G2','G3']:
            assert df_proc[col].between(0, 20).all(), f"{col} fuera de [0,20]"
        print(f"  ✓ G1, G2, G3 en rango [0, 20]")

        print(f"  → VALIDACIÓN EXITOSA ✅")
    except AssertionError as e:
        print(f"  → ERROR: {e} ❌")
        ok = False
    return ok

# ============================================================
# FUNCIÓN: integrar_datasets
# Combina dos DataFrames mediante concatenación vertical.
# Parámetros: df_a, df_b (DataFrames con col 'asignatura')
# Retorna: pd.DataFrame combinado con índice reiniciado
# ============================================================
def integrar_datasets(df_a: pd.DataFrame, df_b: pd.DataFrame) -> pd.DataFrame:
    """Concatena verticalmente dos DataFrames. Requiere columna 'asignatura'."""
    df_comb = pd.concat([df_a, df_b], axis=0, ignore_index=True)
    print(f"  Concatenado: {len(df_a)} + {len(df_b)} = {len(df_comb)} registros")
    print("  Distribución:\n", df_comb['asignatura'].value_counts().to_string())
    return df_comb

 ##Funcion para mostrar estadisticas descriptivas F3*
def estadisticas_descriptivas(df):
     return df.describe().round(2)


##FUNCION PARA GRAFICAS VARIABLES CATEGORICAS F3*
def plot_distribucion_categoricas(df, categorical_cols,
                                   titulo='General',
                                   output_dir='../data/processed/F3/',
                                   figsize=(15, 10), dpi=100):

    n_cols = 4
    n_rows = math.ceil(len(categorical_cols) / n_cols)

    plt.figure(figsize=figsize)
    for i, col in enumerate(categorical_cols):
        counts = df[col].value_counts()
        counts_df = counts.rename_axis(col).reset_index(name='count')
        palette = sns.color_palette('tab20', len(counts_df))

        plt.subplot(n_rows, n_cols, i + 1)
        sns.barplot(x='count', y=col, data=counts_df, hue=col, dodge=False, palette=palette, legend=False)
        plt.title(f'Distribution of {col}')
        plt.xlabel('Count')
        plt.ylabel(col)

    plt.suptitle("Distribución de Variables Categóricas", fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()

    # ── Nombre de archivo basado en el título ─────────────────
    nombre = titulo.lower().replace(' ', '_').replace('á','a').replace('é','e') \
                           .replace('í','i').replace('ó','o').replace('ú','u')
    output_path = os.path.join(output_dir, f"fig_distribucion_categoricas_{nombre}.png")

    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(output_path, dpi=dpi, bbox_inches='tight')
    plt.show()

##funcion para graficar boxplot de ausencias F3*
def plot_outliers_boxplot(df, columna='absences',
                          suptitulo=None,
                          titulo='General',
                          output_dir='../data/processed/F3/',
                          figsize=(6, 4), dpi=100):
    """
    Genera un boxplot de una columna para visualizar su distribución/outliers
    según criterio IQR.
     Parámetros:
        df (pd.DataFrame): DataFrame con los datos.
        columna (str): Nombre de la columna a graficar.
        suptitulo (str): Título general de la figura. Si es None, se genera uno automático.
        output_path (str): Ruta donde se guardará la imagen.
        figsize (tuple): Tamaño de la figura.
        dpi (int): Resolución de la imagen guardada.
    """
    if suptitulo is None:
        suptitulo = f'Outliers en variable {columna} (criterio IQR)'

    fig, ax = plt.subplots(figsize=figsize)

    ax.boxplot(df[columna], vert=True, patch_artist=True,
               boxprops=dict(facecolor='#AED6F1', color='#2874A6'),
               medianprops=dict(color='red', linewidth=2),
               flierprops=dict(marker='o', color='orange', alpha=0.6))
    ax.set_title('Distribución de Ausencias', fontweight='bold')
    ax.set_ylabel(columna)
    ax.set_xticks([])

    plt.suptitle(suptitulo, y=1.02)
    plt.tight_layout()

    # ── Nombre de archivo basado en título y columna ───────────
    nombre = titulo.lower().replace(' ', '_').replace('á','a').replace('é','e') \
                           .replace('í','i').replace('ó','o').replace('ú','u')
    output_path = os.path.join(output_dir, f"fig_outliers_{columna}_{nombre}.png")

    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(output_path, dpi=dpi, bbox_inches='tight')
    plt.show()


def plot_distribucion_g3(df, titulo='Matemáticas', color='#3498DB',
                          output_dir='../data/processed/F3/',
                          figsize=(6, 4), dpi=100):

    fig, ax = plt.subplots(figsize=figsize)

    ax.hist(df['G3'], bins=21, range=(-0.5, 20.5), color=color, edgecolor='white', alpha=0.85)
    ax.axvline(10, color='red', linestyle='--', linewidth=1.5, label='Umbral aprobación (10)')
    ax.axvline(df['G3'].mean(), color='navy', linestyle=':', linewidth=1.5,
               label=f"Media={df['G3'].mean():.1f}")
    ax.set_title(f'Distribución G3 — {titulo}', fontweight='bold')
    ax.set_xlabel('Calificación final (G3)')
    ax.set_ylabel('Frecuencia')
    ax.legend(fontsize=9)

    plt.suptitle('Variable Objetivo G3: Calificación Final', fontsize=12)
    plt.tight_layout()

    # ── Nombre de archivo basado en el título ─────────────────
    nombre = titulo.lower().replace(' ', '_').replace('á','a').replace('é','e') \
                           .replace('í','i').replace('ó','o').replace('ú','u')
    output_path = os.path.join(output_dir, f"fig_distribucion_g3_{nombre}.png")

    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(output_path, dpi=dpi, bbox_inches='tight')
    plt.show()


# función de ordenamiento merge sort F3
def merge_sort(lista):
    """
    Ordena una lista usando Merge Sort recursivo (divide y vencerás, O(n log n)).
    CASO BASE     : lista de 0 o 1 elemento → ya ordenada, se retorna tal cual.
    CASO RECURSIVO: divide la lista a la mitad, ordena cada parte
                    recursivamente y combina los resultados.
    """
    if len(lista) <= 1:               # CASO BASE: lista mínima, nada que ordenar
        return lista

    medio = len(lista) // 2
    izq = merge_sort(lista[:medio])   # divide → ordena mitad izquierda
    der = merge_sort(lista[medio:])   # divide → ordena mitad derecha
    return combinar(izq, der)         # y vence (combina)

# Función auxiliar para combinar dos listas ordenadas en una sola lista ordenada
def combinar(a, b):
    """Fusiona dos listas ya ordenadas en una sola lista ordenada."""
    res, i, j = [], 0, 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            res.append(a[i]); i += 1
        else:
            res.append(b[j]); j += 1
    res.extend(a[i:]); res.extend(b[j:])
    return res

# Función para determinar aprobado usando un bucle fila a fila F3*
def aprobado_bucle(df: pd.DataFrame) -> list:
    """
    Determina si cada estudiante aprobó (G3 >= 10) usando un bucle fila a fila.
    Complejidad: O(n) — pero lento por el overhead de Python en cada iteración.
    """
    resultado = []
    for _, fila in df.iterrows():        # iterrows es lento: crea un objeto por fila
        resultado.append(1 if fila["G3"] >= 10 else 0)
    return resultado

# Función para determinar aprobado usando operación vectorizada F3*
def aprobado_vectorizado(df: pd.DataFrame) -> pd.Series:
    """
    Determina si cada estudiante aprobó (G3 >= 10) con operación vectorizada.
    Complejidad: O(n) — pero rápido porque opera en C/NumPy de una sola vez.
    """
    return (df["G3"] >= 10).astype(int)

##FUNCION PARA GRAFICAR RADAR COMPARATIVO MAT VS POR F4*
def plot_radar_reprobaciones(df_mat, df_por,
                              output_dir='../data/processed/F4/',
                              figsize=(14, 7.8), dpi=110):
    from matplotlib.lines import Line2D

    #metricas    = ['studytime', 'G3', 'Walc', 'Medu', 'absences']
    #nombres_eje = ['Tiempo\nestudio', 'Nota final', 'Alcohol\nfin de semana',
    #               'Educ.\nmadre', 'Ausencias']

    metricas    = ['studytime', 'G3', 'nivel_alcohol', 'edu_familiar_media', 'absences']
    nombres_eje = ['Tiempo\nestudio', 'Nota final', 'Alcohol\nen la semana',
                   'Educ.\nPadres', 'Ausencias']

    COLOR_0    = '#2BB5A0'
    COLOR_3MAS = '#E8714A'
    angulos    = np.linspace(0, 2 * np.pi, len(metricas), endpoint=False).tolist()
    angulos   += angulos[:1]

    configs = [
        {'df': df_mat, 'titulo': 'Matemáticas'},
        {'df': df_por, 'titulo': 'Portugués'},
    ]

    fig, axes = plt.subplots(1, 2, figsize=figsize, subplot_kw={'polar': True})

    for ax, cfg in zip(axes, configs):
        df = cfg['df'].copy()
        grupo_0    = df[df['failures'] == 0]
        grupo_3mas = df[df['failures'] >= 3]

        global_min = df[metricas].min()
        global_max = df[metricas].max()

        def normalizar(grupo):
            return ((grupo[metricas].mean() - global_min) /
                    (global_max - global_min)).clip(0, 1)

        for niv in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]:
            ax.plot(angulos, [niv] * len(angulos), color='#CCCCCC', linewidth=0.6)
            ax.text(angulos[1], niv, f'{niv}', ha='center', va='bottom',
                    fontsize=7.5, color='#888888')
        for ang in angulos[:-1]:
            ax.plot([ang, ang], [0, 1], color='#CCCCCC', linewidth=0.6)

        for norm, color in [(normalizar(grupo_0), COLOR_0),
                            (normalizar(grupo_3mas), COLOR_3MAS)]:
            vals = norm.tolist() + norm.tolist()[:1]
            ax.plot(angulos, vals, linewidth=2.3, color=color)
            ax.fill(angulos, vals, alpha=0.13, color=color)

        ax.set_ylim(0, 0.85)
        ax.set_xticks(angulos[:-1])
        ax.set_xticklabels(nombres_eje, fontsize=10)
        ax.set_yticklabels([])
        ax.grid(False)
        ax.spines['polar'].set_visible(False)
        ax.set_title(
            f'{cfg["titulo"]}\n(0 reprob.: n={len(grupo_0)} | 3+ reprob.: n={len(grupo_3mas)})',
            pad=28, fontsize=11.5, fontweight='bold'
        )
        ax.legend(handles=[
            Line2D([0], [0], color=COLOR_0,    linewidth=2.3, label='0 reprobaciones'),
            Line2D([0], [0], color=COLOR_3MAS, linewidth=2.3, label='3+ reprobaciones'),
        ], loc='lower center', bbox_to_anchor=(0.5, -0.20), ncol=2, frameon=False, fontsize=9.5)

    plt.suptitle('Perfil comparativo de estudiantes según historial de reprobaciones: 0 vs. 3+ reprobaciones',
                 fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, 'fig_radar_reprobaciones.png'), dpi=dpi, bbox_inches='tight')
    plt.show()


    # ============================================================
# GENERADOR DE DATOS SINTÉTICOS — respaldo de reproducibilidad
# Replica el esquema del Student Performance Dataset con las
# proporciones observadas en la Fase 2 del proyecto.
# ============================================================
SEMILLA = 42
np.random.seed(SEMILLA)
def generar_datos_sinteticos_estudiantes(asignatura: str,
                                          semilla: int = SEMILLA) -> pd.DataFrame:
    """
    Genera un DataFrame con el mismo esquema que el Student Performance Dataset
    (Cortez & Silva, 2008). Se usa SOLO como respaldo cuando los CSV originales
    no están disponibles, garantizando que el pipeline sea ejecutable de
    principio a fin sin dependencias externas.

    Parámetros
    ----------
    n          : número de filas a generar (395 para mat, 649 para por).
    asignatura : 'mat' o 'por' — ajusta las proporciones según los
                 estadísticos observados en la Fase 2.
    semilla    : semilla para reproducibilidad (default = SEMILLA global).

    Retorna
    -------
    pd.DataFrame con las 33 columnas originales del dataset.
    """
    rng = np.random.default_rng(semilla)
    if asignatura == 'Matemáticas':
        n = 395
    elif asignatura == 'Portugués':
        n = 649

    # Proporciones calibradas con los estadísticos de Fase 2
    g3_boost = 1 if asignatura == 'por' else 0   # Portugués tiene media G3 ~1 pt mayor

    g1 = rng.integers(4, 19, n)
    g2 = np.clip(g1 + rng.integers(-2, 3, n), 0, 20)
    g3 = np.clip(g2 + rng.integers(-2, 3, n) + g3_boost, 0, 20)

    df = pd.DataFrame({
        # Variables demográficas
        'school'    : rng.choice(['GP', 'MS'], n, p=[0.78, 0.22]),
        'sex'       : rng.choice(['F', 'M'],   n, p=[0.53, 0.47]),
        'age'       : rng.integers(15, 22, n),
        'address'   : rng.choice(['U', 'R'],   n, p=[0.77, 0.23]),
        'famsize'   : rng.choice(['GT3', 'LE3'], n, p=[0.74, 0.26]),
        'Pstatus'   : rng.choice(['T', 'A'],   n, p=[0.90, 0.10]),
        # Variables socioeconómicas
        'Medu'      : rng.integers(0, 5, n),
        'Fedu'      : rng.integers(0, 5, n),
        'Mjob'      : rng.choice(['teacher','health','services','at_home','other'], n,
                                 p=[0.09, 0.09, 0.18, 0.20, 0.44]),
        'Fjob'      : rng.choice(['teacher','health','services','at_home','other'], n,
                                 p=[0.07, 0.04, 0.23, 0.08, 0.58]),
        'reason'    : rng.choice(['home','reputation','course','other'], n,
                                 p=[0.27, 0.31, 0.27, 0.15]),
        'guardian'  : rng.choice(['mother','father','other'], n, p=[0.60, 0.33, 0.07]),
        # Hábitos de estudio
        'traveltime': rng.choice([1,2,3,4], n, p=[0.48, 0.35, 0.12, 0.05]),
        'studytime' : rng.choice([1,2,3,4], n, p=[0.20, 0.45, 0.25, 0.10]),
        'failures'  : rng.choice([0,1,2,3], n, p=[0.67, 0.18, 0.10, 0.05]),
        # Apoyo escolar y familiar
        'schoolsup' : rng.choice(['yes','no'], n, p=[0.18, 0.82]),
        'famsup'    : rng.choice(['yes','no'], n, p=[0.55, 0.45]),
        'paid'      : rng.choice(['yes','no'], n, p=[0.35, 0.65]),
        'activities': rng.choice(['yes','no'], n, p=[0.50, 0.50]),
        'nursery'   : rng.choice(['yes','no'], n, p=[0.81, 0.19]),
        'higher'    : rng.choice(['yes','no'], n, p=[0.94, 0.06]),
        'internet'  : rng.choice(['yes','no'], n, p=[0.84, 0.16]),
        'romantic'  : rng.choice(['yes','no'], n, p=[0.34, 0.66]),
        # Hábitos sociales
        'famrel'    : rng.integers(1, 6, n),
        'freetime'  : rng.integers(1, 6, n),
        'goout'     : rng.integers(1, 6, n),
        'Dalc'      : rng.integers(1, 6, n),
        'Walc'      : rng.integers(1, 6, n),
        'health'    : rng.integers(1, 6, n),
        'absences'  : rng.integers(0, 30, n),
        # Calificaciones
        'G1': g1, 'G2': g2, 'G3': g3,
    })
    return df