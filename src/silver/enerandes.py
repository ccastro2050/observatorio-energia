"""
Capa PLATA: limpia la hoja 2023 del Excel de ventas de EnerAndes.

Lee data/bronze/enerandes_ventas_2023.parquet (tal cual llego), aplica las
reglas de limpieza una por una y MIDE cada problema antes y despues.
Luego valida el resultado con pandera (src/quality/esquemas.py) y guarda:
  - data/silver/enerandes_ventas.parquet       las filas limpias
  - data/silver/enerandes_cuarentena.parquet   las filas que no se pueden usar
  - docs/reporte_calidad.md                    la tabla de metricas antes y despues

En bronce no se modifica nada: aqui se trabaja sobre una copia.

Uso:
    python -m src.silver.enerandes
"""
# ---------------------------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------------------------
import unicodedata      # unicodedata: separa una letra de su tilde (para quitar tildes)

import pandas as pd     # pandas: tablas

from src import config                           # rutas de las carpetas
from src.quality.esquemas import ESQUEMA_VENTAS  # las reglas que debe cumplir la tabla limpia
from src.utils import log                        # mensajes con hora

LINAJE = ["_fuente", "_origen", "_extraido_en"]  # columnas que agrego guardar_bronce()

# Encabezados de la hoja 2023 -> nombres estandar de la capa plata
COLUMNAS_2023 = {
    "Fecha": "periodo",
    "Municipio": "municipio",
    "Segmento": "segmento",
    "Tipo_Compra": "tipo_compra",
    "Energia_kWh": "energia_kwh",
    "Valor_COP": "valor_cop",
    "Clientes": "clientes",
}

# Municipio (escrito sin tildes y en minuscula) -> (codigo DIVIPOLA, nombre oficial)
MUNICIPIOS = {
    "medellin": ("05001", "Medellín"),
    "santa fe de antioquia": ("05042", "Santa Fe de Antioquia"),
    "apartado": ("05045", "Apartadó"),
    "bello": ("05088", "Bello"),
    "caldas": ("05129", "Caldas"),
    "caucasia": ("05154", "Caucasia"),
    "copacabana": ("05212", "Copacabana"),
    "envigado": ("05266", "Envigado"),
    "girardota": ("05308", "Girardota"),
    "itagui": ("05360", "Itagüí"),
    "la estrella": ("05380", "La Estrella"),
    "marinilla": ("05440", "Marinilla"),
    "rionegro": ("05615", "Rionegro"),
    "sabaneta": ("05631", "Sabaneta"),
    "turbo": ("05837", "Turbo"),
}
# Otras formas de escribir el mismo municipio -> la forma de la lista de arriba
ALIAS_MUNICIPIO = {
    "rio negro": "rionegro",
    "rionegro (ant)": "rionegro",
    "medellin d.e.": "medellin",
    "sta fe de antioquia": "santa fe de antioquia",
    "santafe de antioquia": "santa fe de antioquia",
}
# Formas de escribir el segmento y el tipo de compra -> valor estandar
SEGMENTOS = {"residencial": "Residencial", "resid.": "Residencial",
             "comercial": "Comercial", "industrial": "Industrial", "ind": "Industrial"}
TIPOS_COMPRA = {"bolsa": "Bolsa", "contrato": "Contrato", "contratos": "Contrato"}


def sin_tildes(texto: str) -> str:
    """'Itagüí' -> 'itagui': minuscula, sin espacios a los lados y sin tildes."""
    # NFD separa cada letra de su tilde ('í' -> 'i' + tilde); luego se quitan las tildes
    letras = unicodedata.normalize("NFD", texto.strip().lower())
    return "".join(c for c in letras if unicodedata.category(c) != "Mn")   # Mn = tilde


def clave_municipio(texto) -> str | None:
    """Convierte cualquier forma de escribir el municipio en la clave de MUNICIPIOS."""
    if pd.isna(texto):
        return None
    clave = sin_tildes(texto)
    return ALIAS_MUNICIPIO.get(clave, clave)   # si es un alias, lo cambia; si no, lo deja


def limpiar(bronce: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, list[dict]]:
    """Aplica las reglas en orden. Devuelve (limpias, cuarentena, metricas)."""
    metricas = []       # una fila del reporte por cada regla

    def medir(problema: str, regla: str, antes: int, despues: int) -> None:
        metricas.append({"problema": problema, "regla aplicada": regla,
                         "antes": antes, "despues": despues})

    df = bronce.drop(columns=LINAJE, errors="ignore")   # sin linaje; si alguna no existe, la ignora

    # Regla 1. La primera fila es el encabezado (se leyo con header=None)
    encabezado = df.iloc[0].tolist()                    # ['Fecha', 'Municipio', ...]
    df = df.iloc[1:].copy()                              # los datos: de la fila 1 en adelante
    df.columns = [COLUMNAS_2023[nombre] for nombre in encabezado]   # nombres estandar
    medir("Encabezado guardado como una fila", "Usarlo como nombres de columna", 1, 0)

    # Regla 2. Filas de totales al final de la hoja: no son ventas
    es_total = df["periodo"].str.upper().str.strip() == "TOTAL"
    medir("Filas de totales", "Eliminarlas", int(es_total.sum()), 0)
    df = df[~es_total]                                   # ~ = negacion: las que NO son total

    # Regla 3. Filas repetidas exactamente iguales
    antes = int(df.duplicated().sum())
    df = df.drop_duplicates()
    medir("Filas duplicadas", "Dejar una sola copia", antes, int(df.duplicated().sum()))

    # Regla 4. Segmento escrito de varias formas o vacio
    antes = df["segmento"].nunique()
    df["segmento"] = df["segmento"].map(lambda s: SEGMENTOS.get(sin_tildes(s)) if pd.notna(s) else None)
    vacios = int(df["segmento"].isna().sum())
    df["segmento"] = df["segmento"].fillna("No informado")
    medir("Segmento escrito de varias formas", "Unificar a 3 valores", antes, df["segmento"].nunique() - 1)
    medir("Segmento vacio", "Marcarlo como 'No informado'", vacios, 0)

    # Regla 5. Tipo de compra escrito de varias formas
    antes = df["tipo_compra"].nunique()
    df["tipo_compra"] = df["tipo_compra"].map(lambda t: TIPOS_COMPRA.get(sin_tildes(t)))
    medir("Tipo de compra escrito de varias formas", "Unificar a Bolsa y Contrato",
          antes, df["tipo_compra"].nunique())

    # Regla 6. Municipio escrito de varias formas: se cambia por su codigo DIVIPOLA
    antes = df["municipio"].nunique()
    claves = df["municipio"].map(clave_municipio)
    df["divipola"] = claves.map(lambda c: MUNICIPIOS[c][0])   # MUNICIPIOS[c] = (codigo, nombre)
    df["municipio"] = claves.map(lambda c: MUNICIPIOS[c][1])
    medir("Municipio escrito de varias formas", "Unificar con el codigo DIVIPOLA",
          antes, df["municipio"].nunique())

    # Regla 7. Los numeros llegaron como texto: se convierten a numero
    for col in ["energia_kwh", "valor_cop", "clientes"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")   # coerce: si no es numero, queda vacio
    df["clientes"] = df["clientes"].astype(int)

    # Regla 8. Energia vacia o negativa: no se puede adivinar -> cuarentena
    malas = df["energia_kwh"].isna() | (df["energia_kwh"] < 0)
    cuarentena = df[malas]
    df = df[~malas]
    medir("Energia vacia o negativa", "Pasar la fila a cuarentena", int(malas.sum()), 0)

    # Regla 9. Valor facturado vacio: se deja vacio (no se inventa un valor)
    vacios = int(df["valor_cop"].isna().sum())
    medir("Valor facturado vacio", "Dejarlo vacio y documentarlo", vacios, vacios)

    orden = ["periodo", "divipola", "municipio", "segmento", "tipo_compra",
             "energia_kwh", "valor_cop", "clientes"]
    return df[orden].reset_index(drop=True), cuarentena, metricas


def escribir_reporte(metricas: list[dict], filas_bronce: int, filas_plata: int, filas_cuarentena: int) -> None:
    """Escribe docs/reporte_calidad.md con la tabla de metricas antes y despues."""
    lineas = [
        "# Reporte de calidad: ventas de EnerAndes (hoja 2023)\n",
        f"- Filas en bronce: {filas_bronce:,}",
        f"- Filas en plata: {filas_plata:,}",
        f"- Filas en cuarentena: {filas_cuarentena:,}\n",
        "| # | Problema | Regla aplicada | Antes | Despues |",
        "|---|---|---|---|---|",
    ]
    for n, m in enumerate(metricas, start=1):    # enumerate: numera desde 1
        lineas.append(f"| {n} | {m['problema']} | {m['regla aplicada']} | {m['antes']} | {m['despues']} |")
    config.DIR_DOCS.mkdir(parents=True, exist_ok=True)
    (config.DIR_DOCS / "reporte_calidad.md").write_text("\n".join(lineas) + "\n", encoding="utf-8")


def main() -> None:
    bronce = pd.read_parquet(config.DIR_BRONZE / "enerandes_ventas_2023.parquet")
    log(f"Bronce: {len(bronce):,} filas")
    limpias, cuarentena, metricas = limpiar(bronce)

    ESQUEMA_VENTAS.validate(limpias, lazy=True)   # si una regla falla, se detiene aqui
    log("Validacion con pandera: OK")             # lazy=True: muestra TODOS los errores juntos

    config.DIR_SILVER.mkdir(parents=True, exist_ok=True)
    limpias.to_parquet(config.DIR_SILVER / "enerandes_ventas.parquet", index=False)
    cuarentena.to_parquet(config.DIR_SILVER / "enerandes_cuarentena.parquet", index=False)
    escribir_reporte(metricas, len(bronce), len(limpias), len(cuarentena))

    print(f"   {'problema':<42}{'antes':>7}{'despues':>9}")
    for m in metricas:
        print(f"   {m['problema']:<42}{m['antes']:>7}{m['despues']:>9}")
    log(f"Plata: {len(limpias):,} filas limpias y {len(cuarentena)} en cuarentena")
    log("Reporte en docs/reporte_calidad.md")


if __name__ == "__main__":
    main()
