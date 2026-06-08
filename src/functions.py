def cargar_dataset(ruta):

    """
    Carga un archivo CSV y devuelve un DataFrame.
    """
    return pd.read_csv(ruta) 
 
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
 