"""
Fuente 2 - IDEAM en datos.gov.co (plataforma Socrata, lenguaje de consulta SoQL).
  - El dataset tiene MILLONES de observaciones (una cada pocos minutos desde 2005)
  - Por eso FILTRAMOS ($where) y AGREGAMOS ($select + $group) EN EL SERVIDOR:
    viaja un resumen diario por estacion, no millones de filas
  - Ademas paginamos con $limit / $offset por si una ventana trae muchas filas
Documentacion SoQL: https://dev.socrata.com/docs/queries/
"""
import pandas as pd

from src import config
from src.utils import guardar_bronce, http_json, log, ventanas, ya_existe

NOMBRE = "ideam_precipitacion_diaria"
CAMPOS = "codigoestacion, nombreestacion, municipio, latitud, longitud"
PAGINA = 50000


def consulta_soql(inicio, fin, offset: int) -> dict:
    return {
        "$select": f"{CAMPOS}, date_trunc_ymd(fechaobservacion) AS fecha, "
                   f"sum(valorobservado) AS precipitacion_mm, count(*) AS n_obs",
        "$where": f"departamento = '{config.IDEAM_DEPARTAMENTO}' AND "
                  f"fechaobservacion BETWEEN '{inicio}T00:00:00' AND '{fin}T23:59:59'",
        "$group": f"{CAMPOS}, fecha",
        "$order": "fecha, codigoestacion",
        "$limit": PAGINA,
        "$offset": offset,
    }


def extraer(forzar: bool = False) -> None:
    log("IDEAM - datos abiertos (SoQL)")
    if ya_existe(NOMBRE, forzar):
        return
    filas = []
    for inicio, fin in ventanas(config.IDEAM_FECHA_INICIO, config.FECHA_FIN, config.IDEAM_DIAS_VENTANA):
        offset = 0
        while True:                                   # paginacion
            lote = http_json("GET", config.IDEAM_URL, params=consulta_soql(inicio, fin, offset))
            filas.extend(lote)
            if len(lote) < PAGINA:                    # ultima pagina
                break
            offset += PAGINA
        log(f"   semana {inicio} a {fin}: {len(lote)} filas")
    guardar_bronce(pd.DataFrame(filas), NOMBRE, fuente="IDEAM", origen=config.IDEAM_URL)


if __name__ == "__main__":
    extraer()
