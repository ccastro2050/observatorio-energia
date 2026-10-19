"""
Fuente 3 - NOAA: indice ONI de El Nino (archivo de texto separado por espacios).
  Columnas: SEAS (trimestre movil, ej. JAS), YR (anio), TOTAL (temp. del mar), ANOM (anomalia)
  ANOM >= +0.5  -> El Nino      ANOM <= -0.5 -> La Nina
"""
import io

import pandas as pd

from src import config
from src.utils import guardar_bronce, http_texto, log, ya_existe

NOMBRE = "noaa_oni"


def extraer(forzar: bool = False) -> None:
    log("NOAA - indice ONI (El Nino)")
    if ya_existe(NOMBRE, forzar):
        return
    texto = http_texto(config.NOAA_ONI_URL)
    # sep=r"\s+": uno o mas espacios separan las columnas
    # dtype=str: en bronce guardamos el texto tal cual, sin convertir tipos
    df = pd.read_csv(io.StringIO(texto), sep=r"\s+", dtype=str)
    guardar_bronce(df, NOMBRE, fuente="NOAA", origen=config.NOAA_ONI_URL)


if __name__ == "__main__":
    extraer()
