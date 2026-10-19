"""
Fuente 4 - Archivo interno de EnerAndes (Excel con una hoja por anio).
  Cada hoja tiene encabezados DISTINTOS y algunas traen un titulo encima.
  Regla de bronce: NO lo arreglamos. Guardamos cada hoja tal cual, como texto,
  incluidas las filas de titulo y la fila TOTAL. Limpiar es trabajo de la capa plata.
"""
import pandas as pd

from src import config
from src.utils import guardar_bronce, log, ya_existe


def extraer(forzar: bool = False) -> None:
    log("EnerAndes - Excel interno")
    archivo = config.ENERANDES_EXCEL
    if not archivo.exists():
        raise FileNotFoundError(f"No se encontro {archivo}. Copielo en data/insumos/.")

    # sheet_name=None -> lee TODAS las hojas y devuelve {nombre_hoja: DataFrame}
    # header=None     -> no interpreta ninguna fila como encabezado (tal cual)
    hojas = pd.read_excel(archivo, sheet_name=None, header=None, dtype=str)
    for nombre_hoja, df in hojas.items():
        nombre = "enerandes_" + nombre_hoja.lower().replace(" ", "_")   # "Ventas 2024" -> enerandes_ventas_2024
        if ya_existe(nombre, forzar):
            continue
        df.columns = [f"col_{i}" for i in range(df.shape[1])]           # Parquet exige nombres de texto
        guardar_bronce(df, nombre, fuente="EnerAndes", origen=f"{archivo.name}#{nombre_hoja}")


if __name__ == "__main__":
    extraer()
