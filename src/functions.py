import sys
import os
sys.path.append(os.path.abspath("../src"))

from librerias import *
##
def cargar_dataset(ruta):

    """
    Carga un archivo CSV y devuelve un DataFrame.
    """
    return pd.read_csv(ruta,sep=";") 
 
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
    g3_0    = (df['G3'] == 0).sum()
    deserc  = ((df['G2'] == 0) & (df['G3'] == 0)).sum()
    reprobad= g3_0 - deserc
    print(f"  {nombre}: G3=0 total={g3_0} | G2=0 y G3=0 (deserción)={deserc} | G2>0 y G3=0 (reprobado)={reprobad}")
    return None

