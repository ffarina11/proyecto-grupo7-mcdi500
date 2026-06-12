import sys
import os
sys.path.append(os.path.abspath("../src"))

from librerias import *
###

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
