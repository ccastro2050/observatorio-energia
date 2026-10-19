"""
Utilidades comunes a todos los extractores:
  - log():            mensajes con hora
  - http_json() / http_texto(): peticiones con REINTENTOS y espera exponencial
  - ya_existe():      idempotencia (no volver a descargar lo que ya esta)
  - guardar_bronce(): guarda en Parquet agregando columnas de LINAJE
"""
import time
from datetime import datetime, timedelta, timezone

import pandas as pd
import requests

from src import config


def log(mensaje: str) -> None:
    print(f"[{datetime.now():%H:%M:%S}] {mensaje}", flush=True)


def _con_reintentos(funcion, descripcion: str):
    """Ejecuta funcion(); si falla, espera 2, 4, 8... segundos y reintenta."""
    for intento in range(1, config.HTTP_REINTENTOS + 1):
        try:
            return funcion()
        except requests.RequestException as error:
            if intento == config.HTTP_REINTENTOS:
                raise RuntimeError(f"Fallo definitivo en {descripcion}: {error}") from error
            espera = 2 ** intento
            log(f"   ! intento {intento} fallo ({type(error).__name__}); reintento en {espera} s")
            time.sleep(espera)


def http_json(metodo: str, url: str, **kwargs):
    """GET o POST que devuelve JSON, con reintentos."""
    def llamar():
        r = requests.request(metodo, url, timeout=config.HTTP_TIMEOUT, **kwargs)
        r.raise_for_status()           # convierte 4xx/5xx en excepcion
        return r.json()
    return _con_reintentos(llamar, f"{metodo} {url}")


def http_texto(url: str) -> str:
    """GET que devuelve texto plano, con reintentos."""
    def llamar():
        r = requests.get(url, timeout=config.HTTP_TIMEOUT)
        r.raise_for_status()
        return r.text
    return _con_reintentos(llamar, f"GET {url}")


def ventanas(inicio, fin, dias: int):
    """Parte el rango [inicio, fin] en bloques de 'dias' dias."""
    a = inicio
    while a <= fin:
        b = min(a + timedelta(days=dias - 1), fin)
        yield a, b
        a = b + timedelta(days=1)


def ruta_bronce(nombre: str):
    return config.DIR_BRONZE / f"{nombre}.parquet"


def ya_existe(nombre: str, forzar: bool) -> bool:
    """Idempotencia: si el archivo ya esta y no se pide forzar, no se descarga."""
    if ruta_bronce(nombre).exists() and not forzar:
        log(f"   = {nombre}.parquet ya existe; se omite (use --forzar para repetir)")
        return True
    return False


def guardar_bronce(df: pd.DataFrame, nombre: str, fuente: str, origen: str) -> None:
    """Guarda TAL CUAL llego + 3 columnas de linaje. En bronce no se limpia nada."""
    df = df.copy()
    df["_fuente"] = fuente                                   # de donde vino
    df["_origen"] = origen                                   # URL o archivo exacto
    df["_extraido_en"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    config.DIR_BRONZE.mkdir(parents=True, exist_ok=True)
    df.to_parquet(ruta_bronce(nombre), index=False)
    log(f"   + {nombre}.parquet guardado: {len(df):,} filas x {df.shape[1]} columnas")
