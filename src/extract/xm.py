"""
Fuente 1 - API REST de XM (operador del mercado electrico colombiano).
  - Metodo POST con un cuerpo JSON
  - Maximo 30 dias por consulta  ->  pedimos por VENTANAS
  - No requiere usuario ni clave
Documentacion: https://github.com/EquipoAnaliticaXM/API_XM
"""
import pandas as pd

from src import config
from src.utils import guardar_bronce, http_json, log, ventanas, ya_existe


def aplanar(respuesta: dict, periodo: str) -> list:
    """Convierte el JSON anidado de XM en filas planas, SIN cambiar los valores."""
    filas = []
    for item in respuesta.get("Items", []):
        if periodo == "hourly":
            for entidad in item["HourlyEntities"]:
                filas.append({"Date": item["Date"], "Id": entidad["Id"], **entidad["Values"]})
        else:
            for entidad in item["DailyEntities"]:
                filas.append({"Date": item["Date"], "Id": entidad["Id"], "Value": entidad["Value"]})
    return filas


def extraer_metrica(metrica: str, entidad: str, periodo: str, nombre: str, forzar: bool) -> None:
    if ya_existe(nombre, forzar):
        return
    url = config.XM_URL.format(periodo=periodo)
    filas = []
    for inicio, fin in ventanas(config.FECHA_INICIO, config.FECHA_FIN, config.XM_MAX_DIAS):
        cuerpo = {"MetricId": metrica, "Entity": entidad,
                  "StartDate": str(inicio), "EndDate": str(fin), "Filter": []}
        respuesta = http_json("POST", url, json=cuerpo)
        nuevas = aplanar(respuesta, periodo)
        filas.extend(nuevas)
        log(f"   {metrica} {inicio} a {fin}: {len(nuevas)} filas")
    guardar_bronce(pd.DataFrame(filas), nombre, fuente="XM", origen=f"{url} MetricId={metrica}")


def extraer(forzar: bool = False) -> None:
    log("XM - API REST del mercado electrico")
    for metrica, entidad, periodo, nombre in config.XM_METRICAS:
        extraer_metrica(metrica, entidad, periodo, nombre, forzar)


if __name__ == "__main__":
    extraer()
