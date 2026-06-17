"""
============================================================
 MCDI500 — Proyecto Transversal — Grupo 7
 Fase 3: Núcleo Algorítmico y Programación Orientada a Objetos
 Módulo: clases.py

 Encapsula el pipeline de la Fase 2 (carga, exploración,
 limpieza, transformación y validación) dentro de una clase
 reutilizable, aplicando los conceptos de:

   - Clase, objeto, atributo, método, constructor (__init__)
   - Herencia (clase base -> clases hijas por asignatura)
   - Polimorfismo (mismo método, distinta interpretación
     según la asignatura)

 Internamente, los métodos de esta clase REUTILIZAN las
 funciones ya validadas en `functions.py` (Fase 2). Es decir,
 la POO aquí actúa como una capa de organización y estado
 sobre el pipeline funcional existente, sin reescribirlo.

 NOTA DE AJUSTE — versión alineada con el `functions.py` real
 del proyecto (el que usa F2_limpieza.ipynb):
   - `cargar_dataset(ruta)` no imprime nada -> cargar() agrega
     su propio mensaje de confirmación.
   - `resumen_dataset(df, nombre)` solo imprime y retorna None
     -> explorar() ya no depende de su valor de retorno; arma
     su propio diccionario-resumen a partir de self.df.
   - `crear_variables_derivadas(df)` crea 4 variables
     (aprobado, progreso_g1_g3, nivel_alcohol,
     edu_familiar_media) y NO incluye 'nota_promedio'
     -> transformar() agrega 'nota_promedio' como una variable
     adicional a nivel de objeto (extensión de la Fase 3 sobre
     el pipeline de la Fase 2, sin modificar functions.py).
============================================================
"""

import os
import pandas as pd

from functions import (
    cargar_dataset, mostrar_primeras_filas,estadisticas_descriptivas, plot_distribucion_g3,resumen_dataset,
    validar_rangos, detectar_outliers_iqr,plot_distribucion_categoricas ,plot_outliers_boxplot
    ,analizar_correlaciones,
    analizar_g3_cero, limpiar_dataset, winsorizacion,
    codificar_binarias, codificar_ohe, crear_variables_derivadas,
    validar_dataset_final, exportar_dataset,
)


# ============================================================
# CLASE BASE
# ============================================================
class PreprocesadorAsignatura:
    """Clase base que encapsula el pipeline completo de la Fase 2
    (carga -> exploración -> limpieza -> transformación -> validación
    -> exportación) para UNA asignatura del Student Performance Dataset.

    Atributos de instancia
    -----------------------
    ruta : str
        Ruta al CSV crudo (data/raw/...).
    asignatura : str
        Identificador corto de la asignatura ('mat' o 'por').
    df_raw : pd.DataFrame | None
        Copia inmutable de los datos originales (tal cual se cargan).
    df : pd.DataFrame | None
        Copia de trabajo: se actualiza en limpiar().
    df_enc : pd.DataFrame | None
        Versión codificada/transformada (resultado de transformar()).

    Atributo de clase
    -----------------
    NOMBRE_ASIGNATURA : str
        Nombre legible de la asignatura. Se sobrescribe en cada
        clase hija (PreprocesadorMatematicas, PreprocesadorPortugues).
    """

    NOMBRE_ASIGNATURA = "Genérica"

    def __init__(self, ruta: str, asignatura: str):
        # __init__ es el constructor: deja listos los atributos del objeto.
        self.ruta = ruta
        self.asignatura = asignatura
        self.df_raw = None
        self.df = None
        self.df_enc = None

    # --------------------------------------------------------
    # 1. CARGA
    # --------------------------------------------------------
    def cargar(self) -> pd.DataFrame:
        """Carga el CSV crudo y guarda una copia inmutable (df_raw) y
        una copia de trabajo (df).

        Nota: `cargar_dataset()` (Fase 2) solo lee el CSV y retorna el DataFrame,
        """
        self.df_raw = cargar_dataset(self.ruta)
        self.df = self.df_raw.copy()
        print(f"  ✓ {self.NOMBRE_ASIGNATURA}: {self.df.shape[0]} filas × "
              f"{self.df.shape[1]} columnas cargadas desde '{self.ruta}'")
        return self.df

    # --------------------------------------------------------
    # 2. EXPLORACIÓN
    # --------------------------------------------------------
    def explorar(self, mostrar_correlaciones: bool = False) -> dict:
        """Ejecuta el diagnóstico completo sobre self.df: resumen general,
        validación de rangos, outliers (IQR) y análisis de G3=0.

        Nota: `resumen_dataset()` (Fase 2) solo imprime y retorna None,
        por lo que el diccionario-resumen se construye aquí directamente
        a partir de self.df (mismas métricas que imprime resumen_dataset).
        """
        print("\nPrimeras filas:")
        print(mostrar_primeras_filas(self.df, n=5))
        #mostrar_primeras_filas(self.df, n=5)
        resumen_dataset(self.df, self.NOMBRE_ASIGNATURA)
        print("\nEstadísticas descriptivas:")
        print(estadisticas_descriptivas(self.df))
        validar_rangos(self.df, self.NOMBRE_ASIGNATURA)
        categorical_cols = ['school', 'sex', 'address', 'famsize', 'Pstatus', 'Mjob', 'Fjob', 'reason', 
                     'guardian', 'schoolsup', 'famsup', 'paid', 'activities', 'nursery', 'higher', 
                     'internet', 'romantic']
        plot_distribucion_categoricas(self.df, categorical_cols, titulo=self.NOMBRE_ASIGNATURA)
        detectar_outliers_iqr(self.df, ['age', 'absences', 'G1', 'G2', 'G3'],
                               self.NOMBRE_ASIGNATURA)
        plot_outliers_boxplot(self.df, columna='absences', titulo=self.NOMBRE_ASIGNATURA)
        #if mostrar_correlaciones:
        analizar_correlaciones(self.df, nombre_dataset=self.NOMBRE_ASIGNATURA)       
        analizar_g3_cero(self.df, self.NOMBRE_ASIGNATURA)
        plot_distribucion_g3(self.df, titulo=self.NOMBRE_ASIGNATURA)

        resumen = {
            'nombre': self.NOMBRE_ASIGNATURA,
            'filas': self.df.shape[0],
            'columnas': self.df.shape[1],
            'duplicados': int(self.df.duplicated().sum()),
            'nulos': int(self.df.isnull().sum().sum()),
            #'muestra filas': mostrar_primeras_filas(self.df, n=5).to_dict(orient='records'),
        }
        return resumen

    # --------------------------------------------------------
    # 3. LIMPIEZA
    # --------------------------------------------------------
    def limpiar(self, percentil_absences: float = 0.95) -> pd.DataFrame:
        """Aplica el pipeline de limpieza (flags + winsorización) sobre self.df."""
        self.df = limpiar_dataset(self.df, self.asignatura)
        self.df = winsorizacion(self.df, 'absences', percentil_absences)
        return self.df

    # --------------------------------------------------------
    # 4. TRANSFORMACIÓN
    # --------------------------------------------------------
    def transformar(self) -> pd.DataFrame:
        """Aplica codificación binaria, One-Hot Encoding y variables derivadas
        sobre self.df, guardando el resultado en self.df_enc.

        Nota: `crear_variables_derivadas()` (Fase 2) genera 'aprobado',
        'progreso_g1_g3', 'nivel_alcohol' y 'edu_familiar_media',
        """
        df_enc = codificar_binarias(self.df)
        df_enc = codificar_ohe(df_enc)
        df_enc = crear_variables_derivadas(df_enc)

   

        self.df_enc = df_enc
        return self.df_enc

    # --------------------------------------------------------
    # 5. VALIDACIÓN
    # --------------------------------------------------------
    def validar(self) -> bool:
        """Valida self.df_enc contra self.df_raw mediante asserts."""
        return validar_dataset_final(self.df_raw, self.df_enc, self.NOMBRE_ASIGNATURA)

    # --------------------------------------------------------
    # 6. EXPORTACIÓN
    # --------------------------------------------------------
    def exportar(self, base_path: str = "../data/processed/F3/") -> None:
        """Exporta self.df (limpio) y self.df_enc (codificado) a data/processed/."""
        exportar_dataset(self.df, base_path + f"student_{self.asignatura}_clean.csv",
                          f"{self.NOMBRE_ASIGNATURA} limpio: flags + winsorización (sin OHE)")
        exportar_dataset(self.df_enc, base_path + f"student_{self.asignatura}_clean_encode.csv",
                          f"{self.NOMBRE_ASIGNATURA} limpio + encoded: flags + winsorización + OHE + variables derivadas")

    # --------------------------------------------------------
    # MÉTODO POLIMÓRFICO — cada clase hija lo implementa distinto
    # --------------------------------------------------------
    def interpretar_resultados(self) -> None:
        """Interpreta las correlaciones de la asignatura con G3.

        Este método se declara aquí como contrato (debe existir en toda
        subclase) pero su implementación concreta varía según la
        asignatura: POLIMORFISMO — mismo nombre de método, comportamiento
        distinto en cada clase hija.
        """
        raise NotImplementedError(
            "interpretar_resultados() debe implementarse en la subclase "
            "correspondiente (PreprocesadorMatematicas / PreprocesadorPortugues)."
        )

    # --------------------------------------------------------
    # MÉTODO DE ALTO NIVEL — orquesta todo el pipeline
    # --------------------------------------------------------
    def ejecutar_pipeline(self, exportar_resultados: bool = True,
                        base_path: str = "../data/processed/F3/") -> bool:
        print(f"\n{'='*60}")
        print(f"  PIPELINE — {self.NOMBRE_ASIGNATURA}  (objeto: {self.__class__.__name__})")
        print(f"{'='*60}")

        pasos = [
            ("cargar",      self.cargar),
            ("explorar",    self.explorar),
            ("limpiar",     self.limpiar),
            ("transformar", self.transformar),
            ("validar",     self.validar),
        ]

        ok = False
        for nombre_paso, metodo in pasos:
            try:
                resultado = metodo()
                if nombre_paso == "validar":
                    ok = resultado
            except Exception as e:
                print(f"\n❌ Pipeline detenido en el paso '{nombre_paso}': {type(e).__name__}: {e}")
                print(f"   Estado del objeto: {repr(self)}")
                return False

        if exportar_resultados:
            try:
                self.exportar(base_path)
            except Exception as e:
                print(f"\n⚠️  Validación exitosa pero falló la exportación: {type(e).__name__}: {e}")

        return ok

    #def __repr__(self) -> str:
     #   n_filas = self.df.shape[0] if self.df is not None else 0
     #   n_cols_enc = self.df_enc.shape[1] if self.df_enc is not None else 0
    #  return (f"<{self.__class__.__name__} asignatura='{self.asignatura}' "
    #            f"filas={n_filas} columnas_encoded={n_cols_enc}>")

    
    def __repr__(self) -> str:
        if self.df is None:
            estado_df = "sin cargar"
        else:
            estado_df = f"{self.df.shape[0]} filas × {self.df.shape[1]} cols"

        if self.df_enc is None:
            estado_enc = "sin transformar"
        else:
            estado_enc = f"{self.df_enc.shape[0]} filas × {self.df_enc.shape[1]} cols"

        return (f"<{self.__class__.__name__} asignatura='{self.asignatura}' "
                f"| df={estado_df} | df_enc={estado_enc}>")

# ============================================================
# CLASES HIJAS — HERENCIA Y POLIMORFISMO
# ============================================================
class PreprocesadorMatematicas(PreprocesadorAsignatura):
    """Especialización de PreprocesadorAsignatura para Matemáticas (student-mat.csv)."""

    NOMBRE_ASIGNATURA = "Matemáticas"

    def __init__(self, ruta: str = "../data/raw/student-mat.csv"):
        # super().__init__ reutiliza el constructor de la clase padre
        super().__init__(ruta=ruta, asignatura='mat')

     
    def interpretar_resultados(self) -> None:
        """Interpretación de las correlaciones con G3 específica de Matemáticas
        (resultados obtenidos en la Fase 2 del proyecto)."""
        print(f"\n{'='*60}")
        print(f"  INTERPRETACIÓN — {self.NOMBRE_ASIGNATURA}")
        print(f"{'='*60}")
        print("""
        Las variables con mayor relación positiva con G3 corresponden a las
        notas de períodos anteriores: G2 (0.90) y G1 (0.80), lo que indica
        que el desempeño previo es el principal predictor del rendimiento final.

        En menor medida, el nivel educativo de la madre (Medu=0.22) y del
        padre (Fedu=0.15) muestran correlaciones positivas débiles.

        La variable con mayor asociación negativa es 'failures' (-0.36):
        los estudiantes con más asignaturas reprobadas previamente tienden
        a obtener notas finales más bajas. Las variables de hábitos (goout,
        Dalc, Walc) presentan asociaciones débiles.
        """)


class PreprocesadorPortugues(PreprocesadorAsignatura):
    """Especialización de PreprocesadorAsignatura para Portugués (student-por.csv)."""

    NOMBRE_ASIGNATURA = "Portugués"

    def __init__(self, ruta: str = "../data/raw/student-por.csv"):
        super().__init__(ruta=ruta, asignatura='por')

    def interpretar_resultados(self) -> None:
        """Interpretación de las correlaciones con G3 específica de Portugués
        (resultados obtenidos en la Fase 2 del proyecto)."""
        print(f"\n{'='*60}")
        print(f"  INTERPRETACIÓN — {self.NOMBRE_ASIGNATURA}")
        print(f"{'='*60}")
        print("""
  Igual que en Matemáticas, las notas previas dominan la correlación
  con G3: G2 (0.92) y G1 (0.83) son los predictores más fuertes.

  A diferencia de Matemáticas, aquí el tiempo de estudio (studytime=0.25)
  y el nivel educativo de la madre (Medu=0.24) tienen un peso algo mayor.

  El consumo de alcohol entre semana (Dalc=-0.20) y fin de semana
  (Walc=-0.18) se asocia negativamente con el rendimiento, más
  marcado que en Matemáticas. 'failures' (-0.39) sigue siendo la
  variable con la correlación negativa más fuerte.
        """)
