"""
Reglas de calidad de la capa plata, escritas con pandera.

Un ESQUEMA es la lista de condiciones que una tabla limpia DEBE cumplir:
que columnas tiene, de que tipo es cada una y que valores acepta.
Si una sola fila no cumple, pandera detiene el programa y dice cual fila
y cual regla fallo. Asi, ningun dato sucio llega a la capa oro.

Uso (desde otro archivo):
    from src.quality.esquemas import ESQUEMA_VENTAS
    ESQUEMA_VENTAS.validate(tabla, lazy=True)
"""
# ---------------------------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------------------------
import pandera.pandas as pa     # pandera: libreria para validar tablas de pandas.
                                # .pandas = la version de pandera para tablas de pandas
from pandera.pandas import Check, Column   # Column: reglas de UNA columna
                                           # Check: una condicion (>= 0, esta en la lista...)

# Valores aceptados en las columnas de categorias
SEGMENTOS = ["Residencial", "Comercial", "Industrial", "No informado"]
TIPOS_COMPRA = ["Bolsa", "Contrato"]

ESQUEMA_VENTAS = pa.DataFrameSchema(
    {
        # periodo: texto con el formato AAAA-MM y un mes entre 01 y 12
        "periodo": Column(str, Check.str_matches(r"^\d{4}-(0[1-9]|1[0-2])$")),
        # divipola: el codigo DANE del municipio, siempre de 5 digitos
        "divipola": Column(str, Check.str_matches(r"^\d{5}$")),
        "municipio": Column(str),                       # nombre oficial del municipio
        "segmento": Column(str, Check.isin(SEGMENTOS)),  # solo los 4 valores aceptados
        "tipo_compra": Column(str, Check.isin(TIPOS_COMPRA)),
        "energia_kwh": Column(float, Check.ge(0)),      # ge = mayor o igual (>= 0)
        "valor_cop": Column(float, Check.ge(0), nullable=True),   # nullable: puede estar vacio
        "clientes": Column(int, Check.ge(0)),
    },
    # unique: no puede haber dos filas con el mismo periodo, municipio, segmento y tipo
    unique=["periodo", "divipola", "segmento", "tipo_compra"],
    strict=True,        # strict: la tabla no puede traer columnas que no esten aqui
)
