# Clase AAA – Lunes 26 de octubre y Encuentros Sincrónicos del miércoles 28 de octubre y el miércoles 4 de noviembre de 2026

## Limpiar los datos (capa plata) y organizarlos en un esquema estrella (capa oro)

**Proyecto Integrado IV – Integración de Información (PREICA2602B020037)** · Docente: Carlos Arturo Castro Castro
**Semanas 3 y 4 del reto** *Observatorio Energía y Clima* · Prepara la **Evidencia 2** (vence el miércoles 11 de noviembre)

### ¿De qué trata esta clase?

En la Evidencia 1 guardamos los datos **tal como llegaron**, con todos sus errores, en la capa bronce. Hoy damos los dos pasos siguientes:

1. **Capa plata:** limpiar la hoja 2023 del Excel de EnerAndes con reglas escritas en Python, **medir cada problema antes y después** y comprobar el resultado con **pandera**.
2. **Capa oro:** organizar los datos limpios en un **esquema estrella** (una tabla de hechos rodeada de dimensiones) con **dbt**, la herramienta que usa la industria para transformar datos con SQL.

| Término | En palabras sencillas |
|---|---|
| **Capa plata** | La carpeta donde quedan los datos **ya limpios**: sin duplicados, con los nombres unificados y los números como números. Se construye a partir de bronce, que no se toca. |
| **Calidad de datos** | Qué tan confiables son los datos para tomar decisiones. Se mide con números: "32 filas duplicadas → 0". |
| **Capa oro** | Los datos limpios organizados para responder preguntas de negocio y alimentar el dashboard. Aquí: un **esquema estrella** dentro de una base de datos DuckDB. |

> **Resultado de la clase:** cada equipo termina con la hoja 2023 limpia en `data/silver/`, un **reporte de calidad** con 9 reglas medidas antes y después, **6 pruebas automáticas** de esas reglas con pytest, y un **esquema estrella** de 4 tablas creado con un comando de dbt que además ejecuta **13 pruebas automáticas**.

> **Cómo está organizada esta guía:** la clase tiene **5 partes**, numeradas del 0 al 4. Cada parte empieza con sus **conceptos clave**, y luego trae el código completo, el comando para ejecutarlo y el resultado esperado, con una tabla que explica cada parte del resultado.

> ✅ **Todo este paso a paso se probó el 25 de octubre y el 4 de noviembre de 2026 en Windows 11 con Python 3.14, pandera 0.35 y dbt 1.12.** Las salidas que aparecen aquí son las reales. El proyecto completo y funcionando está en la carpeta `observatorio-energia/`, al lado de este archivo.

---

## Mapa de la clase

| Parte de la clase | Concepto clave | Comando que lo demuestra |
|---|---|---|
| 0. Preparar el proyecto **(en paralelo con la Parte 1)** | Rama nueva, archivos nuevos y librerías nuevas | `pip install -r requirements.txt` |
| 1. Conceptos | Calidad de datos, capa plata, modelo dimensional | — |
| 2. Capa plata | Reglas de limpieza, métricas antes y después, cuarentena, pandera y pruebas con pytest | `python -m src.silver.enerandes` y `python -m pytest -v` |
| 3. Capa oro con dbt | Hechos, dimensiones, grano, pruebas de dbt | `dbt build --project-dir dbt --profiles-dir dbt` |
| 4. Equipo y Evidencia 2 | Commit, Pull Request y lo que el equipo agrega | `git push` → PR → merge |

## Resumen de los pasos

| # | Sección | Qué se hace | ¿Para qué? | Resultado esperado | Qué significa el resultado |
|---|---|---|---|---|---|
| 1 | 0.1 | `git switch main`, `git pull` y `git switch -c feature/plata-oro` | Partir de la última versión del repositorio del equipo, en una rama nueva. | `Switched to a new branch 'feature/plata-oro'` | Los cambios de hoy no tocan `main` hasta el Pull Request. |
| 2 | 0.2 | Crear las carpetas `src/silver/`, `src/quality/` y `dbt/models/` | Preparar dónde van los archivos de hoy. Cada archivo se crea en su sección, pegando el código de la guía. | Las carpetas en el EXPLORER de VS Code. | El proyecto está listo para la capa plata y la capa oro. |
| 3 | 0.3 | Agregar 2 líneas a `src/config.py`, 2 a `requirements.txt` y 3 a `.gitignore` | Rutas nuevas, librerías nuevas y archivos que no se suben. | — | La configuración queda lista. |
| 4 | 0.4 | `pip install -r requirements.txt` | Instalar pandera y dbt. | `Successfully installed ... dbt-duckdb-1.11.1 ... pandera-0.35.0 ...` | Las librerías nuevas quedaron en `.venv`. |
| 5 | 0.4 | `dbt --version` | Comprobar que dbt funciona. | `installed: 1.12.6` y el plugin `duckdb: 1.11.1` | dbt y su conexión con DuckDB están listos. |
| 6 | 2.4 | `python -m src.silver.enerandes` | Limpiar la hoja 2023. | Tabla de 9 problemas con su valor antes y después; `Plata: 1,064 filas limpias y 16 en cuarentena`. | La hoja quedó limpia, validada con pandera, y el reporte quedó en `docs/reporte_calidad.md`. |
| 7 | 2.5 | Ver la cuarentena con `python -c "..."` | Revisar qué filas se apartaron y por qué. | 16 filas con energía vacía (`NaN`) o negativa. | Ninguna fila se borra sin dejar rastro. |
| 8 | 2.6 | Probar pandera con datos malos | Ver qué pasa cuando una regla falla. | `SchemaErrors` con `CONTRATOS, bolsa` y `-500.0` | pandera detiene el programa y dice qué columna y qué valor fallaron. |
| 9 | 2.7 | `python -m pytest -v` | Probar el código de las reglas de limpieza. | `6 passed` | Cada regla hace lo que debe. |
| 10 | 2.8 | Borrar `"resid."` de `SEGMENTOS` y ejecutar `python -m pytest` | Ver para qué sirve una prueba. | `1 failed, 5 passed` y `assert 'No informado' == 'Residencial'` | La prueba detecta un error que pandera no ve. Luego se vuelve a poner la regla. |
| 11 | 2.9 | Escribir `test_total_en_minuscula_tambien_se_elimina` en `tests/test_limpieza.py` | Aprender a escribir una prueba nueva: preparar, ejecutar y comprobar. | — | El archivo tiene 7 pruebas. |
| 12 | 2.9 | `python -m pytest -v -k minuscula` | Ejecutar solo la prueba nueva. | `1 passed, 6 deselected` | La prueba nueva pasa: la regla 2 también quita `total` en minúscula. |
| 13 | 2.9 | `python -m pytest` | Ejecutar todas antes del commit. | `7 passed` | Lo nuevo no dañó nada. |
| 14 | 3.6 | `dbt build --project-dir dbt --profiles-dir dbt` | Crear el esquema estrella y probarlo. | `Done. PASS=18 WARN=0 ERROR=0` | Se crearon 1 vista y 4 tablas, y pasaron las 13 pruebas. |
| 15 | 3.7 | `dbt show --inline "..."` | Consultar el modelo con SQL. | Energía por segmento: Residencial 309,7 GWh… | El esquema estrella responde preguntas de negocio. |
| 16 | 4.1 | `git add`, `git commit`, `git push` y Pull Request | Llevar el trabajo al repositorio del equipo. | El PR aprobado y unido a `main`. | El código base de la EA2 queda en `main` para todo el equipo. |

---

## Parte 0 · Preparar el proyecto (en paralelo con la Parte 1)

Se trabaja sobre el **repositorio del equipo** de la Evidencia 1: el que tiene la capa bronce funcionando.

### 0.1 Una rama nueva para el trabajo de hoy

En VS Code, abran la carpeta del repositorio (**Archivo → Abrir carpeta**) y abran la terminal con **Ctrl + ñ**. Escriban los comandos **uno por uno**, con Enter después de cada uno.

**1. Activar el entorno virtual:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Resultado:**

```text
(.venv) PS C:\clases\observatorio-energia>
```

| Parte | Qué significa |
|---|---|
| `.venv` | La carpeta del entorno virtual del proyecto: ahí están instaladas las librerías (pandas, duckdb…). |
| `Scripts\Activate.ps1` | El programa que activa el entorno virtual en PowerShell. |
| `(.venv)` al inicio de la línea | El entorno virtual está activo: `python`, `pip` y `dbt` usan las librerías del proyecto. |

> ⚠️ Si la terminal se cierra o se abre una nueva, hay que activar el entorno otra vez.

**2. Pasarse a la rama principal:**

```powershell
git switch main
```

**Resultado:**

```text
Already on 'main'
Your branch is up to date with 'origin/main'.
```

| Parte | Qué significa |
|---|---|
| `git switch main` | Se pasa a la rama principal, `main`. |
| `Already on 'main'` | Ya estaba en `main`: no tuvo que cambiar. |
| `Your branch is up to date with 'origin/main'` | Su copia de `main` está igual a la última versión que el computador conoce de GitHub (`origin`). |

**3. Traer los últimos cambios del equipo:**

```powershell
git pull
```

**Resultado:**

```text
Already up to date.
```

| Parte | Qué significa |
|---|---|
| `git pull` | Trae de GitHub los cambios que subieron los compañeros y los une a su copia. |
| `Already up to date.` | No había cambios nuevos en GitHub. Si los hay, aparece la lista de archivos que cambiaron. |

**4. Crear la rama de hoy:**

```powershell
git switch -c feature/plata-oro
```

**Resultado:**

```text
Switched to a new branch 'feature/plata-oro'
```

| Parte | Qué significa |
|---|---|
| `-c` | *create*: crea la rama antes de pasarse a ella. |
| `feature/plata-oro` | El nombre de la rama: `feature/` indica que es una funcionalidad nueva; `plata-oro`, las capas de hoy. |
| `Switched to a new branch 'feature/plata-oro'` | La rama se creó y ya están en ella: todo lo que hagan hoy queda aquí, sin tocar `main`. |

> 💡 **Opcional: su nombre en la rama.** Si quieren, pueden agregarle su nombre, por ejemplo `git switch -c feature/ana_perez_plata-oro`; así el equipo ve de un vistazo de quién es cada rama. No es obligatorio: `feature/plata-oro` también está bien. Si usan otro nombre, escríbanlo en lugar de `feature/plata-oro` en los comandos que lo piden más adelante (`git push -u origin ...` y `git merge ...`).

### 0.2 Crear las carpetas nuevas

Hoy **cada uno crea los archivos nuevos en su repositorio**. En este paso solo se crean las **carpetas**; cada archivo se crea más adelante, en la sección donde se explica, pegando el código que trae la guía.

En el EXPLORER de VS Code (panel de la izquierda), con los botones **Nueva carpeta** y **Nuevo archivo**, creen:

| Qué crear | Dónde | Para qué |
|---|---|---|
| Carpeta `silver` | dentro de `src/` | La capa plata: la limpieza |
| Archivo `__init__.py` **vacío** | dentro de `src/silver/` | Le dice a Python que la carpeta es un paquete: así funciona `python -m src.silver.enerandes` |
| Carpeta `quality` | dentro de `src/` | Las reglas de calidad con pandera |
| Archivo `__init__.py` **vacío** | dentro de `src/quality/` | Igual que el anterior |
| Carpeta `dbt` | en la raíz del proyecto | La capa oro |
| Carpetas `models/staging` y `models/marts` | dentro de `dbt/` | Los modelos de dbt: la entrada y las tablas finales |
| Carpeta `tests` | en la raíz, **solo si no existe** | Las pruebas automáticas |

**¿Por qué esos nombres?**

| Nombre | Por qué se llama así | ¿Es obligatorio? |
|---|---|---|
| `silver` | *Plata* en inglés. Es la segunda capa: bronce (sin tocar) → **plata** (limpio) → oro (listo para el negocio). Como las medallas: cada una vale más que la anterior. | No: es la costumbre de la **arquitectura medallón**, la forma más usada en la industria para organizar un proyecto de datos por capas. |
| `quality` | *Calidad* en inglés: aquí van las reglas de calidad de los datos. | No: es un nombre que elegimos para el proyecto. |
| `models` | *Modelos* en inglés. En dbt, cada archivo `.sql` **modela** una tabla: describe cómo debe quedar. | **Sí**: dbt busca los modelos en la carpeta que dice `dbt_project.yml`, y ahí está escrito `models`. |
| `staging` | *Zona de preparación* en inglés. Como el andén de una bodega, donde la mercancía **llega y se recibe** antes de acomodarla: aquí los datos de plata **entran** a dbt sin cambiarlos. | No: es una **costumbre de la industria**; casi todos los proyectos de dbt la usan. |
| `marts` | De *data mart*, "tienda de datos". Como la **vitrina** de una tienda, donde está lo que ya está listo para que el cliente lo use: aquí quedan las tablas finales del esquema estrella, listas para el dashboard. | No: también es una **costumbre de la industria**. |

```text
plata (data/silver) → staging (llega) → marts (se exhibe) → dashboard
```

> ⚠️ **`staging` y `marts` van DENTRO de `models`**, no al lado. dbt solo busca los `.sql` en la carpeta `models` (así lo dice `model-paths: ["models"]` en `dbt_project.yml`). `staging` y `marts` son solo una forma de **ordenar** los modelos dentro de `models`, como subcarpetas de una misma gaveta. Si quedan al lado de `models`, dbt no los ve: no crea las tablas y tampoco da error.

> ⚠️ **No toquen `src/config.py`, `requirements.txt` ni `.gitignore`**: su equipo ya los cambió en la Evidencia 1 (fechas, métricas, fuente propia). En el paso 0.3 se les **agregan** líneas.

> 💡 En la carpeta de Drive **`04_Clase_26_oct_4_nov_Calidad_Modelo/observatorio-energia`** está el proyecto de la clase ya terminado. Úsenlo solo para **comparar** si algo no les funciona.

Al terminar la clase, el proyecto queda así (lo nuevo está marcado con ✨; los archivos se crean en las secciones 2.2, 2.3, 2.7 y en la Parte 3):


```text
observatorio-energia/
├── dbt/                                ✨ capa oro: crea el esquema estrella
│   ├── dbt_project.yml                 # nombre del proyecto y tipo de modelos
│   ├── profiles.yml                    # conexión: el archivo DuckDB
│   └── models/                         # cada .sql es una tabla o una vista
│       ├── staging/                    # entrada: lee la capa plata
│       │   ├── sources.yml             # dónde están los Parquet de plata
│       │   └── stg_ventas.sql          # lectura de las ventas limpias
│       └── marts/                      # las tablas del esquema estrella
│           ├── dim_mes.sql             # dimensión: un mes por fila
│           ├── dim_municipio.sql       # dimensión: un municipio (DIVIPOLA)
│           ├── dim_segmento.sql        # dimensión: un segmento por fila
│           ├── fact_ventas_mensual.sql # hechos: las ventas y sus medidas
│           └── schema.yml              # pruebas y descripción de las tablas
├── src/
│   ├── extract/                        # (Evidencia 1) extractores de bronce
│   ├── quality/                        ✨ reglas de calidad
│   │   ├── __init__.py                 # vacío: la carpeta es un paquete
│   │   └── esquemas.py                 # esquema de pandera de la tabla limpia
│   ├── silver/                         ✨ capa plata
│   │   ├── __init__.py                 # vacío: la carpeta es un paquete
│   │   └── enerandes.py                # limpia la hoja 2023 y mide cada regla
│   ├── config.py                       # (+2 líneas) rutas de plata y docs
│   └── ...                             # demás archivos de la Evidencia 1
├── tests/                              # pruebas automáticas con pytest
│   ├── ...                             # las pruebas de la Evidencia 1
│   └── test_limpieza.py                ✨ pruebas de las reglas de limpieza
├── requirements.txt                    # (+2 o 3 líneas) pandera, dbt, pytest
└── .gitignore                          # (+4 líneas) lo de dbt que no se sube
```

### 0.3 Agregar las líneas nuevas

**En `src/config.py`**, debajo de la línea de `DIR_BRONZE`, agreguen:

```python
DIR_SILVER = RAIZ / "data" / "silver"       # capa plata: los datos ya limpios
DIR_DOCS = RAIZ / "docs"                    # documentacion: perfilamiento, reporte de calidad
```

**Al final de `requirements.txt`**, agreguen:

```text
pandera>=0.30
dbt-duckdb>=1.9
pytest>=8
```

(Si `pytest` ya está en `requirements.txt` desde la Evidencia 1, no lo repitan).

**Al final de `.gitignore`**, agreguen:

```text
# Archivos que genera dbt al ejecutarse (se regeneran con dbt build)
dbt/target/
dbt/logs/
dbt/.user.yml
```

| Línea | Para qué |
|---|---|
| `DIR_SILVER` | La carpeta donde se guardan los datos limpios. Ya está en `.gitignore` (`data/silver/`): no se sube a GitHub. |
| `DIR_DOCS` | La carpeta `docs/`, donde se escribe el reporte de calidad. |
| `pandera` | La librería que valida las tablas limpias. |
| `dbt-duckdb` | dbt y su conexión con DuckDB. Instala también `dbt-core`. |
| `pytest` | La librería que ejecuta las pruebas automáticas. |
| `dbt/target/` y `dbt/logs/` | Carpetas que dbt crea cada vez que se ejecuta. Se regeneran solas: no se suben. |
| `dbt/.user.yml` | Un archivo que dbt crea la primera vez, con un número que identifica al computador. Es de cada persona: no se sube. |

> 💡 El archivo de la capa oro, `data/observatorio.duckdb`, tampoco se sube: la línea `*.duckdb` ya estaba en `.gitignore` desde la Evidencia 1.

### 0.4 Instalar las librerías nuevas

En `requirements.txt` ya están pandera, dbt-duckdb y pytest, pero todavía no están instaladas. Este comando lee la lista e instala en `.venv` lo que falte:

```powershell
pip install -r requirements.txt
```

| Parte | Qué significa |
|---|---|
| `pip` | El programa de Python que descarga e instala librerías. |
| `install` | La orden de instalar. |
| `-r requirements.txt` | *read*: lee las librerías de ese archivo, en lugar de escribirlas una por una. Las que ya están instaladas (pandas, duckdb…) las salta. |

Tarda de 1 a 3 minutos: dbt trae muchas dependencias. **Resultado** (las últimas líneas, recortadas):

```text
Installing collected packages: text-unidecode, pytz, ... dbt-core, dbt-duckdb
Successfully installed ... dbt-core-1.12.6 ... dbt-duckdb-1.11.1 ... pandera-0.35.0 ... pytest-9.1.1 ...

[notice] A new release of pip is available: 25.2 -> 26.2.2
[notice] To update, run: python.exe -m pip install --upgrade pip
```

| Lo que aparece | Qué significa |
|---|---|
| `Using cached ...` / `Downloading ...` | Cada librería que necesita: *cached* si ya estaba descargada en el computador, *Downloading* si la baja de internet. |
| `Installing collected packages: ...` | La lista de librerías que va a instalar: las tres nuevas y las que ellas necesitan (sus *dependencias*). |
| `Successfully installed ...` | Todo quedó instalado, con la versión de cada librería. |
| `[notice] A new release of pip is available` | Solo un aviso: hay una versión nueva de `pip`. No es un error y no hay que hacer nada. |

Comprueben que dbt funciona. Este comando muestra la versión de dbt y la de su conexión con DuckDB; si responde, dbt está listo:

```powershell
dbt --version
```

| Parte | Qué significa |
|---|---|
| `dbt` | El programa que se acaba de instalar en `.venv`. |
| `--version` | Le pide que muestre su versión, sin hacer nada más. |

**Resultado:**

```text
Core:
  - installed: 1.12.6
  - latest:    1.12.6 - Up to date!

Plugins:
  - duckdb: 1.11.1 - Up to date!


21:21:42  dbt v2 is available, and is the default for new installations. This is dbt Core v1.
          New project - install v2: https://docs.getdbt.com/docs/local/install-dbt?utm_source=dbt-cli
          Existing v1 project - upgrade guide: https://docs.getdbt.com/docs/dbt-versions/dbt-upgrade/upgrading-to-v2?utm_source=dbt-cli
```

| Lo que aparece | Qué significa |
|---|---|
| `Core: installed: 1.12.6` | dbt está instalado, en la versión 1.12.6. |
| `latest: 1.12.6 - Up to date!` | Es la versión más nueva de dbt Core v1. |
| `Plugins: duckdb: 1.11.1` | dbt sabe trabajar con DuckDB (el *adaptador*). |
| `dbt v2 is available...` | Solo un aviso: existe una versión 2 de dbt, que es otro producto. En el curso se usa **dbt Core v1**. No hay que instalar nada ni seguir esos enlaces. |

> ⚠️ **Si sale `dbt : El término 'dbt' no se reconoce...`:** el entorno virtual no está activo. Ejecuten `.\.venv\Scripts\Activate.ps1` y repitan.

> ⚠️ **La capa plata parte de la capa bronce.** Si en su computador no está el archivo `data/bronze/enerandes_ventas_2023.parquet`, créenlo con `python -m src.extract.enerandes` (lee el Excel; no necesita internet).

---

## Parte 1 · Conceptos

### De bronce a plata y a oro

![Las tres capas: bronce, plata y oro, con lo que tiene cada una en esta clase](img/capas_bronce_plata_oro.png)

| Capa | ¿Se modifica? | Qué se hace | Qué no se hace |
|---|---|---|---|
| Bronce | **No se modifica nada** | Guardar el original | Corregir errores |
| Plata | Es una **copia** que se corrige | Quitar duplicados, unificar nombres, convertir tipos, apartar lo que no sirve | Inventar datos que no existen |
| Oro | Se **reorganiza** | Separar hechos y dimensiones para analizar | Volver a limpiar: eso ya se hizo en plata |

### ¿Qué es la calidad de datos?

Es **qué tan confiables son los datos para tomar decisiones**. Por ejemplo, en el Excel Medellín está escrito de 5 formas (`Medellín`, `Medellin`, `medellin`, `Medellín D.E.` y `"Medellín "` con un espacio al final). Un tablero hecho con esos datos mostraría a Medellín **5 veces**, como si fueran 5 municipios distintos, cada uno con una parte de las ventas. La gerencia vería menos ventas en Medellín de las que hubo de verdad y tomaría decisiones con números falsos.

La guía de referencia de la gestión de datos, el **DAMA-DMBOK**, organiza la calidad en **dimensiones**. Cada problema del Excel cae en una de ellas:

| Dimensión | Pregunta que responde | Problema real en la hoja 2023 |
|---|---|---|
| **Unicidad** | ¿Cada hecho está una sola vez? | 32 filas duplicadas |
| **Consistencia** | ¿El mismo dato se escribe siempre igual? | Medellín de 5 formas; el segmento de 6 formas |
| **Completitud** | ¿Están todos los datos? | 14 ventas sin segmento; 9 sin energía |
| **Validez** | ¿Los valores son posibles y tienen el formato correcto? | 7 ventas con energía negativa; una fila `TOTAL` que no es una venta |
| **Exactitud** | ¿El dato corresponde a la realidad? | (se revisa contra otra fuente; por ejemplo, el municipio contra DIVIPOLA) |
| **Oportunidad** | ¿El dato llega a tiempo? | El IDEAM publica con unos 2,5 meses de rezago |

### Conceptos clave de la capa plata

| Concepto | Qué es | Ejemplo en la clase |
|---|---|---|
| **Regla de limpieza** | Una corrección escrita en código, que se aplica igual cada vez que se ejecuta. | "Unificar el segmento: `RESID.` → `Residencial`". |
| **Métrica antes y después** | El número que mide un problema antes y después de aplicar la regla. Es la prueba de que la regla funcionó. | "Filas duplicadas: 32 → 0". |
| **Cuarentena** | Un archivo aparte con las filas que **no se pueden usar** ni corregir. No se borran: se apartan, para revisarlas con el dueño de los datos. | Las 16 ventas con energía vacía o negativa. |
| **Esquema de validación** | La lista de condiciones que la tabla limpia **debe** cumplir. Si una falla, el programa se detiene. | "`tipo_compra` solo puede ser Bolsa o Contrato". |
| **pandera** | Una librería de Python que valida tablas de pandas contra un esquema. | `ESQUEMA_VENTAS.validate(tabla)` |
| **DIVIPOLA** | La codificación oficial de los municipios de Colombia, del DANE. Cada municipio tiene un código de 5 dígitos. | Medellín = `05001`. |

**Las palabras de pandera.** Para escribir las reglas se importan algunas palabras de pandera. En la clase se usan dos; se pueden importar más en la misma línea, separadas por comas:

```python
# Lo que se usa en la clase:
from pandera.pandas import Check, Column

# Con tres mas que vale la pena conocer:
from pandera.pandas import Check, Column, DataFrameSchema, check_output, infer_schema
```

| Nombre | Para qué sirve | Ejemplo | ¿Se usa en la clase? |
|---|---|---|---|
| `Check` | Una condición. | `Check.ge(0)`: mayor o igual a 0, así que `-500` no pasa. `Check.isin(["Bolsa", "Contrato"])`: debe estar en la lista, así que `bolsa` no pasa. | Sí |
| `Column` | Las reglas de una columna: su tipo y sus condiciones. | `Column(float, Check.ge(0))`: número con decimales, mayor o igual a 0. | Sí |
| `DataFrameSchema` | Crear el esquema: el paquete con todas las reglas. | `DataFrameSchema({"energia_kwh": Column(float, Check.ge(0))})`: un esquema con una sola columna. | Sí, pero escrito `pa.DataFrameSchema`. Si se importa en esta línea, se escribe sin el `pa.` |
| `check_output` | Revisar automáticamente la tabla que **devuelve** una función, sin escribir `validate`. | `@check_output(ESQUEMA_VENTAS)` encima de `def limpiar(...)`: cada vez que `limpiar()` termina, pandera revisa la tabla que devolvió. | No |
| `infer_schema` | pandera **adivina** el esquema mirando una tabla: qué columnas tiene y de qué tipo es cada una. Las condiciones (`Check`) las agrega uno después. Sirve como punto de partida con una fuente nueva, por ejemplo XM o IDEAM. | `infer_schema(limpias)` propone: `energia_kwh` es `float64` y `segmento` es texto. | No |

Así se usaría cada una de las tres:

```python
# 1. DataFrameSchema: igual que en la clase, pero sin "pa."
ESQUEMA_VENTAS = DataFrameSchema({
    "energia_kwh": Column(float, Check.ge(0)),
})

# 2. check_output: se pone encima de la funcion, con @
@check_output(ESQUEMA_VENTAS)     # cada vez que la funcion termine, pandera revisa lo que devuelve
def limpiar(bronce):
    ...
    return df

# 3. infer_schema: pandera mira la tabla y propone reglas
print(infer_schema(limpias))      # muestra las columnas que encontro y el tipo de cada una
```

> 💡 `Check`, `Column`, `DataFrameSchema`... son palabras **de pandera**: hay que escribirlas tal cual. `ESQUEMA_VENTAS`, `SEGMENTOS` o `limpias` son nombres que **inventamos nosotros**: se pueden cambiar, siempre que se cambien en todos los lugares donde se usan.

> 🔑 **La regla de oro de la capa plata: no se inventa nada.** Lo que se puede corregir con certeza, se corrige (`Medellin` → `Medellín`). Lo que no, se marca (`No informado`) o se aparta en cuarentena (energía negativa). Y todo se mide.

### Conceptos clave de la capa oro (modelo dimensional)

El modelo dimensional lo propuso **Ralph Kimball** en los años 90 y es la forma estándar de organizar datos para inteligencia de negocios. Separa **lo que se mide** de **cómo se mira**.

| Concepto | Qué es | Ejemplo en la clase |
|---|---|---|
| **Tabla de hechos** | Guarda los **eventos que se miden**, con sus números (*medidas*). Tiene muchas filas. | `fact_ventas_mensual`: energía, valor y clientes de cada venta. |
| **Medida** | Un número del hecho que se puede sumar o promediar. | `energia_kwh`, `valor_cop`. |
| **Dimensión** | Describe el **contexto** del hecho: cuándo, dónde, quién. Se usa para filtrar y agrupar. Tiene pocas filas. | `dim_mes`, `dim_municipio`, `dim_segmento`. |
| **Llave** | La columna que identifica cada fila de una dimensión y que el hecho usa para apuntarle. | `municipio_id = '05001'`. |
| **Grano** | Qué representa **una fila** de la tabla de hechos. Es la decisión más importante del modelo. | Un mes, un municipio, un segmento y un tipo de compra. |
| **Esquema estrella** | El hecho en el centro y las dimensiones alrededor, cada una unida al hecho por su llave. | El diagrama de abajo. |

![Esquema estrella de las ventas de EnerAndes: la tabla de hechos en el centro y tres dimensiones alrededor](img/esquema_estrella_ventas.png)

**Cómo se lee:**

| Elemento del diagrama | Qué significa |
|---|---|
| Caja naranja | La **tabla de hechos**: las ventas, con sus medidas. |
| Cajas azules | Las **dimensiones**: el mes, el municipio y el segmento. |
| `PK` | **Llave primaria** (*primary key*): identifica cada fila de la dimensión. No se repite. |
| `FK` | **Llave foránea** (*foreign key*): la columna del hecho que apunta a la llave primaria de una dimensión. |
| Línea con `1` y `N` | **Un** mes (o municipio, o segmento) aparece en **muchas** ventas. Es una relación **uno a muchos**. |
| `medida` | Un número que se suma o se promedia. |

### ¿Qué es dbt?

**dbt** (*data build tool*) es una herramienta para **transformar datos con SQL**, muy usada en la industria. Cada tabla del modelo se escribe como un archivo `.sql` con un `select`. dbt:

| Qué hace dbt | Cómo se ve en el proyecto |
|---|---|
| Crea cada tabla a partir de su `select` | `dim_mes.sql` → tabla `dim_mes` en DuckDB |
| Las crea **en el orden correcto**, porque sabe cuál depende de cuál | `{{ ref('stg_ventas') }}` le dice que `dim_mes` necesita primero a `stg_ventas` |
| Ejecuta **pruebas** sobre las tablas | `unique`, `not_null`, `relationships` en `schema.yml` |
| Deja todo **versionado** en Git, como cualquier código | La carpeta `dbt/` va en el repositorio |

| Tarea | ¿Con qué se hace? | ¿Por qué? |
|---|---|---|
| Limpiar el Excel (capa plata) | Python + pandas + pandera | Hay que leer texto sucio, quitar tildes y decidir fila por fila: Python lo hace mejor. |
| Construir el modelo (capa oro) | dbt + SQL | Son uniones y agrupaciones de tablas ya limpias: SQL lo hace mejor, y dbt lo organiza y lo prueba. |

---

## Parte 2 · Capa plata: limpiar la hoja 2023

### Idea central

El programa lee la hoja 2023 de bronce, aplica **9 reglas en orden**, mide cada problema antes y después, valida el resultado con pandera y guarda tres cosas: las filas limpias, las filas en cuarentena y el reporte de calidad.

### 2.1 Lo que hay que limpiar

En la Evidencia 1 vimos los problemas de la hoja 2023 con el perfilamiento. Esta es la lista de reglas que se van a aplicar, en orden:

| # | Problema (perfilamiento) | Regla | Dimensión de calidad |
|---|---|---|---|
| 1 | El encabezado quedó guardado como la primera fila | Usarlo como nombres de columna | Validez |
| 2 | Una fila `TOTAL` al final, que no es una venta | Eliminarla | Validez |
| 3 | 32 filas duplicadas | Dejar una sola copia | Unicidad |
| 4 | Segmento escrito de 6 formas | Unificar a Residencial, Comercial e Industrial | Consistencia |
| 5 | 14 ventas sin segmento | Marcarlas como `No informado` | Completitud |
| 6 | Tipo de compra escrito de 4 formas | Unificar a Bolsa y Contrato | Consistencia |
| 7 | Municipio escrito de 31 formas | Unificar con el código DIVIPOLA | Consistencia |
| 8 | Energía vacía o negativa | Pasar la fila a cuarentena | Completitud y validez |
| 9 | Valor facturado vacío | Dejarlo vacío y documentarlo | Completitud |

> 💡 **¿Por qué el orden importa?** Los duplicados (regla 3) se buscan **antes** de unificar los nombres. Si se unificara primero, una fila con `Medellin` y otra con `Medellín` se volverían iguales, y se contaría como duplicado algo que el perfilamiento no midió así.

### 2.2 Las reglas de calidad: `src/quality/esquemas.py`

Este archivo dice **cómo debe quedar** la tabla limpia. No limpia nada: solo comprueba.

**¿Quién pone las reglas?** **Nosotros.** pandera no inventa ninguna regla ni las saca de ningún lado: solo trae las **palabras** para escribirlas (`Column`, `Check`, `isin`, `ge`...) y después las aplica. Es como una fórmula de Excel: en `=SUMA(A1:A10)` la idea de sumar es de usted, y `SUMA` es una palabra de Excel.

Las reglas salen de **lo que sabemos del negocio**:

| Lo que sabemos de EnerAndes | Cómo se escribe con palabras de pandera |
|---|---|
| La energía solo se compra en bolsa o por contrato | `Check.isin(["Bolsa", "Contrato"])` |
| No existe energía negativa | `Check.ge(0)` |
| El código DIVIPOLA de un municipio tiene 5 dígitos (`05001` = Medellín) | `Check.str_matches(r"^\d{5}$")` |
| No puede haber dos ventas iguales del mismo mes, municipio, segmento y tipo | `unique=[...]` |

Lo que no esté escrito en este archivo, pandera **no** lo revisa.

**Creen el archivo `src/quality/esquemas.py` y peguen este código:**

```python
"""
Reglas de calidad de la capa plata, escritas con pandera.

Un ESQUEMA es la lista de condiciones que una tabla limpia DEBE cumplir:
que columnas tiene, de que tipo es cada una y que valores acepta.
Si una sola fila no cumple, pandera detiene el programa y dice cual fila
y cual regla fallo. Asi, ningun dato sucio llega a la capa oro.

Este archivo SOLO GUARDA las reglas: no revisa nada por si solo.
Quien las usa es OTRO archivo: src/silver/enerandes.py (la limpieza).
Ese archivo, despues de limpiar, escribe estas dos lineas:

    from src.quality.esquemas import ESQUEMA_VENTAS
    ESQUEMA_VENTAS.validate(limpias, lazy=True)

  - La primera trae las reglas de este archivo (la variable ESQUEMA_VENTAS).
  - La segunda revisa la tabla limpia con esas reglas.
    Si una regla falla, el programa se detiene y la tabla NO se guarda.
    lazy=True: revisa toda la tabla y muestra TODOS los errores juntos
    (sin lazy=True, se detiene en el primer error y no se sabe si hay mas).

Las reglas van en un archivo aparte para escribirlas una sola vez:
las usan la limpieza (enerandes.py) y las pruebas (tests/).
"""
# ---------------------------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------------------------
# pandera: libreria para revisar que una tabla de pandas cumpla reglas.
# .pandas es la parte de pandera para tablas de pandas; "as pa" le da el nombre corto pa
import pandera.pandas as pa
# Column: las reglas de UNA columna (su tipo y sus condiciones)
# Check: una condicion, por ejemplo ">= 0" o "esta en esta lista"
from pandera.pandas import Check, Column

# ---------------------------------------------------------------------------
# VALORES ACEPTADOS en las columnas de categorias
# ---------------------------------------------------------------------------
# Los unicos 4 valores que puede tener la columna segmento
SEGMENTOS = ["Residencial", "Comercial", "Industrial", "No informado"]
# Los unicos 2 valores que puede tener la columna tipo_compra
TIPOS_COMPRA = ["Bolsa", "Contrato"]

# ---------------------------------------------------------------------------
# EL ESQUEMA de la tabla limpia
# ---------------------------------------------------------------------------
# pa.DataFrameSchema(...) crea el esquema. Recibe un diccionario
# {nombre de columna: Column(tipo, condicion)} y algunas reglas de toda la tabla
ESQUEMA_VENTAS = pa.DataFrameSchema(
    {
        # periodo: texto (str) que cumpla el patron AAAA-MM con un mes de 01 a 12.
        # r"^\d{4}-(0[1-9]|1[0-2])$" es una expresion regular (un patron de texto):
        #   ^ inicio, \d{4} cuatro digitos, - un guion, (0[1-9]|1[0-2]) del 01 al 12, $ fin
        # Ejemplo: '2023-04' cumple; '2023-13' y 'TOTAL' no cumplen
        "periodo": Column(str, Check.str_matches(r"^\d{4}-(0[1-9]|1[0-2])$")),
        # divipola: texto de exactamente 5 digitos (^\d{5}$). '05001' cumple; '5001' no
        "divipola": Column(str, Check.str_matches(r"^\d{5}$")),
        # municipio: texto, sin condicion extra (el nombre oficial ya viene de MUNICIPIOS)
        "municipio": Column(str),
        # segmento: texto que este en la lista SEGMENTOS (.isin = "esta en")
        "segmento": Column(str, Check.isin(SEGMENTOS)),
        # tipo_compra: texto que este en la lista TIPOS_COMPRA: solo Bolsa o Contrato
        "tipo_compra": Column(str, Check.isin(TIPOS_COMPRA)),
        # energia_kwh: numero con decimales (float) mayor o igual a 0 (ge = greater or equal)
        "energia_kwh": Column(float, Check.ge(0)),
        # valor_cop: numero >= 0; nullable=True permite celdas vacias (regla 9 de la limpieza)
        "valor_cop": Column(float, Check.ge(0), nullable=True),
        # clientes: numero entero (int) mayor o igual a 0
        "clientes": Column(int, Check.ge(0)),
    },
    # unique: no puede haber dos filas con el mismo periodo, municipio, segmento y tipo
    # de compra; si las hay, es una venta repetida
    unique=["periodo", "divipola", "segmento", "tipo_compra"],
    # strict=True: la tabla no puede traer columnas que no esten en este esquema
    strict=True,
)
```

| Parte | Qué hace |
|---|---|
| `import pandera.pandas as pa` | Trae pandera, en su versión para tablas de pandas. |
| `pa.DataFrameSchema({...})` | Crea el esquema: un diccionario con una regla por columna. |
| `Column(str, ...)` | La columna debe ser de **texto**. `Column(float, ...)`: número decimal. `Column(int, ...)`: número entero. |
| `Check.str_matches(r"^\d{4}-(0[1-9]\|1[0-2])$")` | El texto debe tener la forma `AAAA-MM`. `\d{4}` = 4 dígitos; `(0[1-9]\|1[0-2])` = un mes de 01 a 12. Es una **expresión regular**. |
| `Check.str_matches(r"^\d{5}$")` | El código DIVIPOLA debe tener exactamente 5 dígitos. |
| `Check.isin(SEGMENTOS)` | El valor debe estar en la lista: solo se aceptan esos 4 segmentos. |
| `Check.ge(0)` | *Greater or equal*: el número debe ser mayor o igual a 0. |
| `nullable=True` | La columna puede tener celdas vacías. Sin esto, una celda vacía es un error. |
| `unique=[...]` | No puede haber dos filas con el mismo periodo, municipio, segmento y tipo de compra: es el **grano** de la tabla. |
| `strict=True` | La tabla no puede traer columnas que no estén en el esquema. |

**Dónde están todas las reglas que pandera entiende:** en la documentación oficial, https://pandera.readthedocs.io, en la sección **Checks**.

**Otras reglas que pueden servir más adelante.** No están en el proyecto todavía, pero se probaron con pandera 0.35 y funcionan:

| Para qué | Cómo se escribe | Qué detiene |
|---|---|---|
| Precio de bolsa de XM en un rango que tenga sentido | `Column(float, Check.in_range(0, 5000))` | Un precio de 80.000 $/kWh (error de digitación) |
| Temperatura del IDEAM posible en Colombia | `Column(float, Check.in_range(-10, 45))` | Un `-999`, que es el código de "sin dato" |
| Fecha que no esté en el futuro | `Column("datetime64[ns]", Check.le(pd.Timestamp.today()))` | Una venta con fecha de 2031 |
| Solo periodos del año del estudio | `Column(str, Check.str_startswith("2023"))` | Una fila de `2022-12` que se coló |
| Nombre sin espacios sobrantes | `Column(str, Check(lambda s: s == s.str.strip()))` | `" Medellín "` |
| Tarifa razonable: mira **dos columnas** a la vez | `checks=Check(lambda df: (df["valor_cop"] / df["energia_kwh"]).between(200, 2000))`, dentro de `pa.DataFrameSchema(...)` | 100 kWh facturados a $5 |
| Columna que puede venir o no | `Column(str, required=False)` | Nada: acepta la tabla con o sin la columna `observacion` |

`Check(lambda ...)` sirve para escribir una **regla propia** cuando pandera no trae una palabra hecha para eso. `lambda s:` recibe la columna completa (`s`) y debe responder, fila por fila, `True` (cumple) o `False` (no cumple).

### 2.3 La limpieza: `src/silver/enerandes.py`

**¿Para qué otro archivo, si ya está `esquemas.py`?** Son dos archivos distintos que trabajan juntos:

| Archivo | Qué hace | Ejemplo |
|---|---|---|
| `enerandes.py` | **Limpia**: cambia los datos. | Convierte `RESID.` en `Residencial` y quita las filas repetidas. |
| `esquemas.py` | **Revisa**: no cambia nada, solo dice si quedó bien o mal. | Comprueba que el segmento sea uno de los 4 permitidos. |

Es como una fábrica: `enerandes.py` es el **operario** que arregla el producto y `esquemas.py` es el **inspector** que al final revisa si quedó bien. Si el inspector encuentra un error, el producto no sale: la tabla no se guarda.

```text
bronce → enerandes.py (limpia) → esquemas.py (revisa) → plata
```

**¿Por qué separados y no en un solo archivo?**

| Razón | Explicación |
|---|---|
| El inspector no puede ser el mismo operario | Si las reglas estuvieran mezcladas con la limpieza, un error en la limpieza también podría dañar la revisión, y nadie lo notaría. Separadas, la revisión no depende de cómo se limpió. |
| Las reglas se escriben una sola vez y se usan en varios lados | `esquemas.py` lo usan la limpieza (`enerandes.py`) **y** las pruebas (`tests/`). Si estuvieran dentro de `enerandes.py`, habría que copiarlas. |
| Cada archivo hace una sola cosa | Si cambia una regla de calidad, se toca solo `esquemas.py`; si cambia la forma de limpiar, solo `enerandes.py`. |
| Cada rol del equipo tiene su archivo | El **Data Quality Analyst** escribe las reglas (`esquemas.py`) y el **Data Engineer** escribe la limpieza (`enerandes.py`), sin pisarse. |

**Las 5 funciones de `enerandes.py`:**

| Función | Qué hace |
|---|---|
| `sin_tildes()` | Ayudante: quita tildes, mayúsculas y espacios. `" ITAGÜÍ "` → `"itagui"`. |
| `clave_municipio()` | Ayudante: convierte las formas de escribir un municipio en una sola. `"Rio Negro"` → `"rionegro"`. |
| **`limpiar()`** | **La que limpia**: aplica las 9 reglas, una detrás de otra, y separa las filas limpias de la cuarentena. Las 9 reglas no son 9 funciones: son 9 bloques dentro de `limpiar()`, cada uno con su comentario `# Regla 1`, `# Regla 2`… |
| `escribir_reporte()` | Escribe `docs/reporte_calidad.md` con el antes y el después de cada regla. |
| `main()` | La que arranca todo: lee bronce → llama a `limpiar()` → revisa con pandera → guarda. |

**¿Quién usa `esquemas.py`?** No es `limpiar()`: es **`main()`**, después de limpiar. `main()` es el jefe que pone a trabajar en orden al operario y al inspector:

```python
# Linea 24: trae las reglas de esquemas.py
from src.quality.esquemas import ESQUEMA_VENTAS

# Dentro de main():
limpias, cuarentena, metricas = limpiar(bronce)   # 1. el operario limpia
ESQUEMA_VENTAS.validate(limpias, lazy=True)       # 2. el inspector revisa
```

| Función | ¿Usa `esquemas.py`? |
|---|---|
| `limpiar()` | No: solo limpia. |
| `main()` | **Sí**: primero llama a `limpiar()` y después revisa el resultado con `ESQUEMA_VENTAS`. |

**Creen el archivo `src/silver/enerandes.py` y peguen este código:**

```python
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


# ---------------------------------------------------------------------------
# FUNCIONES DE APOYO
# ---------------------------------------------------------------------------
def sin_tildes(texto: str) -> str:
    """'Itagüí' -> 'itagui': minuscula, sin espacios a los lados y sin tildes."""
    # texto.strip() quita los espacios de los lados: ' ITAGÜÍ ' -> 'ITAGÜÍ'
    # .lower() lo pasa a minuscula: 'ITAGÜÍ' -> 'itagüí'
    # normalize("NFD", ...) separa cada letra de su tilde: 'í' queda como 'i' + tilde
    letras = unicodedata.normalize("NFD", texto.strip().lower())
    # (c for c in letras if ...) recorre las letras una por una y salta las tildes
    # (las tildes son de la categoria "Mn"); "".join(...) las vuelve a unir en un texto
    return "".join(c for c in letras if unicodedata.category(c) != "Mn")


def clave_municipio(texto) -> str | None:
    """Convierte cualquier forma de escribir el municipio en la clave de MUNICIPIOS."""
    # pd.isna(texto) es True si la celda esta vacia: no hay municipio que buscar
    if pd.isna(texto):
        # None significa "sin valor"
        return None
    # Quita espacios, mayusculas y tildes: ' Rio Negro ' -> 'rio negro'
    clave = sin_tildes(texto)
    # .get(clave, clave) busca la clave en ALIAS_MUNICIPIO:
    # si la encuentra ('rio negro'), devuelve su valor ('rionegro');
    # si no la encuentra ('bello'), devuelve la misma clave ('bello')
    return ALIAS_MUNICIPIO.get(clave, clave)


# ---------------------------------------------------------------------------
# LIMPIEZA: las 9 reglas, en orden
# ---------------------------------------------------------------------------
def limpiar(bronce: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, list[dict]]:
    """Aplica las reglas en orden. Devuelve (limpias, cuarentena, metricas)."""
    # metricas es una lista vacia. Cada regla le agrega una fila del reporte de calidad
    metricas = []

    # medir() es una funcion dentro de la funcion. Ejemplo:
    #   medir("Filas duplicadas", "Dejar una sola copia", 32, 0)
    # agrega a metricas: {"problema": "Filas duplicadas", "regla aplicada": "Dejar una
    # sola copia", "antes": 32, "despues": 0}
    def medir(problema: str, regla: str, antes: int, despues: int) -> None:
        metricas.append({"problema": problema, "regla aplicada": regla,
                         "antes": antes, "despues": despues})

    # La tabla de bronce tiene 10 columnas: col_0 ... col_6 y las 3 de linaje
    # (_fuente, _origen, _extraido_en). .drop(columns=LINAJE) quita esas 3.
    # errors="ignore": si alguna de las 3 no existe, no da error.
    # df es la tabla con la que se trabaja de aqui en adelante
    df = bronce.drop(columns=LINAJE, errors="ignore")

    # ------------------------------------------------------------------
    # Regla 1. La primera fila es el encabezado
    # ------------------------------------------------------------------
    # Asi esta df ahora:
    #        col_0      col_1      col_2        col_3  ...
    #   0    Fecha  Municipio   Segmento  Tipo_Compra  ...   <- el encabezado
    #   1  2023-04 Copacabana Industrial        Bolsa  ...   <- la primera venta
    # df.iloc[0] es la fila de la posicion 0; .tolist() la vuelve una lista:
    #   encabezado = ['Fecha', 'Municipio', 'Segmento', 'Tipo_Compra', ...]
    encabezado = df.iloc[0].tolist()
    # df.iloc[1:] son las filas desde la posicion 1 hasta el final: todas menos el
    # encabezado. .copy() hace una copia, para trabajar sobre ella sin danar bronce
    df = df.iloc[1:].copy()
    # Para cada nombre del encabezado busca su nombre estandar en COLUMNAS_2023:
    #   'Fecha' -> 'periodo', 'Municipio' -> 'municipio', 'Segmento' -> 'segmento' ...
    # y pone esa lista como los nombres de las columnas. Asi queda df:
    #        periodo   municipio    segmento tipo_compra  ...
    #   1    2023-04  Copacabana  Industrial       Bolsa  ...
    df.columns = [COLUMNAS_2023[nombre] for nombre in encabezado]
    # Habia 1 encabezado guardado como fila; despues hay 0
    medir("Encabezado guardado como una fila", "Usarlo como nombres de columna", 1, 0)

    # ------------------------------------------------------------------
    # Regla 2. La fila TOTAL al final de la hoja: no es una venta
    # ------------------------------------------------------------------
    # df["periodo"] es la columna periodo: '2023-04', '2023-09', ..., 'TOTAL'
    # .str.upper() la pasa a mayuscula y .str.strip() le quita los espacios
    # (por si dijera ' total '). == "TOTAL" compara cada fila con 'TOTAL'.
    # El resultado es una columna de True/False, una respuesta por fila:
    #   '2023-04' -> False,  '2023-09' -> False,  ...,  'TOTAL' -> True
    es_total = df["periodo"].str.upper().str.strip() == "TOTAL"
    # .sum() suma la columna: cada True vale 1 y cada False vale 0.
    # Aqui da 1, porque hay 1 fila TOTAL. int() lo vuelve un numero entero normal
    medir("Filas de totales", "Eliminarlas", int(es_total.sum()), 0)
    # ~ invierte cada respuesta: True -> False y False -> True.
    # ~es_total es True en las filas que NO son total.
    # df[ columna de True/False ] devuelve solo las filas que dicen True.
    # Resultado: df ya no tiene la fila TOTAL
    df = df[~es_total]

    # ------------------------------------------------------------------
    # Regla 3. Filas repetidas exactamente iguales
    # ------------------------------------------------------------------
    # .duplicated() revisa fila por fila: True si la fila es igual a otra que ya
    # aparecio antes (la primera vez que aparece queda en False).
    # .sum() cuenta los True: aqui da 32 copias. antes guarda ese 32
    antes = int(df.duplicated().sum())
    # .drop_duplicates() borra las 32 copias y deja la primera de cada una
    df = df.drop_duplicates()
    # Vuelve a contar las copias: ahora da 0
    medir("Filas duplicadas", "Dejar una sola copia", antes, int(df.duplicated().sum()))

    # ------------------------------------------------------------------
    # Regla 4. Segmento escrito de varias formas o vacio
    # ------------------------------------------------------------------
    # df["segmento"] es la columna segmento. Tiene estos valores distintos:
    #   'Industrial', 'Comercial', 'Residencial', 'RESID.', 'Comercial ', 'IND'
    #   (y algunas celdas vacias)
    # .nunique() cuenta cuantos valores DISTINTOS hay, sin contar los vacios: 6.
    # antes guarda ese 6
    antes = df["segmento"].nunique()
    # .map(...) recorre la columna y cambia cada celda por lo que diga la funcion.
    # lambda s: ... es esa funcion, escrita en una linea; s es el valor de la celda:
    #   si s no esta vacio (pd.notna(s)):
    #       sin_tildes(s) lo limpia:         'RESID.' -> 'resid.'
    #       SEGMENTOS.get(...) lo busca:     'resid.' -> 'Residencial'
    #   si s esta vacio: devuelve None (sigue vacio)
    # Ejemplos:  'RESID.' -> 'Residencial'   'IND' -> 'Industrial'
    #            'Comercial ' -> 'Comercial'  (vacio) -> None
    df["segmento"] = df["segmento"].map(lambda s: SEGMENTOS.get(sin_tildes(s)) if pd.notna(s) else None)
    # .isna() da True en cada celda vacia; .sum() las cuenta: 14
    vacios = int(df["segmento"].isna().sum())
    # .fillna("No informado") escribe 'No informado' en cada celda vacia
    df["segmento"] = df["segmento"].fillna("No informado")
    # Valores distintos despues: Residencial, Comercial, Industrial y No informado = 4.
    # El - 1 descuenta 'No informado', que no es un segmento real: queda 3
    medir("Segmento escrito de varias formas", "Unificar a 3 valores", antes, df["segmento"].nunique() - 1)
    # Habia 14 vacios; despues, 0
    medir("Segmento vacio", "Marcarlo como 'No informado'", vacios, 0)

    # ------------------------------------------------------------------
    # Regla 5. Tipo de compra escrito de varias formas
    # ------------------------------------------------------------------
    # Valores distintos de tipo_compra: 'Bolsa', 'Contrato', 'CONTRATOS', 'bolsa'.
    # .nunique() da 4; antes guarda ese 4
    antes = df["tipo_compra"].nunique()
    # A cada celda t: sin_tildes la limpia y TIPOS_COMPRA.get la cambia:
    #   'CONTRATOS' -> 'contratos' -> 'Contrato'
    #   'bolsa'     -> 'bolsa'     -> 'Bolsa'
    df["tipo_compra"] = df["tipo_compra"].map(lambda t: TIPOS_COMPRA.get(sin_tildes(t)))
    # Valores distintos despues: 'Bolsa' y 'Contrato' = 2
    medir("Tipo de compra escrito de varias formas", "Unificar a Bolsa y Contrato",
          antes, df["tipo_compra"].nunique())

    # ------------------------------------------------------------------
    # Regla 6. Municipio escrito de varias formas: se cambia por su codigo DIVIPOLA
    # ------------------------------------------------------------------
    # La columna municipio tiene 31 formas distintas de escribir 15 municipios:
    #   'Medellin', 'medellin', 'Medellín', 'Medellín ', 'Medellín D.E.',
    #   'Bello', 'BELLO', 'Bello ', 'Rio Negro', 'Rionegro', 'Rionegro (Ant)', ...
    # .nunique() las cuenta: 31. antes guarda ese 31
    antes = df["municipio"].nunique()
    # .map(clave_municipio) le aplica a cada celda la funcion clave_municipio,
    # que deja una sola forma por municipio:
    #   'Medellín D.E.' -> 'medellin'    'BELLO' -> 'bello'    'Rio Negro' -> 'rionegro'
    # claves es una columna nueva con esas formas
    claves = df["municipio"].map(clave_municipio)
    # Con cada clave c busca en MUNICIPIOS, que guarda (codigo, nombre oficial):
    #   MUNICIPIOS['rionegro'] = ('05615', 'Rionegro')
    # [0] toma el primero, el codigo: '05615'.
    # df["divipola"] = ... crea la columna divipola con esos codigos
    df["divipola"] = claves.map(lambda c: MUNICIPIOS[c][0])
    # [1] toma el segundo, el nombre oficial: 'Rionegro'.
    # Se escribe encima de la columna municipio
    df["municipio"] = claves.map(lambda c: MUNICIPIOS[c][1])
    # Valores distintos despues: los 15 municipios reales
    medir("Municipio escrito de varias formas", "Unificar con el codigo DIVIPOLA",
          antes, df["municipio"].nunique())

    # ------------------------------------------------------------------
    # Regla 7. Los numeros llegaron como texto: se convierten a numero
    # ------------------------------------------------------------------
    # for col in [...] repite lo de adentro 3 veces, una con cada columna:
    # primero col = "energia_kwh", luego "valor_cop" y luego "clientes"
    for col in ["energia_kwh", "valor_cop", "clientes"]:
        # pd.to_numeric convierte el texto en numero: '98240' -> 98240.0
        # errors="coerce": si una celda no es un numero, queda vacia (NaN)
        # en vez de detener el programa con un error
        df[col] = pd.to_numeric(df[col], errors="coerce")
    # .astype(int) quita los decimales: 2.0 -> 2. Los clientes son personas
    df["clientes"] = df["clientes"].astype(int)

    # ------------------------------------------------------------------
    # Regla 8. Energia vacia o negativa: no se puede adivinar -> cuarentena
    # ------------------------------------------------------------------
    # df["energia_kwh"].isna()  -> True si la energia esta vacia
    # (df["energia_kwh"] < 0)   -> True si la energia es negativa
    # |                         -> significa "o": True si pasa cualquiera de las dos
    # malas es una columna de True/False. Ejemplo:
    #   98240 -> False    NaN (vacia) -> True    -594733 -> True    74785 -> False
    malas = df["energia_kwh"].isna() | (df["energia_kwh"] < 0)
    # df[malas] devuelve solo las filas que dicen True: las 16 malas.
    # Se guardan aparte en cuarentena: no se borran
    cuarentena = df[malas]
    # ~malas invierte: True en las filas buenas. df[~malas] devuelve solo esas,
    # y se guardan otra vez en df: desde aqui df ya no tiene las 16 malas
    df = df[~malas]
    # .sum() cuenta los True de malas: 16
    medir("Energia vacia o negativa", "Pasar la fila a cuarentena", int(malas.sum()), 0)

    # ------------------------------------------------------------------
    # Regla 9. Valor facturado vacio: se deja vacio (no se inventa un valor)
    # ------------------------------------------------------------------
    # .isna() da True en cada valor vacio y .sum() los cuenta: 7.
    # No se corrige nada: solo se cuenta para que quede en el reporte
    vacios = int(df["valor_cop"].isna().sum())
    # Antes 7, despues 7: no hay como saber el valor real
    medir("Valor facturado vacio", "Dejarlo vacio y documentarlo", vacios, vacios)

    # ------------------------------------------------------------------
    # Resultado
    # ------------------------------------------------------------------
    # El orden en que quedan las columnas en la capa plata
    orden = ["periodo", "divipola", "municipio", "segmento", "tipo_compra",
             "energia_kwh", "valor_cop", "clientes"]
    # df[orden] pone las columnas en ese orden.
    # .reset_index(drop=True) vuelve a numerar las filas 0, 1, 2, ... sin huecos
    # (quedaron huecos donde estaban las filas borradas).
    # return devuelve 3 cosas: la tabla limpia, la cuarentena y la lista de metricas
    return df[orden].reset_index(drop=True), cuarentena, metricas


# ---------------------------------------------------------------------------
# REPORTE DE CALIDAD
# ---------------------------------------------------------------------------
def escribir_reporte(metricas: list[dict], filas_bronce: int, filas_plata: int, filas_cuarentena: int) -> None:
    """Escribe docs/reporte_calidad.md con la tabla de metricas antes y despues."""
    # Lista con las primeras lineas del reporte: el titulo, el conteo de filas
    # y el encabezado de la tabla.
    # f"...{filas_bronce:,}" mete el numero dentro del texto; :, le pone separador de miles
    lineas = [
        "# Reporte de calidad: ventas de EnerAndes (hoja 2023)\n",
        f"- Filas en bronce: {filas_bronce:,}",
        f"- Filas en plata: {filas_plata:,}",
        f"- Filas en cuarentena: {filas_cuarentena:,}\n",
        "| # | Problema | Regla aplicada | Antes | Despues |",
        "|---|---|---|---|---|",
    ]
    # Recorre las metricas; enumerate(..., start=1) da tambien su numero: 1, 2, 3...
    # n es el numero y m es el diccionario de la metrica
    for n, m in enumerate(metricas, start=1):
        # Agrega una fila de la tabla con los datos de esa regla
        lineas.append(f"| {n} | {m['problema']} | {m['regla aplicada']} | {m['antes']} | {m['despues']} |")
    # .mkdir crea la carpeta docs/; parents=True crea tambien las carpetas de arriba
    # si faltan; exist_ok=True no da error si ya existe
    config.DIR_DOCS.mkdir(parents=True, exist_ok=True)
    # "\n".join(lineas) une las lineas con un salto de linea entre cada una;
    # .write_text(...) escribe ese texto en docs/reporte_calidad.md
    (config.DIR_DOCS / "reporte_calidad.md").write_text("\n".join(lineas) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# PROGRAMA PRINCIPAL
# ---------------------------------------------------------------------------
def main() -> None:
    # Lee el archivo Parquet de bronce y lo guarda en la tabla bronce
    bronce = pd.read_parquet(config.DIR_BRONZE / "enerandes_ventas_2023.parquet")
    # len(bronce) es el numero de filas; log lo muestra con la hora
    log(f"Bronce: {len(bronce):,} filas")
    # Llama a limpiar(); como devuelve tres cosas, se reciben en tres variables
    limpias, cuarentena, metricas = limpiar(bronce)

    # Revisa la tabla limpia con las reglas de pandera.
    # Si una regla falla, el programa se detiene aqui y no guarda nada;
    # lazy=True: revisa todo y muestra TODOS los errores juntos
    ESQUEMA_VENTAS.validate(limpias, lazy=True)
    # Si llego a esta linea, la tabla cumplio todas las reglas
    log("Validacion con pandera: OK")

    # Crea la carpeta data/silver/ si no existe
    config.DIR_SILVER.mkdir(parents=True, exist_ok=True)
    # .to_parquet guarda la tabla en un archivo Parquet;
    # index=False: no guarda la columna de numeros de fila
    limpias.to_parquet(config.DIR_SILVER / "enerandes_ventas.parquet", index=False)
    cuarentena.to_parquet(config.DIR_SILVER / "enerandes_cuarentena.parquet", index=False)
    # Escribe docs/reporte_calidad.md
    escribir_reporte(metricas, len(bronce), len(limpias), len(cuarentena))

    # Muestra la tabla de metricas en la terminal, alineada en columnas:
    # :<42 ocupa 42 espacios alineado a la izquierda; :>7 ocupa 7 alineado a la derecha
    print(f"   {'problema':<42}{'antes':>7}{'despues':>9}")
    # Una linea por cada regla
    for m in metricas:
        print(f"   {m['problema']:<42}{m['antes']:>7}{m['despues']:>9}")
    log(f"Plata: {len(limpias):,} filas limpias y {len(cuarentena)} en cuarentena")
    log("Reporte en docs/reporte_calidad.md")


# __name__ vale "__main__" solo cuando se ejecuta este archivo
# (python -m src.silver.enerandes). Si otro archivo lo importa (las pruebas),
# main() no se ejecuta: solo se usan sus funciones
if __name__ == "__main__":
    main()
```

**Las tablas de traducción** (al inicio del archivo):

| Parte | Qué hace |
|---|---|
| `COLUMNAS_2023` | Traduce los encabezados de la hoja 2023 (`Energia_kWh`) a los nombres estándar de plata (`energia_kwh`). Cada hoja del Excel tiene encabezados distintos: la Evidencia 2 pide uno de estos diccionarios por hoja. |
| `MUNICIPIOS` | Para cada municipio, escrito en minúscula y sin tildes, su código DIVIPOLA y su nombre oficial: `"itagui": ("05360", "Itagüí")`. |
| `ALIAS_MUNICIPIO` | Las formas de escribir un municipio que **no** se arreglan quitando tildes y mayúsculas: `"rio negro"` → `"rionegro"`. |
| `SEGMENTOS` y `TIPOS_COMPRA` | Cada forma de escribir el segmento o el tipo de compra → su valor estándar: `"resid."` → `"Residencial"`. |

**Las funciones de apoyo:**

| Parte | Qué hace |
|---|---|
| `sin_tildes(texto)` | `' ITAGÜÍ '` → `'itagui'`: quita los espacios de los lados (`strip`), pasa a minúscula (`lower`) y quita las tildes. |
| `unicodedata.normalize("NFD", ...)` | Separa cada letra de su tilde: `í` queda como `i` + tilde. Luego se quedan solo las letras: las tildes son la categoría `Mn`. |
| `clave_municipio(texto)` | Quita tildes y, si el resultado es un alias, lo cambia: `'Rio Negro'` → `'rio negro'` → `'rionegro'`. |
| `ALIAS_MUNICIPIO.get(clave, clave)` | Busca la clave en los alias; si no está, devuelve la misma clave. |

**La función `limpiar()`, regla por regla:**

| Parte | Qué hace |
|---|---|
| `medir(problema, regla, antes, despues)` | Anota una fila del reporte de calidad. Se llama una vez por cada regla. |
| `df.iloc[0].tolist()` | Regla 1: toma la primera fila (el encabezado) como lista. |
| `df.iloc[1:].copy()` | Se queda con las filas de la 1 en adelante: los datos. |
| `es_total = ... == "TOTAL"` | Regla 2: marca las filas cuyo periodo dice `TOTAL`; `df[~es_total]` se queda con las demás. |
| `df.duplicated().sum()` y `df.drop_duplicates()` | Regla 3: cuenta las filas repetidas y deja una sola copia de cada una. |
| `df["segmento"].map(...)` | Regla 4: cambia cada valor por el de la tabla `SEGMENTOS`. `map` aplica una función a cada celda. |
| `fillna("No informado")` | Regla 5: llena los segmentos vacíos con `No informado`. |
| `claves.map(lambda c: MUNICIPIOS[c][0])` | Regla 6: con la clave del municipio, busca su código DIVIPOLA (posición `0` de la pareja) y su nombre oficial (posición `1`). |
| `pd.to_numeric(..., errors="coerce")` | Regla 7: convierte el texto en número; si una celda no es un número, queda vacía en vez de dar error. |
| `malas = ... isna() \| ... < 0` | Regla 8: marca las filas con energía vacía **o** (`\|`) negativa. Esas filas van a `cuarentena`; las demás siguen. |
| `vacios = ... valor_cop ... isna()` | Regla 9: solo **cuenta** los valores vacíos; no los cambia. |
| `return df[orden], cuarentena, metricas` | Devuelve 3 cosas: la tabla limpia (con las columnas en orden), la cuarentena y la lista de métricas. |

**¿De dónde sale `limpias`?** La crea `limpiar()`. **Adentro** de la función, la tabla se llama `df`. Cuando la función termina, la **entrega** con `return`, y quien la recibe le pone el nombre `limpias`. Es **la misma tabla con dos nombres**: adentro de `limpiar()` se llama `df`, y afuera, en `main()`, se llama `limpias`:

```python
# --- Dentro de limpiar() ---
def limpiar(bronce):                          # recibe la tabla sucia de bronce
    df = bronce.drop(columns=LINAJE, ...)     # linea 120: aqui nace df, una copia de bronce
    # ... de aqui en adelante se le aplican las 9 reglas a df ...
    return df[orden].reset_index(drop=True), cuarentena, metricas   # linea 291: entrega 3 cosas

# --- Dentro de main() ---
limpias, cuarentena, metricas = limpiar(bronce)   # linea 332: recibe las 3 y les pone nombre
ESQUEMA_VENTAS.validate(limpias, lazy=True)       # linea 337: pandera revisa limpias
```

| Lo que entrega `return` (línea 291) | Variable que lo recibe (línea 332) | Qué es |
|---|---|---|
| `df[orden].reset_index(drop=True)` | `limpias` | La tabla limpia: 1.064 filas |
| `cuarentena` | `cuarentena` | Las 16 filas apartadas |
| `metricas` | `metricas` | Lo que se midió antes y después de cada regla |

`df[orden]` pone las columnas en el orden del esquema, y `.reset_index(drop=True)` vuelve a numerar las filas desde 0, porque al quitar filas quedaron huecos en la numeración.

> 💡 Es como un panadero: mientras trabaja la llama "la masa"; cuando se la entrega a usted, usted la llama "el pan". Es lo mismo con otro nombre.

**Las funciones finales:**

| Parte | Qué hace |
|---|---|
| `escribir_reporte(...)` | Escribe `docs/reporte_calidad.md`: las filas de cada capa y la tabla de métricas en formato Markdown. |
| `ESQUEMA_VENTAS.validate(limpias, lazy=True)` | *Validate* = validar: revisa cada fila de la tabla `limpias` contra cada regla de `esquemas.py`. Si hay 0 errores, el programa sigue y guarda; si hay 1 o más, se detiene con `SchemaErrors` y no guarda nada. *Lazy* = perezoso: no se detiene en el primer error, revisa **toda** la tabla y al final muestra **todos** los errores juntos. Sin `lazy=True`, se vería un error, se corregiría, se ejecutaría otra vez y aparecería el siguiente, una y otra vez. |
| `limpias.to_parquet(...)` | Guarda la tabla limpia en `data/silver/enerandes_ventas.parquet`. |
| `cuarentena.to_parquet(...)` | Guarda la cuarentena en `data/silver/enerandes_cuarentena.parquet`. |

### 2.4 Ejecutarlo

El programa `src/silver/enerandes.py` lee la hoja 2023 de bronce, le aplica las 9 reglas, mide cada problema antes y después, revisa la tabla limpia con pandera y guarda las filas limpias, la cuarentena y el reporte de calidad.

```powershell
python -m src.silver.enerandes
```

| Parte | Qué significa |
|---|---|
| `python` | Ejecuta un programa de Python. |
| `-m` | *module*: ejecuta el archivo como módulo del proyecto. Así funcionan las líneas `from src.config import ...` del código. |
| `src.silver.enerandes` | El archivo `src/silver/enerandes.py`, escrito con puntos en lugar de `/` y sin `.py`. |

**Resultado:**

```text
[20:35:29] Bronce: 1,114 filas
[20:35:29] Validacion con pandera: OK
   problema                                    antes  despues
   Encabezado guardado como una fila               1        0
   Filas de totales                                1        0
   Filas duplicadas                               32        0
   Segmento escrito de varias formas               6        3
   Segmento vacio                                 14        0
   Tipo de compra escrito de varias formas         4        2
   Municipio escrito de varias formas             31       15
   Energia vacia o negativa                       16        0
   Valor facturado vacio                           7        7
[20:35:29] Plata: 1,064 filas limpias y 16 en cuarentena
[20:35:29] Reporte en docs/reporte_calidad.md
```

| Lo que aparece | Qué significa |
|---|---|
| `[20:35:29]` | La hora en que pasó cada cosa. En su computador sale otra hora. |
| `Bronce: 1,114 filas` | La hoja 2023 como llegó: 1 encabezado + 1.080 ventas + 32 duplicados + 1 fila `TOTAL`. |
| `Validacion con pandera: OK` | La tabla limpia cumple **todas** las reglas del esquema. |
| `Encabezado guardado como una fila 1 → 0` | Había una fila con los títulos de las columnas; se usó como nombres de columna y se quitó de los datos. |
| `Filas de totales 1 → 0` | Se quitó la fila `TOTAL`: no es una venta. |
| `Filas duplicadas 32 → 0` | Se quitaron las 32 copias. |
| `Segmento ... 6 → 3` | `Residencial`, `Comercial`, `Industrial`, `RESID.`, `IND` y `"Comercial "` (con espacio) quedaron en 3 valores. |
| `Segmento vacio 14 → 0` | Las 14 ventas sin segmento quedaron como `No informado`. |
| `Tipo de compra ... 4 → 2` | Las 4 formas de escribirlo quedaron en `Bolsa` y `Contrato`. |
| `Municipio ... 31 → 15` | Las 31 formas de escribir los municipios quedaron en los **15** municipios reales, cada uno con su código DIVIPOLA. |
| `Energia vacia o negativa 16 → 0` | 9 vacías y 7 negativas pasaron a la cuarentena. |
| `Valor facturado vacio 7 → 7` | No se corrige: no hay cómo saber el valor real. Se deja vacío y queda documentado. |
| `1,064 filas limpias y 16 en cuarentena` | 1.080 ventas reales = 1.064 limpias + 16 apartadas. No se perdió ninguna fila sin dejar rastro. |
| `Reporte en docs/reporte_calidad.md` | Se escribió el reporte de calidad: cada problema, la regla y el antes y el después. |

> ✅ **Este comando crea 3 archivos nuevos.** Búsquenlos en el EXPLORER de VS Code:
>
> ```text
> observatorio-energia/
> ├── data/
> │   └── silver/                          ← carpeta nueva: la capa plata
> │       ├── enerandes_ventas.parquet     ← las 1.064 ventas limpias
> │       └── enerandes_cuarentena.parquet ← las 16 ventas apartadas
> └── docs/
>     └── reporte_calidad.md               ← el reporte de calidad
> ```
>
> `.parquet` es un formato de tabla comprimido, que pandas, DuckDB y dbt leen muy rápido; no se abre con doble clic, se lee con código (paso 2.5). Estos archivos son los que usa la capa oro.

**El reporte de calidad** (`docs/reporte_calidad.md`) queda así:

| # | Problema | Regla aplicada | Antes | Despues |
|---|---|---|---|---|
| 1 | Encabezado guardado como una fila | Usarlo como nombres de columna | 1 | 0 |
| 2 | Filas de totales | Eliminarlas | 1 | 0 |
| 3 | Filas duplicadas | Dejar una sola copia | 32 | 0 |
| 4 | Segmento escrito de varias formas | Unificar a 3 valores | 6 | 3 |
| 5 | Segmento vacio | Marcarlo como 'No informado' | 14 | 0 |
| 6 | Tipo de compra escrito de varias formas | Unificar a Bolsa y Contrato | 4 | 2 |
| 7 | Municipio escrito de varias formas | Unificar con el codigo DIVIPOLA | 31 | 15 |
| 8 | Energia vacia o negativa | Pasar la fila a cuarentena | 16 | 0 |
| 9 | Valor facturado vacio | Dejarlo vacio y documentarlo | 7 | 7 |

> ✅ **Esto es lo que pide la Evidencia 2 en el reporte de calidad:** cada problema, la regla que se aplicó y la métrica antes y después.

### 2.5 Ver los datos limpios y la cuarentena

Este comando abre el archivo de la capa plata y muestra sus 3 primeras filas, para ver cómo quedaron los datos limpios:

```powershell
python -c "import pandas as pd; print(pd.read_parquet('data/silver/enerandes_ventas.parquet').head(3))"
```

| Parte | Qué significa |
|---|---|
| `python -c "..."` | *command*: ejecuta el código de Python que va entre comillas, sin crear un archivo `.py`. |
| `import pandas as pd` | Carga pandas con el nombre corto `pd`. |
| `pd.read_parquet('data/silver/enerandes_ventas.parquet')` | Lee el archivo de las ventas limpias y lo convierte en una tabla (DataFrame). |
| `.head(3)` | Toma solo las 3 primeras filas. |
| `print(...)` | Las muestra en la terminal. |
| `;` | Separa dos instrucciones escritas en la misma línea. |

```text
   periodo divipola   municipio    segmento tipo_compra  energia_kwh    valor_cop  clientes
0  2023-04    05212  Copacabana  Industrial       Bolsa      98240.0   78251589.0         2
1  2023-09    05266    Envigado  Industrial    Contrato    1147369.0  949585522.0        27
2  2023-06    05212  Copacabana   Comercial       Bolsa      74785.0   75041080.0        53
```

| Lo que aparece | Qué significa |
|---|---|
| `0`, `1`, `2` a la izquierda | El número de cada fila (el *índice* de pandas). No es una columna del archivo. |
| Columnas con nombres estándar | Ya no son `col_0`, `col_1`…: cada columna tiene su nombre. |
| `divipola` = `05212` | Cada venta tiene el código oficial de su municipio: con él se puede cruzar con cualquier otra fuente del DANE. |
| `98240.0` | La energía ya es un **número** (antes era texto): se puede sumar. |

> 💡 **Si la terminal es angosta**, pandas no cabe y muestra `...` en lugar de algunas columnas, y al final `[3 rows x 8 columns]`. Es normal: los datos están completos. Para verlas todas, agranden el panel de la terminal o maximicen VS Code y ejecuten otra vez el comando.

Ahora las filas que **no** pasaron a la plata. Es el mismo comando, con otro archivo y 5 filas:

```powershell
python -c "import pandas as pd; print(pd.read_parquet('data/silver/enerandes_cuarentena.parquet').head(5))"
```

| Parte | Qué significa |
|---|---|
| `enerandes_cuarentena.parquet` | El archivo de la cuarentena: las 16 ventas con la energía vacía o negativa. No se borran: se guardan aparte para revisarlas. |
| `.head(5)` | Toma las 5 primeras filas. |

```text
   periodo municipio     segmento tipo_compra  energia_kwh     valor_cop  clientes divipola
0  2023-08     Bello  Residencial    Contrato          NaN  2.343628e+09     16391    05088
1  2023-06     Turbo  Residencial    Contrato    -594733.0  5.154798e+08      3717    05837
2  2023-01     Turbo   Industrial    Contrato    -387623.0  2.997692e+08         9    05837
3  2023-03  Apartadó    Comercial       Bolsa          NaN  1.141880e+08        82    05045
4  2023-02     Turbo   Industrial    Contrato          NaN  3.140045e+08        10    05837
```

| Lo que aparece | Qué significa |
|---|---|
| `energia_kwh` = `NaN` | La venta no tiene energía: no se puede saber cuánto se vendió. |
| `energia_kwh` = `-594733.0` | Energía negativa: es imposible. Puede ser un error de digitación del signo, pero **no se adivina**: se pregunta al área comercial. |
| `2.343628e+09` | Notación científica: 2,34 × 10⁹ = 2.343.628.000 COP. Es solo la forma en que pandas muestra números grandes. |

### 2.6 ¿Qué pasa cuando una regla falla?

Para ver a pandera en acción, dañemos a propósito 3 celdas de la tabla limpia y validémosla:

**¿Qué es "dañar"?** Ponerle **a propósito** datos malos a la tabla, para comprobar que pandera los atrapa. Es como probar una alarma: se abre la puerta a propósito para ver si suena. El archivo **no se toca**: el cambio se hace en una copia en memoria y se pierde cuando termina el comando.

| Celda | Valor bueno | Se cambia a | Regla de `esquemas.py` que lo atrapa |
|---|---|---|---|
| fila 3, `tipo_compra` | `Bolsa` o `Contrato` | `CONTRATOS` | `"tipo_compra": Column(str, Check.isin(TIPOS_COMPRA))`: solo se permiten `Bolsa` y `Contrato` |
| fila 10, `tipo_compra` | `Bolsa` o `Contrato` | `bolsa` | La misma: `bolsa` en minúscula no está en la lista |
| fila 5, `energia_kwh` | un número ≥ 0 | `-500.0` | `"energia_kwh": Column(float, Check.ge(0))`: la energía debe ser mayor o igual a 0 |


```powershell
python -c "import pandas as pd; from src.quality.esquemas import ESQUEMA_VENTAS; d = pd.read_parquet('data/silver/enerandes_ventas.parquet'); d.loc[[3, 10], 'tipo_compra'] = ['CONTRATOS', 'bolsa']; d.loc[5, 'energia_kwh'] = -500.0; ESQUEMA_VENTAS.validate(d, lazy=True)"
```

| Parte | Qué significa |
|---|---|
| `from src.quality.esquemas import ESQUEMA_VENTAS` | Trae el esquema de pandera: las reglas que debe cumplir la tabla limpia. |
| `d = pd.read_parquet(...)` | Lee la tabla limpia y la guarda en la variable `d`. |
| `d.loc[[3, 10], 'tipo_compra'] = ['CONTRATOS', 'bolsa']` | Daña 2 celdas: en las filas 3 y 10, la columna `tipo_compra` queda con valores que no son `Bolsa` ni `Contrato`. |
| `d.loc[5, 'energia_kwh'] = -500.0` | Daña 1 celda: en la fila 5, la energía queda negativa. |
| `ESQUEMA_VENTAS.validate(d, lazy=True)` | Revisa la tabla con las reglas. `lazy=True`: revisa todo y muestra todos los errores juntos, en vez de parar en el primero. |

**Resultado** (la parte final):

```text
pandera.errors.SchemaErrors: {
    "DATA": {
        "DATAFRAME_CHECK": [
            {
                "schema": null,
                "column": "tipo_compra",
                "check": "isin(['Bolsa', 'Contrato'])",
                "error": "Column 'tipo_compra' failed element-wise validator number 0: isin(['Bolsa', 'Contrato']) failure cases: CONTRATOS, bolsa"
            },
            {
                "schema": null,
                "column": "energia_kwh",
                "check": "greater_than_or_equal_to(0)",
                "error": "Column 'energia_kwh' failed element-wise validator number 0: greater_than_or_equal_to(0) failure cases: -500.0"
            }
        ]
    }
}
```

| Lo que aparece | Qué significa |
|---|---|
| `Traceback (most recent call last):` y las líneas de `pandera\...\container.py` | El camino que siguió el error dentro de la librería. Se puede saltar: lo importante está al final. |
| `SchemaErrors` | La tabla **no** cumple el esquema: el programa se detiene y no guarda nada. |
| `"column": "tipo_compra"` | La columna que falló. |
| `"check": "isin(['Bolsa', 'Contrato'])"` | La regla que falló: es `Check.isin(TIPOS_COMPRA)` de `esquemas.py`. |
| `"check": "greater_than_or_equal_to(0)"` | La otra regla que falló: es `Check.ge(0)` de `energia_kwh` (*ge* = *greater than or equal*, mayor o igual). |
| `failure cases: CONTRATOS, bolsa` | Los valores exactos que no cumplen. |
| Dos errores juntos | Por `lazy=True`: pandera revisa todo y muestra todos los errores de una vez. |

> 💡 Este experimento **no cambia ningún archivo**: dañó una copia en memoria. Por eso pandera es la "aduana" entre plata y oro: si alguien cambia el código de limpieza y deja pasar un error, el programa lo detiene antes de que llegue al dashboard.

**¿Cuándo guarda y dónde?** Es **todo o nada**: si pandera encuentra aunque sea 1 error, el programa se detiene y no guarda nada. Si encuentra 0 errores, guarda 3 archivos:

```text
observatorio-energia/
├── data/
│   └── silver/
│       ├── enerandes_ventas.parquet      ← las 1.064 ventas limpias (no se sube a GitHub)
│       └── enerandes_cuarentena.parquet  ← las 16 ventas apartadas (no se sube a GitHub)
└── docs/
    └── reporte_calidad.md                ← los 9 problemas con su regla, antes y después (sí se sube)
```

Las carpetas las dicen `DIR_SILVER` y `DIR_DOCS` en `src/config.py` (paso 0.3). Los `.parquet` no se suben porque `data/silver/` está en `.gitignore`: se vuelven a crear con `python -m src.silver.enerandes`.

**No confundir la cuarentena con un error de pandera:**

| | Cuarentena | Error de pandera |
|---|---|---|
| Quién lo decide | La limpieza (`enerandes.py`, regla 8) | La revisión final (`esquemas.py`) |
| Qué pasa | Esas filas se apartan y el programa **sigue** | El programa **se detiene** y no guarda nada |
| Para qué | Datos malos que **ya se esperaban** (energía vacía o negativa) | Errores que **no deberían existir** después de limpiar |

### 2.7 Probar las reglas de limpieza con pytest

pandera revisa **los datos**. Falta revisar **el código**: que cada regla de limpieza haga lo que debe. Eso se hace con **pruebas automáticas**.

| Concepto | Qué es | Ejemplo |
|---|---|---|
| **Prueba automática** (*test*) | Un programa pequeño que ejecuta una función del proyecto con datos de ejemplo y comprueba que el resultado es el esperado. | Darle `" ITAGÜÍ "` a `sin_tildes()` y comprobar que devuelve `"itagui"`. |
| **Prueba unitaria** | Una prueba de **una sola** función, con datos pequeños escritos en la misma prueba. No necesita internet ni archivos. | Las 6 pruebas de esta sección. |
| **`assert`** | La instrucción de Python que comprueba algo: si es verdad, sigue; si no, la prueba falla. | `assert sin_tildes("Medellín") == "medellin"` |
| **pytest** | La librería que busca las pruebas (funciones que empiezan por `test_`, en archivos `test_*.py`) y las ejecuta todas. | `python -m pytest -v` |

**Las 3 partes de toda prueba: Arrange, Act, Assert (Preparar, Ejecutar, Comprobar).** Cada prueba se escribe siempre en el mismo orden. En el código, cada parte lleva su comentario: `# 1. Arrange (Preparar)`, `# 2. Act (Ejecutar)` y `# 3. Assert (Comprobar)`.

| Parte | Qué se hace | En inglés se dice | Ejemplo en `test_energia_negativa_va_a_cuarentena` |
|---|---|---|---|
| **1. Arrange (Preparar)** | Armar los datos de ejemplo: pocos, y con el caso que se quiere comprobar | *Arrange* | `hoja = hoja_de_ejemplo()`: una hoja chiquita con una energía de -300 |
| **2. Act (Ejecutar)** | Llamar a la función del proyecto con esos datos | *Act* | `_, cuarentena, _ = limpiar(hoja)` |
| **3. Assert (Comprobar)** | Escribir con `assert` qué resultado se espera | *Assert* | `assert len(cuarentena) == 1`: una sola fila en cuarentena, la de -300 |

**Act y Assert no son lo mismo:** en **Act** se **llama a la función** y se guarda lo que devuelve; en **Assert** no se llama a nada: **solo se compara** lo que devolvió con lo esperado. Es como probar una calculadora:

| Parte | Con la calculadora |
|---|---|
| **Arrange** (Preparar) | Usted sabe que va a sumar 2 + 3 y que **debe dar 5**. |
| **Act** (Ejecutar) | Teclea `2 + 3 =` y **la calculadora trabaja**: muestra 5. |
| **Assert** (Comprobar) | **Usted solo mira** la pantalla y compara: ¿muestra 5? Sí → la calculadora funciona. |

> 💡 En `test_pandera_rechaza_un_tipo_de_compra_invalido`, ejecutar y comprobar van juntos: `with pytest.raises(...)` ejecuta la validación y, a la vez, comprueba que salga el error.

**¿Qué significa que una prueba falle?**

| Pregunta | Respuesta |
|---|---|
| ¿Qué es que falle? | Que la función devolvió **otra cosa** de la esperada. Por ejemplo, `sin_tildes(" ITAGÜÍ ")` devolvió `"ITAGÜÍ"` en vez de `"itagui"`. |
| ¿Dónde se ve? | En la terminal, al ejecutar `python -m pytest -v`: sale `FAILED` en rojo en vez de `PASSED`. |
| ¿Quién lo ve? | El programador que ejecutó las pruebas. En la Evidencia 3, también GitHub Actions, que las ejecuta solo en cada Pull Request. |
| ¿Quién corrige? | El programador: arregla **el código** (`enerandes.py`), no la prueba. Luego vuelve a ejecutar las pruebas hasta que pasen todas. |

Así se vería un fallo:

```text
FAILED tests/test_limpieza.py::test_sin_tildes_quita_tildes_mayusculas_y_espacios
    assert resultado1 == "itagui"
E   AssertionError: assert 'ITAGÜÍ' == 'itagui'
```

| Línea | Qué dice |
|---|---|
| `FAILED ...test_sin_tildes...` | Cuál prueba falló. |
| `assert resultado1 == "itagui"` | Cuál línea de la prueba falló. |
| `'ITAGÜÍ' == 'itagui'` | Lo que salió (izquierda) frente a lo que se esperaba (derecha). |

**Creen el archivo `tests/test_limpieza.py` y peguen este código:**

```python
"""
Pruebas automaticas de la capa plata (reglas de limpieza de EnerAndes).

Cada prueba es una funcion que empieza por test_. Prepara unos datos de
ejemplo pequenos, ejecuta una funcion del proyecto y comprueba con assert
que el resultado es el esperado. No necesitan internet ni los archivos de
data/: se ejecutan en segundos.

Uso:
    python -m pytest -v
"""
# ---------------------------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------------------------
import pandas as pd     # pandas: para armar una tabla de ejemplo
import pandera.errors   # los errores que lanza pandera cuando una regla falla
import pytest           # pytest: la libreria que encuentra y ejecuta las pruebas

from src.quality.esquemas import ESQUEMA_VENTAS               # el esquema de la capa plata
from src.silver.enerandes import clave_municipio, limpiar, sin_tildes   # lo que se prueba


# ---------------------------------------------------------------------------
# DATOS DE EJEMPLO
# ---------------------------------------------------------------------------
def hoja_de_ejemplo() -> pd.DataFrame:
    """Una hoja 2023 en miniatura, como queda en bronce: encabezado como fila,
    una fila repetida, una energia negativa y la fila TOTAL."""
    # Una lista de listas: cada lista de adentro es una fila de la hoja.
    # Todo va entre comillas (texto), como llega del Excel; None es una celda vacia
    filas = [
        ["Fecha", "Municipio", "Segmento", "Tipo_Compra", "Energia_kWh", "Valor_COP", "Clientes"],
        ["2023-01", "Medellín", "Residencial", "Contrato", "1000", "900000", "10"],
        ["2023-01", "Medellín", "Residencial", "Contrato", "1000", "900000", "10"],   # repetida
        ["2023-01", "ITAGUI", "RESID.", "bolsa", "500", "450000", "5"],
        ["2023-02", "Rio Negro", "IND", "CONTRATOS", "-300", "270000", "2"],         # negativa
        ["TOTAL", None, None, None, "1200", "1620000", "17"],                        # total
    ]
    # pd.DataFrame(filas, columns=...) convierte la lista en una tabla.
    # [f"col_{i}" for i in range(7)] arma los nombres col_0 ... col_6, igual que en bronce
    return pd.DataFrame(filas, columns=[f"col_{i}" for i in range(7)])


# ---------------------------------------------------------------------------
# PRUEBAS
# ---------------------------------------------------------------------------
def test_sin_tildes_quita_tildes_mayusculas_y_espacios():
    # 1. Arrange (Preparar): dos textos escritos "mal": con espacios, mayusculas y tildes
    texto1 = " ITAGÜÍ "
    texto2 = "Medellín"
    # 2. Act (Ejecutar): la funcion que se prueba, con cada texto
    resultado1 = sin_tildes(texto1)
    resultado2 = sin_tildes(texto2)
    # 3. Assert (Comprobar): assert A == B: si A es igual a B, sigue; si no, la prueba falla.
    # Los dos deben quedar sin espacios, sin tildes y en minuscula
    assert resultado1 == "itagui"
    assert resultado2 == "medellin"


def test_clave_municipio_resuelve_los_alias():
    # 1. Arrange (Preparar): dos alias de la lista ALIAS_MUNICIPIO y una celda vacia (None)
    alias1 = "Rio Negro"
    alias2 = "Medellín D.E."
    vacio = None
    # 2. Act (Ejecutar): la funcion que se prueba, con cada valor
    clave1 = clave_municipio(alias1)
    clave2 = clave_municipio(alias2)
    clave3 = clave_municipio(vacio)
    # 3. Assert (Comprobar): cada alias da su clave; la celda vacia da None.
    # "is None" pregunta si no tiene valor
    assert clave1 == "rionegro"
    assert clave2 == "medellin"
    assert clave3 is None


def test_limpiar_quita_encabezado_total_y_duplicados():
    # 1. Arrange (Preparar): la hoja 2023 en miniatura (con encabezado, TOTAL y una repetida)
    hoja = hoja_de_ejemplo()
    # 2. Act (Ejecutar): la limpieza completa. limpiar() devuelve tres cosas
    # y se reciben en tres variables
    limpias, cuarentena, metricas = limpiar(hoja)
    # 3. Assert (Comprobar): len(limpias) es el numero de filas.
    # 5 filas de datos - 1 TOTAL - 1 repetida - 1 negativa = 2 limpias
    assert len(limpias) == 2
    # .values son los valores de la columna periodo; "not in" pregunta que NO este
    assert "TOTAL" not in limpias["periodo"].values


def test_limpiar_unifica_valores_y_pone_divipola():
    # 1. Arrange (Preparar): la hoja en miniatura (trae 'ITAGUI', 'RESID.' y 'bolsa')
    hoja = hoja_de_ejemplo()
    # 2. Act (Ejecutar): la limpieza. El _ recibe lo que esta prueba no necesita
    # (cuarentena y metricas)
    limpias, _, _ = limpiar(hoja)
    # limpias["municipio"] == "Itagüí" da True en las filas de Itagui;
    # limpias[...] deja solo esas filas; .iloc[0] toma la primera (posicion 0)
    itagui = limpias[limpias["municipio"] == "Itagüí"].iloc[0]
    # 3. Assert (Comprobar): 'ITAGUI' recibio su codigo DIVIPOLA,
    # 'RESID.' quedo como 'Residencial' y 'bolsa' como 'Bolsa'
    assert itagui["divipola"] == "05360"
    assert itagui["segmento"] == "Residencial"
    assert itagui["tipo_compra"] == "Bolsa"


def test_energia_negativa_va_a_cuarentena():
    # 1. Arrange (Preparar): la hoja en miniatura (trae una energia de -300)
    hoja = hoja_de_ejemplo()
    # 2. Act (Ejecutar): la limpieza. Esta prueba solo necesita la cuarentena: lo demas va a _
    _, cuarentena, _ = limpiar(hoja)
    # 3. Assert (Comprobar): solo una fila tenia energia negativa, y es la de -300.
    # .iloc[0] es la primera fila de la cuarentena
    assert len(cuarentena) == 1
    assert cuarentena.iloc[0]["energia_kwh"] == -300


def test_pandera_rechaza_un_tipo_de_compra_invalido():
    # 1. Arrange (Preparar): una tabla limpia, y se le dana a proposito una celda.
    # .loc[0, "tipo_compra"] es la celda de la fila 0, columna tipo_compra;
    # se le pone un valor que no esta permitido
    limpias, _, _ = limpiar(hoja_de_ejemplo())
    limpias.loc[0, "tipo_compra"] = "CONTRATOS"
    # 2. Act (Ejecutar) y 3. Assert (Comprobar) van juntos en esta prueba:
    # with pytest.raises(...): la prueba ESPERA ese error dentro del bloque.
    # Si pandera lanza SchemaErrors, la prueba pasa; si no lo lanza, falla
    with pytest.raises(pandera.errors.SchemaErrors):
        # Revisa la tabla danada con las reglas de pandera
        ESQUEMA_VENTAS.validate(limpias, lazy=True)
```

| Parte | Qué hace |
|---|---|
| `hoja_de_ejemplo()` | Arma una hoja 2023 **en miniatura** (6 filas) con un error de cada tipo: el encabezado como fila, una fila repetida, `ITAGUI`, `RESID.`, `bolsa`, `Rio Negro`, `CONTRATOS`, una energía negativa y la fila `TOTAL`. Así cada prueba sabe exactamente qué debe salir. |
| `def test_...():` | Cada función que empieza por `test_` es una prueba. El nombre dice **qué** se comprueba. |
| `assert sin_tildes(" ITAGÜÍ ") == "itagui"` | Si `sin_tildes` devuelve otra cosa, la prueba falla y pytest muestra qué salió y qué se esperaba. |
| `limpias, cuarentena, metricas = limpiar(...)` | Ejecuta la limpieza completa sobre la hoja en miniatura. |
| `assert len(limpias) == 2` | De las 5 filas de datos, quedan 2: se fueron la `TOTAL`, la repetida y la negativa. |
| `limpias, _, _ = limpiar(...)` | El guion bajo `_` recibe lo que esta prueba no necesita. |
| `pytest.raises(pandera.errors.SchemaErrors)` | Esta prueba **espera** un error: pasa solo si pandera rechaza el `CONTRATOS` puesto a propósito. |

**Ejecutarlas:**

```powershell
python -m pytest -v
```

| Parte | Qué significa |
|---|---|
| `python -m pytest` | Ejecuta pytest como módulo de Python. Así las pruebas encuentran la carpeta `src` (ver la nota al final de esta sección). |
| `-v` | *verbose*: muestra el nombre de cada prueba y si pasó, en vez de solo un punto por prueba. |

**Resultado:**

```text
============================= test session starts =============================
platform win32 -- Python 3.14.0, pytest-9.1.1, pluggy-1.7.0 -- C:\clases\observatorio-energia\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\clases\observatorio-energia
plugins: typeguard-4.6.0
collected 6 items

tests/test_limpieza.py::test_sin_tildes_quita_tildes_mayusculas_y_espacios PASSED [ 16%]
tests/test_limpieza.py::test_clave_municipio_resuelve_los_alias PASSED   [ 33%]
tests/test_limpieza.py::test_limpiar_quita_encabezado_total_y_duplicados PASSED [ 50%]
tests/test_limpieza.py::test_limpiar_unifica_valores_y_pone_divipola PASSED [ 66%]
tests/test_limpieza.py::test_energia_negativa_va_a_cuarentena PASSED     [ 83%]
tests/test_limpieza.py::test_pandera_rechaza_un_tipo_de_compra_invalido PASSED [100%]

============================== 6 passed in 1.89s ==============================
```

| Lo que aparece | Qué significa |
|---|---|
| `platform win32 -- Python 3.14.0, pytest-9.1.1` | El sistema (Windows), la versión de Python y la de pytest. Al final, el Python que usó: el de `.venv`. |
| `cachedir: .pytest_cache` | La carpeta donde pytest guarda datos entre ejecuciones. La crea solo y trae su propio `.gitignore`: no se sube a GitHub. |
| `rootdir: C:\clases\observatorio-energia` | La carpeta del proyecto: desde ahí busca las pruebas. |
| `plugins: typeguard-4.6.0` | Un complemento de pytest que llegó instalado con pandera. No hay que hacer nada con él. |
| `collected 6 items` | pytest encontró 6 pruebas. Si el equipo tiene las pruebas de la Evidencia 1 en `tests/`, el número es mayor: se ejecutan todas juntas. |
| `PASSED` | La prueba pasó: la función hizo lo que debía. |
| `[ 16%]` … `[100%]` | El avance. |
| `6 passed in 1.89s` | Todas pasaron, en 2 segundos: no necesitan internet ni los archivos de `data/`. |

> 💡 **`python -m pytest` y no solo `pytest`:** con `python -m`, Python agrega la carpeta del proyecto a su búsqueda, y las pruebas encuentran `src`. Sin eso puede salir `ModuleNotFoundError: No module named 'src'`.

### 2.8 ¿Para qué sirve una prueba? Romper una regla a propósito

Abran `src/silver/enerandes.py` y busquen la tabla `SEGMENTOS`. Su primera línea es:

```python
SEGMENTOS = {"residencial": "Residencial", "resid.": "Residencial",
```

**Borren** `"resid.": "Residencial",` (lo que está después de la primera coma), como si alguien lo hubiera borrado por error. La línea queda así:

```python
SEGMENTOS = {"residencial": "Residencial",
```

Guarden el cambio en `enerandes.py` con **Ctrl + S**. No se crea ningún archivo: se guarda el archivo que está abierto, ahora sin la regla. Si la pestaña dice `enerandes.py ●` (con punto), el cambio todavía no está guardado y pytest no lo ve.

Ejecuten las pruebas, esta vez sin `-v`, para ver el resumen corto (un punto por cada prueba que pasa y una `F` por cada una que falla):

```powershell
python -m pytest
```

**Resultado** (la parte final):

```text
============================= test session starts =============================
platform win32 -- Python 3.14.0, pytest-9.1.1, pluggy-1.7.0
rootdir: C:\clases\observatorio-energia
plugins: typeguard-4.6.0
collected 6 items

tests\test_limpieza.py ...F..                                            [100%]

================================== FAILURES ===================================
________________ test_limpiar_unifica_valores_y_pone_divipola _________________

    def test_limpiar_unifica_valores_y_pone_divipola():
        # 1. Arrange (Preparar): la hoja en miniatura (trae 'ITAGUI', 'RESID.' y 'bolsa')
        hoja = hoja_de_ejemplo()
        # 2. Act (Ejecutar): la limpieza. El _ recibe lo que esta prueba no necesita
        # (cuarentena y metricas)
        limpias, _, _ = limpiar(hoja)
        # limpias["municipio"] == "Itagüí" da True en las filas de Itagui;
        # limpias[...] deja solo esas filas; .iloc[0] toma la primera (posicion 0)
        itagui = limpias[limpias["municipio"] == "Itagüí"].iloc[0]
        # 3. Assert (Comprobar): 'ITAGUI' recibio su codigo DIVIPOLA,
        # 'RESID.' quedo como 'Residencial' y 'bolsa' como 'Bolsa'
        assert itagui["divipola"] == "05360"
>       assert itagui["segmento"] == "Residencial"
E       AssertionError: assert 'No informado' == 'Residencial'
E
E         - Residencial
E         + No informado

tests\test_limpieza.py:101: AssertionError
=========================== short test summary info ===========================
FAILED tests/test_limpieza.py::test_limpiar_unifica_valores_y_pone_divipola - AssertionError: assert 'No informado' == 'Residencial'
========================= 1 failed, 5 passed in 1.95s =========================
```

| Lo que aparece | Qué significa |
|---|---|
| `rootdir`, `plugins` | La carpeta del proyecto y el complemento de pytest, como en el paso 2.7. |
| `...F..` | Un punto por cada prueba que pasó; `F` (*failed*) en la que falló. |
| `>` | La línea exacta donde falló el `assert`. |
| `assert 'No informado' == 'Residencial'` | Se esperaba `Residencial` y salió `No informado`. |
| `- Residencial` / `+ No informado` | `-` es lo esperado; `+` es lo que salió. |
| `tests\test_limpieza.py:101` | El archivo y el número de la línea donde falló la prueba. |
| `FAILED ... - AssertionError: ...` | El resumen final: qué prueba falló y por qué. |
| `1 failed, 5 passed` | Una regla quedó mal; las demás siguen bien. |
| Dónde falló | En el **Assert** (la línea con `>`): el Act sí se ejecutó, pero el resultado obtenido (`No informado`) no fue el esperado (`Residencial`). |

**¿Por qué es grave sin la prueba?** Sin `"resid."`, el programa **no da error**: las 17 ventas escritas `RESID.` pasan como `No informado`, pandera las acepta (es un valor permitido) y el dashboard muestra menos ventas residenciales. Nadie lo nota. **La prueba sí lo nota.**

Ahora **vuelvan a poner** la regla, para que la línea quede otra vez así:

```python
SEGMENTOS = {"residencial": "Residencial", "resid.": "Residencial",
```

Guarden y ejecuten otra vez:

```powershell
python -m pytest
```

**Resultado:**

```text
============================= test session starts =============================
platform win32 -- Python 3.14.0, pytest-9.1.1, pluggy-1.7.0
rootdir: C:\clases\observatorio-energia
plugins: typeguard-4.6.0
collected 6 items

tests\test_limpieza.py ......                                           [100%]

============================== 6 passed in 1.42s ==============================
```

| Lo que aparece | Qué significa |
|---|---|
| `......` | 6 puntos: las 6 pruebas pasaron. Ya no hay `F`. |
| `6 passed` | La regla quedó otra vez bien: `RESID.` vuelve a quedar como `Residencial`. |
| No aparece la sección `FAILURES` | Solo sale cuando alguna prueba falla. |


| | pandera | pytest |
|---|---|---|
| Qué revisa | **Los datos**: cada fila de la tabla limpia | **El código**: cada función de limpieza |
| Con qué datos | Los datos reales, cada vez que se limpia | Datos de ejemplo pequeños, escritos en la prueba |
| Cuándo se ejecuta | Al limpiar, antes de guardar en plata | Cada vez que se cambia el código (y en la entrega final, solo, en GitHub Actions) |

### 2.9 Escribir una prueba nueva, paso a paso

La Evidencia 2 pide **mínimo 5 pruebas nuevas** sobre las reglas del equipo. Esta sección muestra cómo se escribe una desde cero.

#### Las reglas de nombres de pytest

pytest no ejecuta cualquier función: busca por el **nombre**. Si el nombre no cumple, la prueba no se ejecuta y **no avisa**.

| Qué | Regla | Ejemplo | Qué pasa si no se cumple |
|---|---|---|---|
| Carpeta | Las pruebas van en `tests/`, en la raíz del proyecto | `tests/` | — |
| Archivo | El nombre empieza por `test_` | `test_limpieza.py` | pytest no lo encuentra: `collected 0 items` y `no tests ran` |
| Función | El nombre empieza por `test_` | `def test_total_en_minuscula_tambien_se_elimina():` | pytest la ignora: no aparece en la cuenta de pruebas |
| Nombre de la función | Dice **qué** se comprueba, en palabras | `test_energia_negativa_va_a_cuarentena` | Funciona, pero cuando falle nadie sabrá qué se rompió |

#### Las 3 partes de toda prueba

| Parte | Qué se hace | En inglés se dice |
|---|---|---|
| **1. Arrange (Preparar)** | Escribir los datos de ejemplo: pocos, y con el caso que se quiere comprobar | *Arrange* |
| **2. Act (Ejecutar)** | Llamar a la función del proyecto con esos datos | *Act* |
| **3. Assert (Comprobar)** | Escribir con `assert` qué resultado se espera | *Assert* |

#### 2.9.1 Decidir qué se quiere comprobar

La regla 2 quita la fila `TOTAL`. Pero en otra hoja del Excel podría venir escrita `total` o `Total`. El código usa `.str.upper()` (pasa a mayúscula) antes de comparar, así que **debería** quitarla también. Una prueba lo demuestra, y además avisa si un día alguien quita el `.str.upper()`.

| Parte | En esta prueba |
|---|---|
| 1. Arrange (Preparar) | La hoja de ejemplo, con la fila de totales escrita `total`, en minúscula |
| 2. Act (Ejecutar) | `limpiar(hoja)` |
| 3. Assert (Comprobar) | Quedan 2 filas limpias, igual que con `TOTAL` en mayúscula |

#### 2.9.2 Escribir la prueba

Abran `tests/test_limpieza.py`, **borren todo** y peguen el archivo completo. Lo nuevo es la última función, `test_total_en_minuscula_tambien_se_elimina`:

```python
"""
Pruebas automaticas de la capa plata (reglas de limpieza de EnerAndes).

Cada prueba es una funcion que empieza por test_. Prepara unos datos de
ejemplo pequenos, ejecuta una funcion del proyecto y comprueba con assert
que el resultado es el esperado. No necesitan internet ni los archivos de
data/: se ejecutan en segundos.

Uso:
    python -m pytest -v
"""
# ---------------------------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------------------------
import pandas as pd     # pandas: para armar una tabla de ejemplo
import pandera.errors   # los errores que lanza pandera cuando una regla falla
import pytest           # pytest: la libreria que encuentra y ejecuta las pruebas

from src.quality.esquemas import ESQUEMA_VENTAS               # el esquema de la capa plata
from src.silver.enerandes import clave_municipio, limpiar, sin_tildes   # lo que se prueba


# ---------------------------------------------------------------------------
# DATOS DE EJEMPLO
# ---------------------------------------------------------------------------
def hoja_de_ejemplo() -> pd.DataFrame:
    """Una hoja 2023 en miniatura, como queda en bronce: encabezado como fila,
    una fila repetida, una energia negativa y la fila TOTAL."""
    # Una lista de listas: cada lista de adentro es una fila de la hoja.
    # Todo va entre comillas (texto), como llega del Excel; None es una celda vacia
    filas = [
        ["Fecha", "Municipio", "Segmento", "Tipo_Compra", "Energia_kWh", "Valor_COP", "Clientes"],
        ["2023-01", "Medellín", "Residencial", "Contrato", "1000", "900000", "10"],
        ["2023-01", "Medellín", "Residencial", "Contrato", "1000", "900000", "10"],   # repetida
        ["2023-01", "ITAGUI", "RESID.", "bolsa", "500", "450000", "5"],
        ["2023-02", "Rio Negro", "IND", "CONTRATOS", "-300", "270000", "2"],         # negativa
        ["TOTAL", None, None, None, "1200", "1620000", "17"],                        # total
    ]
    # pd.DataFrame(filas, columns=...) convierte la lista en una tabla.
    # [f"col_{i}" for i in range(7)] arma los nombres col_0 ... col_6, igual que en bronce
    return pd.DataFrame(filas, columns=[f"col_{i}" for i in range(7)])


# ---------------------------------------------------------------------------
# PRUEBAS
# ---------------------------------------------------------------------------
def test_sin_tildes_quita_tildes_mayusculas_y_espacios():
    # 1. Arrange (Preparar): dos textos escritos "mal": con espacios, mayusculas y tildes
    texto1 = " ITAGÜÍ "
    texto2 = "Medellín"
    # 2. Act (Ejecutar): la funcion que se prueba, con cada texto
    resultado1 = sin_tildes(texto1)
    resultado2 = sin_tildes(texto2)
    # 3. Assert (Comprobar): assert A == B: si A es igual a B, sigue; si no, la prueba falla.
    # Los dos deben quedar sin espacios, sin tildes y en minuscula
    assert resultado1 == "itagui"
    assert resultado2 == "medellin"


def test_clave_municipio_resuelve_los_alias():
    # 1. Arrange (Preparar): dos alias de la lista ALIAS_MUNICIPIO y una celda vacia (None)
    alias1 = "Rio Negro"
    alias2 = "Medellín D.E."
    vacio = None
    # 2. Act (Ejecutar): la funcion que se prueba, con cada valor
    clave1 = clave_municipio(alias1)
    clave2 = clave_municipio(alias2)
    clave3 = clave_municipio(vacio)
    # 3. Assert (Comprobar): cada alias da su clave; la celda vacia da None.
    # "is None" pregunta si no tiene valor
    assert clave1 == "rionegro"
    assert clave2 == "medellin"
    assert clave3 is None


def test_limpiar_quita_encabezado_total_y_duplicados():
    # 1. Arrange (Preparar): la hoja 2023 en miniatura (con encabezado, TOTAL y una repetida)
    hoja = hoja_de_ejemplo()
    # 2. Act (Ejecutar): la limpieza completa. limpiar() devuelve tres cosas
    # y se reciben en tres variables
    limpias, cuarentena, metricas = limpiar(hoja)
    # 3. Assert (Comprobar): len(limpias) es el numero de filas.
    # 5 filas de datos - 1 TOTAL - 1 repetida - 1 negativa = 2 limpias
    assert len(limpias) == 2
    # .values son los valores de la columna periodo; "not in" pregunta que NO este
    assert "TOTAL" not in limpias["periodo"].values


def test_limpiar_unifica_valores_y_pone_divipola():
    # 1. Arrange (Preparar): la hoja en miniatura (trae 'ITAGUI', 'RESID.' y 'bolsa')
    hoja = hoja_de_ejemplo()
    # 2. Act (Ejecutar): la limpieza. El _ recibe lo que esta prueba no necesita
    # (cuarentena y metricas)
    limpias, _, _ = limpiar(hoja)
    # limpias["municipio"] == "Itagüí" da True en las filas de Itagui;
    # limpias[...] deja solo esas filas; .iloc[0] toma la primera (posicion 0)
    itagui = limpias[limpias["municipio"] == "Itagüí"].iloc[0]
    # 3. Assert (Comprobar): 'ITAGUI' recibio su codigo DIVIPOLA,
    # 'RESID.' quedo como 'Residencial' y 'bolsa' como 'Bolsa'
    assert itagui["divipola"] == "05360"
    assert itagui["segmento"] == "Residencial"
    assert itagui["tipo_compra"] == "Bolsa"


def test_energia_negativa_va_a_cuarentena():
    # 1. Arrange (Preparar): la hoja en miniatura (trae una energia de -300)
    hoja = hoja_de_ejemplo()
    # 2. Act (Ejecutar): la limpieza. Esta prueba solo necesita la cuarentena: lo demas va a _
    _, cuarentena, _ = limpiar(hoja)
    # 3. Assert (Comprobar): solo una fila tenia energia negativa, y es la de -300.
    # .iloc[0] es la primera fila de la cuarentena
    assert len(cuarentena) == 1
    assert cuarentena.iloc[0]["energia_kwh"] == -300


def test_pandera_rechaza_un_tipo_de_compra_invalido():
    # 1. Arrange (Preparar): una tabla limpia, y se le dana a proposito una celda.
    # .loc[0, "tipo_compra"] es la celda de la fila 0, columna tipo_compra;
    # se le pone un valor que no esta permitido
    limpias, _, _ = limpiar(hoja_de_ejemplo())
    limpias.loc[0, "tipo_compra"] = "CONTRATOS"
    # 2. Act (Ejecutar) y 3. Assert (Comprobar) van juntos en esta prueba:
    # with pytest.raises(...): la prueba ESPERA ese error dentro del bloque.
    # Si pandera lanza SchemaErrors, la prueba pasa; si no lo lanza, falla
    with pytest.raises(pandera.errors.SchemaErrors):
        # Revisa la tabla danada con las reglas de pandera
        ESQUEMA_VENTAS.validate(limpias, lazy=True)


def test_total_en_minuscula_tambien_se_elimina():
    # 1. Arrange (Preparar): la hoja de ejemplo, con la fila de totales escrita "total".
    # hoja.loc[5, "col_0"] es la celda de la fila 5 (la de totales), columna col_0;
    # se cambia de "TOTAL" a "total"
    hoja = hoja_de_ejemplo()
    hoja.loc[5, "col_0"] = "total"
    # 2. Act (Ejecutar): la limpieza completa sobre esa hoja
    limpias, _, _ = limpiar(hoja)
    # 3. Assert (Comprobar): quedan las mismas 2 filas; si la fila "total" no se hubiera
    # quitado, habria 3 y la prueba fallaria
    assert len(limpias) == 2
```

**Lo que se agregó:**

| Línea | Qué hace |
|---|---|
| `def test_total_en_minuscula_tambien_se_elimina():` | Una función nueva. Empieza por `test_`, así que pytest la encuentra. |
| `hoja = hoja_de_ejemplo()` | **Arrange (Preparar):** usa la misma hoja en miniatura de las otras pruebas. Así no hay que volver a escribir las 6 filas. |
| `hoja.loc[5, "col_0"] = "total"` | **Arrange (Preparar):** cambia la fila 5 (la de totales), columna `col_0`, de `TOTAL` a `total`. `.loc[fila, columna]` cambia una celda. |
| `limpias, _, _ = limpiar(hoja)` | **Act (Ejecutar):** la limpieza completa. |
| `assert len(limpias) == 2` | **Assert (Comprobar):** si la fila `total` no se hubiera quitado, habría 3 filas y la prueba fallaría. |
| Los comentarios `# 1.`, `# 2.`, `# 3.` | Marcan las 3 partes. Así cualquiera del equipo entiende la prueba. |

#### 2.9.3 Ejecutar solo la prueba nueva

Mientras se escribe una prueba, se ejecuta **sola**, para ver rápido si pasa sin esperar a las demás:

```powershell
python -m pytest -v -k minuscula
```

| Parte | Qué significa |
|---|---|
| `python -m pytest` | Ejecuta pytest como módulo de Python, desde la carpeta del proyecto: así las pruebas encuentran `src`. |
| `-v` | *verbose* (detallado): en vez de un punto, muestra el **nombre** de cada prueba y si pasó (`PASSED`) o falló (`FAILED`). |
| `-k minuscula` | *keyword* (palabra clave): ejecuta solo las pruebas cuyo nombre contiene la palabra `minuscula`. Aquí es una sola: `test_total_en_minuscula_tambien_se_elimina`. |

`-k` es un **filtro por nombre**, como el buscador de una carpeta: se escribe una palabra y solo se ejecutan las pruebas que la tienen en el nombre.

| # | Nombre de la prueba | ¿Tiene la palabra `minuscula`? |
|---|---|---|
| 1 | `test_sin_tildes_quita_tildes_mayusculas_y_espacios` | No |
| 2 | `test_clave_municipio_resuelve_los_alias` | No |
| 3 | `test_limpiar_quita_encabezado_total_y_duplicados` | No |
| 4 | `test_limpiar_unifica_valores_y_pone_divipola` | No |
| 5 | `test_energia_negativa_va_a_cuarentena` | No |
| 6 | `test_pandera_rechaza_un_tipo_de_compra_invalido` | No |
| 7 | `test_total_en_minuscula_tambien_se_elimina` | **Sí**: solo esta se ejecuta |

**Resultado:**

```text
============================= test session starts =============================
platform win32 -- Python 3.14.0, pytest-9.1.1, pluggy-1.7.0 -- C:\clases\observatorio-energia\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\clases\observatorio-energia
plugins: typeguard-4.6.0
collected 7 items / 6 deselected / 1 selected

tests/test_limpieza.py::test_total_en_minuscula_tambien_se_elimina PASSED [100%]

======================= 1 passed, 6 deselected in 2.24s =======================
```

| Lo que aparece | Qué significa |
|---|---|
| Las 4 primeras líneas | Las mismas del paso 2.7: el Python de `.venv`, la carpeta del proyecto y el complemento de pytest. |
| `collected 7 items` | Ahora hay 7 pruebas: las 6 de la clase y la nueva. |
| `6 deselected / 1 selected` | *Deselected* = no seleccionadas: 6 pruebas **no se ejecutaron esta vez**, porque no tienen `minuscula` en el nombre. Ni pasaron ni fallaron: no corrieron. Siguen en el archivo, intactas. *Selected* = seleccionada: 1 sí se ejecutó. |
| `PASSED` | La regla 2 sí quita la fila de totales en minúscula. |

> ⚠️ **Cuidado con la palabra del `-k`:** `-k total` ejecutaría 2 pruebas, porque `total` también está en el nombre de `test_limpiar_quita_encabezado_total_y_duplicados`. Usen una palabra que esté **solo** en la prueba que quieren.

#### 2.9.4 Ejecutar todas las pruebas

Antes de hacer commit, siempre se ejecutan **todas**, para comprobar que lo nuevo no dañó nada. Es el mismo comando, sin `-k` (para que se ejecuten todas) y sin `-v` (para ver solo el resumen corto, un punto por prueba):

```powershell
python -m pytest
```

**Resultado:**

```text
============================= test session starts =============================
platform win32 -- Python 3.14.0, pytest-9.1.1, pluggy-1.7.0
rootdir: C:\clases\observatorio-energia
plugins: typeguard-4.6.0
collected 7 items

tests\test_limpieza.py .......                                           [100%]

============================== 7 passed in 1.72s ==============================
```

| Lo que aparece | Qué significa |
|---|---|
| `.......` | 7 puntos: 7 pruebas que pasaron. |
| `7 passed` | Todas pasan. Ya se puede hacer commit. |

**Commit de la capa plata.** Con las pruebas en verde, guarden y suban lo hecho hasta aquí (los 3 comandos van en una sola línea; el `;` los ejecuta uno detrás de otro):

```powershell
git add . ; git commit -m "feat: capa plata con limpieza, reglas de pandera y 7 pruebas" ; git push -u origin feature/plata-oro
```

| Parte | Qué hace |
|---|---|
| `git add .` | Prepara todos los cambios para el commit. |
| `git commit -m "..."` | Guarda los cambios con un mensaje que dice qué se hizo. `feat:` indica que es una funcionalidad nueva. |
| `git push -u origin feature/plata-oro` | Sube el commit a GitHub. Como es la **primera vez** que se sube esta rama, se escribe `-u origin` y el nombre de la rama: `-u` conecta la rama del computador con la de GitHub. Desde ahí, basta con `git push`. Si le pusieron su nombre a la rama (paso 0.1), escriban ese nombre. |

> 💡 **Un commit por cada parte terminada**, no uno solo al final: así, si algo se daña, se sabe en qué parte fue, y GitHub muestra el trabajo repartido en el tiempo. Al terminar la capa oro (sección 3.6) se hace otro commit.

#### 2.9.5 Escribir las pruebas de las reglas del equipo

Para las reglas nuevas de la Evidencia 2 se sigue la misma forma. Esta es la **plantilla** (los nombres son de ejemplo: cada equipo usa los de sus funciones):

```python
from src.silver.mi_archivo import mi_funcion     # la funcion nueva del equipo


def test_lo_que_se_comprueba():
    # 1. Arrange (Preparar): los datos de ejemplo, pocos y con el caso a comprobar
    entrada = ...
    # 2. Act (Ejecutar): la funcion del proyecto
    resultado = mi_funcion(entrada)
    # 3. Assert (Comprobar): el resultado esperado
    assert resultado == ...
```

Ideas para las reglas que pide la Evidencia 2:

| Regla del equipo | Qué se prepara | Qué se comprueba con `assert` |
|---|---|---|
| Convertir MWh a kWh (hoja 2024) | Una fila con `1.5` y unidad `MWh` | La energía queda en `1500` |
| Leer la fecha `mar-24` | El texto `"mar-24"` | El periodo queda `"2024-03"` |
| Leer la fecha `03/2024` | El texto `"03/2024"` | El periodo queda `"2024-03"` |
| Leer la fecha de corte `01/03/2026` (hoja 2026) | El texto `"01/03/2026"` | El periodo queda `"2026-03"` (marzo, no enero) |
| Calcular la fase ENSO | Los ONI `0.7`, `-0.6` y `0.2` | Las fases quedan `El Niño`, `La Niña` y `Neutral` |
| Pasar XM de 24 columnas a una fila por hora | Una fila de un día con `Hour01` a `Hour24` | Quedan 24 filas, una por hora |
| Unificar los encabezados de la hoja 2024 | Una hoja con `PERIODO`, `MUNICIPIO`, `MODALIDAD`… | Las columnas quedan `periodo`, `municipio`, `tipo_compra`… |

> 💡 **Una prueba por cada caso.** Para la fase ENSO conviene escribir 3 pruebas (El Niño, La Niña y Neutral), o una prueba con 3 `assert`. Y no olviden el caso borde: ¿qué fase tiene un ONI de exactamente `0.5`?

#### 2.9.6 (Opcional) Muchos casos en una sola prueba: `parametrize`

> Esta sección es **opcional**: no se necesita para la Evidencia 2. Enseña una forma de escribir menos cuando se prueba la misma función con muchos datos.

Cuando se quiere probar la misma función con varios datos, no hace falta repetir las líneas (`texto1`, `texto2`, `resultado1`, `resultado2`…). Con `@pytest.mark.parametrize` se escribe **una lista de casos** y pytest ejecuta la prueba una vez por cada caso.

Al final de `tests/test_limpieza.py`, agreguen:

```python
# @pytest.mark.parametrize: ejecuta la prueba una vez por cada caso de la lista.
# "texto, esperado" son los nombres de los dos datos de cada caso
@pytest.mark.parametrize("texto, esperado", [
    (" ITAGÜÍ ", "itagui"),      # caso 1: espacios, mayusculas y tildes
    ("Medellín", "medellin"),    # caso 2: una sola tilde
    ("RIONEGRO", "rionegro"),    # caso 3: solo mayusculas. Un caso nuevo = una linea nueva
], ids=["itagui", "medellin", "rionegro"])   # ids: el nombre corto de cada caso en la salida
def test_sin_tildes_varios_casos(texto, esperado):
    # 1. Arrange (Preparar): lo hace parametrize: texto y esperado llegan de la lista
    # 2. Act (Ejecutar): la funcion que se prueba
    resultado = sin_tildes(texto)
    # 3. Assert (Comprobar): el resultado debe ser el esperado de ese caso
    assert resultado == esperado
```

| Parte | Qué hace |
|---|---|
| `@pytest.mark.parametrize(...)` | Se pone **encima** de la prueba, con `@`. Le dice a pytest: "ejecuta esta prueba con cada caso de la lista". |
| `"texto, esperado"` | Los nombres de los datos de cada caso. Son los mismos parámetros de la función: `def test_...(texto, esperado)`. |
| `(" ITAGÜÍ ", "itagui")` | Un caso: lo que entra y lo que debe salir. |
| `ids=[...]` | El nombre de cada caso en la salida. Es opcional; sin él, pytest muestra el texto completo, a veces con caracteres raros por las tildes. |

**Ejecutarla:**

```powershell
python -m pytest -v -k varios_casos
```

**Resultado:**

```text
tests/test_limpieza.py::test_sin_tildes_varios_casos[itagui] PASSED      [ 33%]
tests/test_limpieza.py::test_sin_tildes_varios_casos[medellin] PASSED    [ 66%]
tests/test_limpieza.py::test_sin_tildes_varios_casos[rionegro] PASSED    [100%]
```

| Lo que aparece | Qué significa |
|---|---|
| `[itagui]`, `[medellin]`, `[rionegro]` | Cada caso sale por separado, con su nombre de `ids`. |
| 3 líneas `PASSED` | pytest ejecutó la misma prueba 3 veces, una por caso. |

Si un caso falla, pytest dice **cuál**: por ejemplo, `FAILED tests/test_limpieza.py::test_sin_tildes_varios_casos[rionegro]`, y los otros dos siguen pasando.

| Sin `parametrize` | Con `parametrize` |
|---|---|
| Para un caso nuevo se copian varias líneas | Para un caso nuevo se agrega **una línea** a la lista |
| Si falla, hay que leer el error para saber qué dato fue | pytest dice el nombre del caso que falló |

#### Errores típicos al escribir pruebas

Estos son los mensajes reales:

**1. Ejecutar `pytest` en vez de `python -m pytest`:**

```text
tests\test_limpieza.py:19: in <module>
    from src.quality.esquemas import ESQUEMA_VENTAS               # el esquema de la capa plata
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   ModuleNotFoundError: No module named 'src'
=========================== short test summary info ===========================
ERROR tests/test_limpieza.py
!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
============================== 1 error in 1.77s ===============================
```

**2. El archivo no empieza por `test_`** (por ejemplo, `tests/pruebas_limpieza.py`):

```text
collected 0 items

============================ no tests ran in 0.03s ============================
```

**3. La función no empieza por `test_`** (por ejemplo, `def prueba_sin_tildes...`): pytest no da error, solo **no la cuenta**. Con 6 pruebas en el archivo y una mal nombrada, sale:

```text
============================== 5 passed in 1.71s ==============================
```

| Error | Causa | Solución |
|---|---|---|
| `ModuleNotFoundError: No module named 'src'` | Se ejecutó `pytest` solo: Python no encuentra la carpeta `src`. | Ejecutar `python -m pytest`, desde la raíz del proyecto. |
| `collected 0 items` y `no tests ran` | El archivo no empieza por `test_`, o no está en el proyecto. | Renombrarlo: `test_algo.py`. |
| Salen menos pruebas de las que se escribieron | Una función no empieza por `test_`. | Renombrarla: `def test_algo():`. Siempre revisen que el número de pruebas sea el esperado. |
| `AssertionError` | La función no devolvió lo esperado. | Leer la línea con `>` y las líneas `-` (esperado) y `+` (obtenido). Revisar **primero** si el error está en el código; solo si la prueba esperaba algo equivocado, se corrige la prueba. |
| `NameError: name 'limpiar' is not defined` | Falta el `import` de la función. | Agregarla en la línea `from src.silver.enerandes import ...`. |

#### Qué se hace y qué no con las pruebas

| ❌ No se hace | ✅ Sí se hace |
|---|---|
| Cambiar lo que espera la prueba para que pase. | Corregir el código que falla; la prueba se cambia solo si esperaba algo equivocado. |
| Usar los archivos reales de `data/` en las pruebas. | Escribir datos de ejemplo pequeños dentro de la prueba: así corren en segundos y sin internet. |
| Probar solo el caso fácil. | Probar también los casos raros: minúsculas, espacios, valores vacíos, el límite `0.5`. |
| Hacer commit sin ejecutar las pruebas. | Ejecutar `python -m pytest` antes de cada commit. |
| Una sola prueba gigante que comprueba todo. | Una prueba por regla, con un nombre que diga qué comprueba. |

### Qué se hace y qué no en la capa plata

| ❌ No se hace | ✅ Sí se hace |
|---|---|
| Corregir los datos a mano en el Excel. | Escribir cada corrección como una regla en el código. |
| Borrar filas malas sin dejar rastro. | Pasarlas a cuarentena y contarlas. |
| Inventar un valor que no se conoce (por ejemplo, poner 0 en la energía vacía). | Dejarlo vacío, marcarlo o apartarlo, y documentarlo. |
| Decir "limpiamos los datos" sin números. | Mostrar la métrica antes y después de cada regla. |
| Modificar la capa bronce. | Leer bronce y guardar el resultado en plata. |

---

## Parte 3 · Capa oro: el esquema estrella con dbt

### Idea central

Con los datos limpios, dbt construye 4 tablas en un archivo DuckDB (`data/observatorio.duckdb`): una de hechos y tres dimensiones. Cada tabla es un archivo `.sql`, y un archivo `schema.yml` dice qué pruebas debe pasar cada una.

### 3.1 Los archivos del proyecto dbt

> 💡 **¿Qué es un archivo `.yml`?** Es un archivo de texto para escribir **configuración**: no es un programa, no se ejecuta. Lo lee otro programa (aquí, dbt) para saber cómo trabajar. Se escribe con el formato **YAML**: `nombre: valor` en cada línea, y lo que va más adentro (con 2 espacios de sangría) pertenece a la línea de arriba. Por ejemplo, `name: observatorio` le dice a dbt que el proyecto se llama `observatorio`. El `#` es un comentario, igual que en Python.

| Pregunta | Respuesta |
|---|---|
| ¿Qué significa YAML? | *YAML Ain't Markup Language*: "YAML no es un lenguaje de marcado". Es un juego de palabras de sus creadores. |
| ¿Por qué `.yml` y no `.yaml`? | Las dos sirven; `.yml` es la versión corta, de 3 letras. dbt usa `.yml`. |
| ¿Quién más lo usa? | Muchas herramientas: GitHub Actions (Evidencia 3), Docker, Kubernetes… |
| ¿Es de Linux o de Docker? | No. YAML no es de ningún sistema ni de ningún programa: es un formato de texto libre y gratuito, creado en 2001, que funciona igual en Windows, Mac y Linux. Es como el `.csv`: Excel lo abre y pandas también, pero el `.csv` no es de Excel ni de pandas. Con YAML pasa lo mismo: cada herramienta lo lee para su propia configuración. |

> ⚠️ **La sangría importa:** si una línea se corre un espacio, dbt no la entiende y da error. Usen siempre 2 espacios, nunca la tecla Tab.

**¿Por qué `.yml` y no `.csv`?** Porque guardan cosas distintas. Un `.csv` guarda **datos**: muchas filas iguales, como una tabla de Excel. Un `.yml` guarda **configuración**: opciones que van unas dentro de otras, por niveles. Un `.csv` no puede expresar "esto va dentro de aquello"; un `.yml` sí, con la sangría.

**¿Quién exige que sean `.yml`?** **dbt.** Así lo diseñaron sus creadores: dbt solo lee su configuración en `.yml`. Son reglas de la herramienta, igual que pytest exige que las pruebas se llamen `test_...`.

| Archivo | ¿Qué exige dbt? |
|---|---|
| `dbt_project.yml` | El nombre **exacto**, en la carpeta del proyecto. Si se llama distinto o se guarda como `.csv`, dbt dice que no encuentra el proyecto. |
| `profiles.yml` | El nombre **exacto**, en la carpeta de perfiles. |
| `sources.yml` y `schema.yml` | Que sean `.yml` y estén dentro de `models`. El nombre lo elegimos nosotros: `sources` y `schema` son costumbre. |

| Archivo | Qué es |
|---|---|
| `dbt/dbt_project.yml` | La configuración del proyecto: nombre y cómo se crean los modelos. |
| `dbt/profiles.yml` | La conexión: en qué base de datos se crean las tablas. |
| `dbt/models/staging/sources.yml` | De dónde se leen los datos: la capa plata. |
| `dbt/models/staging/stg_ventas.sql` | La primera lectura de los datos de plata. |
| `dbt/models/marts/*.sql` | Las 4 tablas del esquema estrella. |
| `dbt/models/marts/schema.yml` | Las pruebas de cada tabla. |

> 💡 En dbt, cada archivo `.sql` de la carpeta `models/` se llama un **modelo**. *Staging* es la zona de entrada; *marts* (de *data mart*) es la zona de las tablas finales, listas para el análisis.

**¿Por qué tantos `.yml`?** Cada uno responde **una pregunta distinta**. Ninguno se ejecuta: dbt los lee para saber cómo trabajar.

| Archivo | Pregunta que responde |
|---|---|
| `dbt_project.yml` | ¿**Qué** proyecto es y dónde están los modelos? |
| `profiles.yml` | ¿**Dónde** se crean las tablas? En `data/observatorio.duckdb`. |
| `sources.yml` | ¿**De dónde** se leen los datos? De la capa plata. |
| `schema.yml` | ¿**Qué pruebas** debe pasar cada tabla? |

Van en archivos separados porque así lo organiza dbt, igual que en Python `config.py` tiene las rutas y `esquemas.py` las reglas. Así, si cambia la base de datos, solo se toca `profiles.yml`; si cambia la carpeta de plata, solo `sources.yml`; si cambia una prueba, solo `schema.yml`.

### 3.2 Configuración: `dbt_project.yml` y `profiles.yml`

**Creen el archivo `dbt/dbt_project.yml` y peguen este código:**

```yaml
# Configuracion del proyecto dbt: como se llama, donde estan los modelos y como se crean.
# Es un archivo YAML: cada linea es "nombre: valor", y lo que va con sangria
# (2 espacios mas) pertenece a la linea de arriba. No se ejecuta: dbt lo lee.

# El nombre del proyecto dbt
name: observatorio
# La version del proyecto. La escribe el equipo; dbt solo la muestra
version: "1.0.0"
# Que conexion usar: la que se llama "observatorio" en profiles.yml
profile: observatorio

# La carpeta donde estan los modelos (los archivos .sql)
model-paths: ["models"]

# Como se crea cada grupo de modelos
models:
  # Los modelos de este proyecto (el mismo name de arriba)
  observatorio:
    # Los de la carpeta models/staging/...
    staging:
      # ...se crean como VISTAS: consultas guardadas que no copian los datos
      +materialized: view
    # Los de la carpeta models/marts/...
    marts:
      # ...se crean como TABLAS reales dentro del archivo data/observatorio.duckdb
      +materialized: table
```

| Parte | Qué hace |
|---|---|
| `name: observatorio` | El nombre del proyecto dbt. |
| `version: "1.0.0"` | La versión del proyecto. La escribe el equipo; dbt solo la muestra. |
| `profile: observatorio` | Qué conexión usar: la que se llama `observatorio` en `profiles.yml`. |
| `model-paths: ["models"]` | Los modelos están en la carpeta `models/`. |
| `staging: +materialized: view` | Los modelos de `staging/` se crean como **vistas**: consultas guardadas que no copian los datos. |
| `marts: +materialized: table` | Los modelos de `marts/` se crean como **tablas** reales dentro de DuckDB. |

**Creen el archivo `dbt/profiles.yml` y peguen este código:**

```yaml
# Conexion de dbt con la base de datos. Aqui: un archivo DuckDB local.
# Es un archivo YAML: no se ejecuta; dbt lo lee para saber donde crear las tablas.

# El nombre de la conexion: el mismo de "profile" en dbt_project.yml
observatorio:
  # La conexion que se usa por defecto: dev (desarrollo)
  target: dev
  # Las conexiones disponibles (un proyecto real tiene tambien prod, produccion)
  outputs:
    # La conexion dev
    dev:
      # El motor de base de datos: DuckDB (lo trae el paquete dbt-duckdb)
      type: duckdb
      # El archivo de la base de datos de la capa oro. La ruta es desde la raiz
      # del proyecto, porque dbt se ejecuta desde ahi
      path: data/observatorio.duckdb
      # Cuantos modelos se crean al mismo tiempo: 1, uno detras de otro
      threads: 1
```

| Parte | Qué hace |
|---|---|
| `observatorio:` | El nombre de la conexión, el mismo de `profile` en `dbt_project.yml`. |
| `target: dev` | Usa la conexión llamada `dev` (desarrollo). Un proyecto real tiene también `prod` (producción). |
| `type: duckdb` | El motor de base de datos. |
| `path: data/observatorio.duckdb` | El archivo de la base de datos de la capa oro. La ruta es desde la raíz del proyecto, porque dbt se ejecuta desde ahí. |

> 🔒 En un proyecto real, `profiles.yml` tiene usuarios y contraseñas y **no se sube** a GitHub. Aquí se sube porque DuckDB es un archivo local, sin contraseña.

**¿Por qué se llama *profiles* y por qué va aparte?** *Profile* significa "perfil", como el perfil de usuario de una aplicación: los datos de conexión de cada persona o de cada ambiente (`dev` para probar, `prod` para la base de datos real de la empresa). Va en un archivo aparte de `dbt_project.yml` por estas razones:

| Si todo estuviera en un solo `.yml` | Separados |
|---|---|
| Al subir el proyecto a GitHub se subirían también los usuarios y las contraseñas de la base de datos. | `dbt_project.yml` se sube; `profiles.yml`, con las contraseñas, se queda en el computador de cada uno. |
| Si Ana cambia su conexión, cambia el archivo de todo el equipo. | Cada uno tiene su `profiles.yml` y el proyecto no se toca. |
| Para pasar de `dev` a `prod` habría que editar el proyecto. | Solo se cambia el perfil. |

Es la misma idea del archivo `.env` de la Evidencia 1: **el código se comparte, los secretos no**.

### 3.3 Leer la capa plata: `sources.yml` y `stg_ventas.sql`

**`sources.yml` no crea nada: es como una dirección.** Le dice a dbt dónde están los datos limpios: en `data/silver/enerandes_ventas.parquet`. Ese archivo ya existe: lo creó la limpieza en el paso 2.4.

| Qué | ¿Crea archivos? |
|---|---|
| La limpieza, `python -m src.silver.enerandes` (paso 2.4) | **Sí**, 3 archivos: `data/silver/enerandes_ventas.parquet` (las ventas limpias), `data/silver/enerandes_cuarentena.parquet` (la cuarentena) y `docs/reporte_calidad.md` (el reporte de calidad). Ver el árbol del paso 2.6. |
| El experimento de dañar datos (paso 2.6) | **No**: fue solo en memoria. |
| `esquemas.py` | **No**: solo revisa. |
| `sources.yml` | **No**: solo **señala** dónde está el archivo de plata para que dbt lo lea. |

**Creen el archivo `dbt/models/staging/sources.yml` y peguen este código:**

```yaml
# Las fuentes de dbt: las tablas de la capa plata que dbt va a leer.
# Es un archivo YAML: no se ejecuta; dbt lo lee para saber de donde salen los datos.

# La version del formato de este archivo (dbt pide 2)
version: 2

# La lista de fuentes
sources:
  # Una fuente llamada "plata". En los .sql se usa asi: source('plata', ...)
  - name: plata
    # Datos extra para el adaptador de DuckDB
    meta:
      # dbt-duckdb lee cada tabla directo del archivo Parquet de la capa plata.
      # {name} se reemplaza por el nombre de la tabla: enerandes_ventas
      # -> data/silver/enerandes_ventas.parquet
      external_location: "data/silver/{name}.parquet"
    # Las tablas de esta fuente
    tables:
      # Una tabla: las ventas limpias de EnerAndes
      - name: enerandes_ventas
```

| Parte | Qué hace |
|---|---|
| `sources: - name: plata` | Declara una **fuente** llamada `plata`: datos que dbt lee pero no crea. |
| `external_location: "data/silver/{name}.parquet"` | Le dice a dbt-duckdb que cada tabla de esta fuente es un archivo Parquet. `{name}` se cambia por el nombre de la tabla. |
| `tables: - name: enerandes_ventas` | La tabla `enerandes_ventas` = el archivo `data/silver/enerandes_ventas.parquet`. |

**Creen el archivo `dbt/models/staging/stg_ventas.sql` y peguen este código:**

```sql
-- Staging: lee la tabla de ventas de la capa plata, sin cambiarla.
-- En SQL, lo que va despues de -- es un comentario.
-- dbt reemplaza source('plata', 'enerandes_ventas') por la ruta
-- data/silver/enerandes_ventas.parquet (la dice sources.yml).
-- Se crea como VISTA (dbt_project.yml): los demas modelos leen de aqui.

-- select * = traer todas las columnas
select *
-- from = de donde: la tabla de ventas de la capa plata
from {{ source('plata', 'enerandes_ventas') }}
```

| Parte | Qué hace |
|---|---|
| `{{ source('plata', 'enerandes_ventas') }}` | dbt lo cambia por la ubicación real de la tabla: el archivo Parquet de plata. Lo que va entre `{{ }}` es código de dbt (*Jinja*), no SQL. |
| `select *` | Trae todas las columnas, sin cambiarlas. Si mañana cambia la ruta de plata, solo se cambia `sources.yml`: los demás modelos leen de `stg_ventas`. |

### 3.4 Las dimensiones

**¿Por qué varios `.sql` y no uno solo?** En dbt, **cada archivo `.sql` crea una sola tabla**, y el nombre del archivo es el nombre de la tabla.

| Archivo | Tabla que crea |
|---|---|
| `stg_ventas.sql` | `stg_ventas` (la entrada) |
| `dim_mes.sql` | `dim_mes` |
| `dim_municipio.sql` | `dim_municipio` |
| `dim_segmento.sql` | `dim_segmento` |
| `fact_ventas_mensual.sql` | `fact_ventas_mensual` |

El esquema estrella necesita **4 tablas**: 3 dimensiones y 1 tabla de hechos. Por eso hay 4 archivos, más el de entrada. Si todo se escribe en **un solo `.sql`**, sale **una sola tabla grande**: ya no es una estrella, y los meses, municipios y segmentos quedan repetidos en cada fila.

**Creen el archivo `dbt/models/marts/dim_mes.sql` y peguen este código:**

```sql
-- Dimension MES: una fila por cada mes que tiene ventas.
-- Grano: un mes.
-- ref('stg_ventas') es el modelo stg_ventas.sql: dbt lo crea primero y luego este.

-- select distinct = traer las filas SIN repetir: cada mes aparece una sola vez
select distinct
    -- replace quita el guion: '2023-04' -> '202304'; cast(... as integer) lo vuelve
    -- numero: 202304. "as mes_id" le pone ese nombre a la columna (la llave)
    cast(replace(periodo, '-', '') as integer)      as mes_id,
    -- El periodo como texto: '2023-04'
    periodo,
    -- left(periodo, 4) toma los 4 primeros caracteres: '2023' -> 2023
    cast(left(periodo, 4) as integer)               as anio,
    -- right(periodo, 2) toma los 2 ultimos: '04' -> 4
    cast(right(periodo, 2) as integer)              as mes,
    -- El trimestre: (mes + 2) dividido 3, sin decimales (//).
    -- Ejemplo: enero (1+2)//3 = 1; abril (4+2)//3 = 2; diciembre (12+2)//3 = 4
    (cast(right(periodo, 2) as integer) + 2) // 3   as trimestre
-- De donde: el modelo stg_ventas
from {{ ref('stg_ventas') }}
```

| Parte | Qué hace |
|---|---|
| `select distinct` | Una fila por cada mes distinto: 12 meses de 2023. |
| `replace(periodo, '-', '')` y `cast(... as integer)` | `'2023-04'` → `'202304'` → `202304`: una llave numérica para el mes. |
| `left(periodo, 4)` y `right(periodo, 2)` | Los 4 primeros caracteres (el año) y los 2 últimos (el mes). |
| `(mes + 2) // 3` | El trimestre: `//` es la división entera. Abril: (4 + 2) // 3 = 2. |
| `{{ ref('stg_ventas') }}` | Lee el modelo `stg_ventas`. Con `ref`, dbt sabe que debe crear `stg_ventas` **antes** que `dim_mes`. |

**Creen el archivo `dbt/models/marts/dim_municipio.sql` y peguen este código:**

```sql
-- Dimension MUNICIPIO: una fila por municipio, con su codigo DIVIPOLA.
-- Grano: un municipio.

-- select distinct = sin repetir: cada municipio aparece una sola vez (15 filas)
select distinct
    -- La llave: el codigo DANE de 5 digitos ('05001'), con el nombre municipio_id
    divipola    as municipio_id,
    -- El nombre oficial del municipio
    municipio
-- De donde: el modelo stg_ventas
from {{ ref('stg_ventas') }}
```

| Parte | Qué hace |
|---|---|
| `divipola as municipio_id` | La llave es el código DIVIPOLA. Es una **llave natural**: ya existe fuera del proyecto y es oficial. |
| `select distinct` | Una fila por municipio: 15. |

**Creen el archivo `dbt/models/marts/dim_segmento.sql` y peguen este código:**

```sql
-- Dimension SEGMENTO: una fila por segmento de cliente.
-- Grano: un segmento.

select
    -- row_number() numera las filas 1, 2, 3, 4, en orden alfabetico del segmento
    -- (over (order by segmento)). Ese numero es la llave: segmento_id
    row_number() over (order by segmento)   as segmento_id,
    -- El nombre del segmento: Comercial, Industrial, No informado, Residencial
    segmento
-- De donde: una subconsulta (entre parentesis) que trae cada segmento una sola vez
from (select distinct segmento from {{ ref('stg_ventas') }})
```

| Parte | Qué hace |
|---|---|
| `row_number() over (order by segmento)` | Numera los segmentos 1, 2, 3, 4 en orden alfabético. Es una **llave sustituta**: un número inventado por el modelo, porque el segmento no tiene un código oficial. |
| `from (select distinct segmento ...)` | Primero toma los 4 segmentos distintos y después los numera. |

### 3.5 La tabla de hechos: `fact_ventas_mensual.sql`

**Creen el archivo `dbt/models/marts/fact_ventas_mensual.sql` y peguen este código:**

```sql
-- Tabla de HECHOS: las ventas de energia.
-- Grano: un mes, un municipio, un segmento y un tipo de compra.

select
    -- Llave a dim_mes: '2023-04' -> 202304 (igual que en dim_mes).
    -- v. indica que la columna viene de la tabla v (las ventas)
    cast(replace(v.periodo, '-', '') as integer)    as mes_id,
    -- Llave a dim_municipio: el codigo DIVIPOLA
    v.divipola                                      as municipio_id,
    -- Llave a dim_segmento: el numero del segmento (viene de la tabla s)
    s.segmento_id,
    -- Un dato descriptivo que se deja en el hecho: Bolsa o Contrato
    v.tipo_compra,
    -- Las MEDIDAS: los numeros que se suman en el dashboard
    v.energia_kwh,
    v.valor_cop,
    v.clientes
-- De donde: el modelo stg_ventas, con el nombre corto v
from {{ ref('stg_ventas') }} as v
-- join = unir con otra tabla: dim_segmento, con el nombre corto s...
join {{ ref('dim_segmento') }} as s
    -- ...en las filas donde el segmento es el mismo. Asi cada venta recibe su segmento_id
    on v.segmento = s.segmento
```

| Parte | Qué hace |
|---|---|
| `mes_id`, `municipio_id`, `segmento_id` | Las **llaves** que unen cada venta con sus dimensiones. |
| `tipo_compra` | Un dato descriptivo con solo 2 valores: se deja en el hecho, sin crear una dimensión aparte. |
| `energia_kwh`, `valor_cop`, `clientes` | Las **medidas**: los números que se suman o se promedian. |
| `join {{ ref('dim_segmento') }} as s on v.segmento = s.segmento` | Busca el `segmento_id` de cada venta en la dimensión: así el hecho guarda el número, no el texto. |

> 🔑 **El grano de esta tabla:** una fila = **un mes, un municipio, un segmento y un tipo de compra**. Son las mismas 4 columnas del `unique` del esquema de pandera: plata ya garantizó que no se repiten.

> 💡 **Cuidado con `clientes`:** es una medida **semiaditiva**. Sumar la energía de 12 meses tiene sentido (es la energía del año); sumar los clientes de 12 meses **no** (contaría al mismo cliente 12 veces). Los clientes se promedian o se toman del último mes.

### 3.6 Las pruebas: `schema.yml`, y construir todo con `dbt build`

**Creen el archivo `dbt/models/marts/schema.yml` y peguen este código:**

```yaml
# Pruebas de dbt sobre la capa oro. "dbt build" las ejecuta despues de crear cada tabla.
# Es un archivo YAML: no se ejecuta; dbt lo lee para saber que probar en cada tabla.

# La version del formato de este archivo (dbt pide 2)
version: 2

# La lista de modelos (tablas) y sus pruebas
models:
  # La tabla dim_mes
  - name: dim_mes
    # Una descripcion corta de la tabla (sale en la documentacion de dbt)
    description: "Un mes con ventas."
    # Las columnas que se prueban
    columns:
      # La columna mes_id (la llave)
      - name: mes_id
        # unique: no se repite; not_null: nunca esta vacia
        data_tests: [unique, not_null]

  # La tabla dim_municipio
  - name: dim_municipio
    description: "Un municipio de Antioquia con su codigo DIVIPOLA."
    columns:
      # La llave: no se repite y nunca esta vacia
      - name: municipio_id
        data_tests: [unique, not_null]

  # La tabla dim_segmento
  - name: dim_segmento
    description: "Un segmento de cliente."
    columns:
      # La llave: no se repite y nunca esta vacia
      - name: segmento_id
        data_tests: [unique, not_null]

  # La tabla de hechos
  - name: fact_ventas_mensual
    description: "Ventas de energia por mes, municipio, segmento y tipo de compra."
    columns:
      # La llave al mes
      - name: mes_id
        data_tests:
          # Nunca esta vacia
          - not_null
          # relationships: cada mes_id del hecho debe existir en dim_mes
          # (si no, seria una venta de un mes que no esta en la dimension)
          - relationships:
              arguments:
                # La tabla con la que se compara
                to: ref('dim_mes')
                # La columna de esa tabla
                field: mes_id
      # La llave al municipio: nunca vacia y debe existir en dim_municipio
      - name: municipio_id
        data_tests:
          - not_null
          - relationships:
              arguments:
                to: ref('dim_municipio')
                field: municipio_id
      # La llave al segmento: nunca vacia y debe existir en dim_segmento
      - name: segmento_id
        data_tests:
          - not_null
          - relationships:
              arguments:
                to: ref('dim_segmento')
                field: segmento_id
      # El tipo de compra
      - name: tipo_compra
        data_tests:
          # accepted_values: solo se aceptan los valores de esta lista
          - accepted_values:
              arguments:
                values: ["Bolsa", "Contrato"]
```

| Prueba | Qué comprueba |
|---|---|
| `unique` | La columna no tiene valores repetidos. En una llave es obligatorio. |
| `not_null` | La columna no tiene celdas vacías. |
| `relationships` | Cada valor del hecho existe en la dimensión: no hay ventas que apunten a un municipio que no existe. Se llama **integridad referencial**. |
| `accepted_values` | La columna solo tiene los valores de la lista. |
| `description` | Un texto que explica la tabla. Es el inicio del **diccionario de datos**. |

**Construir el modelo y probarlo, con un solo comando**, desde la raíz del proyecto:

```powershell
dbt build --project-dir dbt --profiles-dir dbt
```

| Parte del comando | Qué significa |
|---|---|
| `dbt build` | Crea todos los modelos **y** ejecuta todas las pruebas, en el orden correcto. |
| `--project-dir dbt` | El proyecto dbt está en la carpeta `dbt/`. |
| `--profiles-dir dbt` | El archivo `profiles.yml` también está en `dbt/`. Sin esto, dbt lo busca en la carpeta del usuario de Windows. |

**Resultado** (tarda unos segundos; la primera vez en un computador puede tardar hasta 25):

```text
22:04:29  Running with dbt=1.12.6
22:04:29  Registered adapter: duckdb=1.11.1
22:04:30  Unable to do partial parsing because saved manifest not found. Starting full parse.
22:04:32  Found 5 models, 13 data tests, 1 source, 511 macros
22:04:32
22:04:32  Concurrency: 1 threads (target='dev')
22:04:32
22:04:33  1 of 18 START sql view model main.stg_ventas ................................... [RUN]
22:04:33  1 of 18 OK created sql view model main.stg_ventas .............................. [OK in 0.11s]
22:04:33  2 of 18 START sql table model main.dim_mes ..................................... [RUN]
22:04:33  2 of 18 OK created sql table model main.dim_mes ................................ [OK in 0.10s]
22:04:33  3 of 18 START sql table model main.dim_municipio ............................... [RUN]
22:04:33  3 of 18 OK created sql table model main.dim_municipio .......................... [OK in 0.04s]
22:04:33  4 of 18 START sql table model main.dim_segmento ................................ [RUN]
22:04:34  4 of 18 OK created sql table model main.dim_segmento ........................... [OK in 0.04s]
22:04:34  5 of 18 START test not_null_dim_mes_mes_id ..................................... [RUN]
22:04:34  5 of 18 PASS not_null_dim_mes_mes_id ........................................... [PASS in 0.05s]
   ...                                     (las pruebas 6 a 10 de las dimensiones: PASS)
22:04:34  11 of 18 START sql table model main.fact_ventas_mensual ........................ [RUN]
22:04:34  11 of 18 OK created sql table model main.fact_ventas_mensual ................... [OK in 0.03s]
22:04:34  12 of 18 START test accepted_values_fact_ventas_mensual_tipo_compra__Bolsa__Contrato  [RUN]
22:04:34  12 of 18 PASS accepted_values_fact_ventas_mensual_tipo_compra__Bolsa__Contrato . [PASS in 0.02s]
   ...                                     (las pruebas 13 a 18 del hecho: PASS)
22:04:34
22:04:34  Finished running 4 table models, 13 data tests, 1 view model in 0 hours 0 minutes and 2.06 seconds (2.06s).
22:04:34
22:04:34  Completed successfully
22:04:34
22:04:34  Done. PASS=18 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=18
```

| Lo que aparece | Qué significa |
|---|---|
| `22:04:29` | La hora en **UTC** (5 horas más que en Colombia: aquí eran las 5:04 p. m.). |
| `Running with dbt=1.12.6` | La versión de dbt que se está usando. |
| `Registered adapter: duckdb=1.11.1` | dbt se conectó con DuckDB. |
| `Unable to do partial parsing ...` | Solo sale la primera vez: dbt lee todos los archivos porque no tiene una lectura guardada. No es un error. |
| `Found 5 models, 13 data tests, 1 source, 511 macros` | Encontró los 5 `.sql`, las 13 pruebas de `schema.yml` y la fuente `plata`. Las *macros* son funciones que trae dbt por dentro; no hay que hacer nada con ellas. |
| `Concurrency: 1 threads (target='dev')` | Crea un modelo a la vez (`threads: 1`) con la conexión `dev` de `profiles.yml`. |
| `1 of 18 ... view model main.stg_ventas` | Creó la vista `stg_ventas`. `main` es el esquema por defecto de DuckDB. |
| `2 ... 4 of 18 ... table model` | Creó las 3 dimensiones. |
| `5 ... 10 of 18 ... PASS` | Las pruebas de las dimensiones pasaron. dbt prueba cada tabla **antes** de crear las que dependen de ella. |
| `11 of 18 ... fact_ventas_mensual` | Creó el hecho **después** de las dimensiones, porque lo lee con `ref('dim_segmento')`. |
| `Done. PASS=18 WARN=0 ERROR=0` | 5 modelos creados y 13 pruebas pasadas. El esquema estrella está listo en `data/observatorio.duckdb`. |

**Commit de la capa oro:**

```powershell
git add . ; git commit -m "feat: capa oro con esquema estrella en dbt" ; git push
```

> 💡 `dbt/target/`, `dbt/logs/`, `dbt/.user.yml` y `data/observatorio.duckdb` no se suben: están en `.gitignore` (paso 0.3).

> ⚠️ **Si sale `IO Error: No files found that match the pattern "data/silver/enerandes_ventas.parquet"`:** falta la capa plata. Ejecuten primero `python -m src.silver.enerandes`. Y ejecuten dbt **desde la raíz del proyecto** (donde está `src/`), no desde dentro de `dbt/`.

### 3.7 Consultar el esquema estrella

`dbt show` ejecuta una consulta SQL sobre el modelo y muestra el resultado. Pregunta de negocio: **¿cuánta energía vendió EnerAndes en 2023 en cada segmento?**

```powershell
dbt show --project-dir dbt --profiles-dir dbt --inline "select s.segmento, round(sum(f.energia_kwh) / 1000000, 1) as gwh from {{ ref('fact_ventas_mensual') }} f join {{ ref('dim_segmento') }} s using (segmento_id) group by s.segmento order by gwh desc"
```

| Parte | Qué significa |
|---|---|
| `dbt show` | Ejecuta una consulta y muestra el resultado en la terminal. No crea ni cambia tablas. |
| `--project-dir dbt --profiles-dir dbt` | Igual que en `dbt build`: dónde están el proyecto y la conexión. |
| `--inline "..."` | La consulta va escrita en el mismo comando, entre comillas. |
| `select s.segmento, ... as gwh` | Las 2 columnas del resultado: el nombre del segmento y la energía en GWh. |
| `round(sum(f.energia_kwh) / 1000000, 1)` | `sum` suma la energía; `/ 1000000` la pasa de kWh a GWh (1 GWh = 1.000.000 kWh); `round(..., 1)` la deja con 1 decimal. |
| `from {{ ref('fact_ventas_mensual') }} f` | Lee la tabla de hechos. `ref(...)` es la forma de dbt de nombrar un modelo; `f` es su nombre corto. |
| `join {{ ref('dim_segmento') }} s using (segmento_id)` | Une el hecho con la dimensión de segmento (nombre corto `s`) por la llave `segmento_id`. Así cada venta tiene el **nombre** de su segmento. Es la forma típica de consultar un esquema estrella. |
| `group by s.segmento` | Agrupa las ventas por segmento: un total por cada uno. |
| `order by gwh desc` | Ordena de mayor a menor (*desc*, descendente). |

**Resultado:**

```text
22:06:06  Running with dbt=1.12.6
22:06:06  Registered adapter: duckdb=1.11.1
22:06:07  Found 5 models, 13 data tests, 1 sql operation, 1 source, 511 macros
22:06:07
22:06:07  Concurrency: 1 threads (target='dev')
22:06:07
Previewing inline node:
| segmento     |   gwh |
| ------------ | ----- |
| Residencial  | 309.7 |
| Industrial   | 231.4 |
| Comercial    | 169.6 |
| No informado |  10.4 |
```

| Lo que aparece | Qué significa |
|---|---|
| `1 sql operation` | La consulta escrita con `--inline`: dbt la cuenta como una operación más. |
| `Previewing inline node:` | dbt muestra el resultado de la consulta escrita con `--inline`. |
| `Residencial 309.7` | El segmento residencial compró 309,7 GWh en 2023: el que más energía compró. |
| `No informado 10.4` | 10,4 GWh de ventas sin segmento: el 1,4 % del total. Gracias a la regla 5 no se perdieron, y se ve cuánto pesan. |

### Qué se hace y qué no en la capa oro

| ❌ No se hace | ✅ Sí se hace |
|---|---|
| Una sola tabla gigante con todo. | Separar hechos (lo que se mide) y dimensiones (el contexto). |
| Crear el modelo sin decir qué es una fila. | Escribir el **grano** de cada tabla de hechos. |
| Crear las tablas a mano en DuckDB. | Escribirlas como `.sql` en dbt, versionadas en Git. |
| Confiar en que las llaves están bien. | Probarlas con `unique`, `not_null` y `relationships`. |
| Volver a limpiar datos en SQL. | Leer de plata, que ya está limpia y validada. |

---

## Parte 4 · Trabajo en equipo y Evidencia 2

### 4.1 Llevar el trabajo al repositorio del equipo

Los dos commits ya se hicieron y se subieron: el de plata en el paso 2.9.4 y el de oro en el paso 3.6. Aquí solo falta unir la rama a `main`.

**1. Confirmar que todo quedó subido:**

```powershell
git status
```

| Parte | Qué significa |
|---|---|
| `git status` | Muestra en qué rama están y si hay cambios sin commit. No cambia nada. |

**Resultado:**

```text
On branch feature/plata-oro
Your branch is up to date with 'origin/feature/plata-oro'.

nothing to commit, working tree clean
```

| Lo que aparece | Qué significa |
|---|---|
| `On branch feature/plata-oro` | Están en la rama de hoy, no en `main` (o en la rama con su nombre, si la personalizaron en el paso 0.1). |
| `up to date with 'origin/...'` | GitHub tiene lo mismo que su computador: los dos commits ya se subieron. |
| `nothing to commit, working tree clean` | No hay nada pendiente. Si aparece algún archivo, hagan `git add .`, un `git commit -m "..."` y `git push`. |

**2. Unir la rama a `main`.** Hay dos formas:

| Forma | Cómo | Qué queda en GitHub |
|---|---|---|
| **A. Pull request** (la del equipo) | En la página de GitHub: se pide unir la rama y otro integrante la revisa | Queda el *pull request*: quién lo pidió, quién lo revisó y la conversación. Es la prueba del trabajo en equipo. |
| **B. `git merge`** (desde la terminal) | Se une en el computador y se sube `main` | Quedan los commits en `main`, pero **no** queda revisión de otro integrante. |

**Forma A · Pull request.** Un *pull request* (PR) es un merge que se **pide** en GitHub para que otro integrante lo revise antes de unirlo a `main`.

| # | Quién | Qué hace en GitHub |
|---|---|---|
| 1 | Quien programó | Abre el repositorio en GitHub **con su sesión iniciada** (arriba a la derecha no debe decir **Sign in**; sin sesión no aparece el botón). Arriba sale un aviso amarillo con el botón **Compare & pull request**; denle clic. Si el aviso no sale, abran `https://github.com/<usuario>/observatorio-energia/compare/main...feature/plata-oro` (con el nombre de su rama) y den **Create pull request**. |
| 2 | Quien programó | Revisa que diga `base: main` ← `compare: feature/plata-oro` y **Able to merge** (se puede unir sin conflictos). Escribe un título, por ejemplo `Capa plata y capa oro (EA2)`, y una descripción corta, por ejemplo `Limpieza de la hoja 2023 con pandera y 7 pruebas; esquema estrella en dbt (PASS=18).` |
| 3 | Quien programó | A la derecha, en **Reviewers**, elige a un compañero y da **Create pull request**. |
| 4 | El compañero | Abre el PR, revisa el código en la pestaña **Files changed** y, arriba a la derecha, da **Submit review** (en otras versiones de GitHub se llama **Review changes**) → marca **Approve** → **Submit review**. GitHub **no** deja que el autor apruebe su propio PR: siempre lo aprueba otra cuenta. |
| 5 | Quien programó (o el compañero) | Da **Merge pull request → Confirm merge**. Ahora `main` tiene la capa plata y la capa oro. |

**Pasos 1 y 2 · La página para crear el Pull Request.** Arriba, `base: main` ← `compare: feature/...` y **Able to merge**; a la derecha, el botón verde **Create pull request**; abajo, los 2 commits (plata y oro) y los 18 archivos que se van a unir:

![Página Comparing changes con el botón Create pull request](img/4_1_comparar_ramas.png)

**Pasos 2 y 3 · Título, descripción y revisor.** En **Add a title** va el título y en **Add a description** lo que se hizo. A la derecha, en **Reviewers** (la tuerca ⚙️), se elige al compañero que va a revisar. Luego, el botón verde **Create pull request**:

![Página Open a pull request con título, descripción y Reviewers](img/4_1_titulo_pr.png)

**Pasos 4 y 5 · El Pull Request creado.** Arriba, el número del PR (`#3`) y **Open** (abierto). En **Commits** están los 2 commits y en **Files changed** los 18 archivos: ahí el compañero revisa y aprueba con **Review changes → Approve**. Abajo, **No conflicts with base branch** y el botón verde **Merge pull request**:

![Pull Request abierto con el botón Merge pull request](img/4_1_pr_creado.png)

**Paso 4 · Lo que ve el compañero en Files changed.** A la izquierda, el árbol con los 18 archivos; en el centro, el código: lo nuevo en verde con `+`. Arriba a la derecha, el botón verde **Submit review**, donde marca **Approve**:

![Pestaña Files changed con el botón Submit review](img/4_1_files_changed.png)

**Paso 5 · Confirmar el merge.** Al dar **Merge pull request** aparece el mensaje del commit de unión (se puede dejar como está) y el botón **Confirm merge**:

![Mensaje del merge y botón Confirm merge](img/4_1_confirm_merge.png)

**Resultado · PR unido.** Arriba dice **Merged** (morado): los 2 commits ya están en `main`. Abajo, **Pull request successfully merged and closed** y el botón **Delete branch**, que borra la rama en GitHub porque ya no se necesita (es opcional):

![Pull Request en estado Merged con el botón Delete branch](img/4_1_merged.png)

**¿Por qué deja hacer Merge si nadie aprobó?** Porque `main` **no está protegida**. En la captura de los pasos 4 y 5 dice **Reviewers: No reviews** y aun así el botón **Merge pull request** está activo.

| `main` | ¿Se puede dar **Merge** sin que nadie apruebe? |
|---|---|
| **Sin proteger** | ✅ Sí. La aprobación es opcional y cualquiera une su rama sin revisión. |
| **Protegida** con *Require approvals* | ❌ No. El botón **Merge** queda bloqueado hasta que un compañero dé **Approve**. |

**Cómo proteger `main`** (lo hace el dueño del repositorio, una sola vez):

| # | Dónde | Qué hacer |
|---|---|---|
| 1 | Pestaña **Settings** del repositorio (la última de arriba) | Clic. Solo la ve el dueño. |
| 2 | Menú izquierdo → **Branches** | Clic. |
| 3 | Botón **Add classic branch protection rule** | Clic. |
| 4 | **Branch name pattern** | Escribir `main`. |
| 5 | **Require a pull request before merging** | Marcarla. Así nadie sube directo a `main` con `git push`: todo entra por un PR. |
| 6 | Debajo: **Require approvals**, con **1** | Marcarla. Así se necesita al menos 1 aprobación de **otra** cuenta. |
| 7 | Abajo, botón **Create** | Clic. GitHub puede pedir la contraseña. |

> ⚠️ Con `main` protegida, el autor del PR no puede aprobarse a sí mismo: **siempre** debe aprobar un compañero. En la EA1 varios equipos perdieron puntos por no proteger `main`.

Luego, **todos** traen `main` actualizada a su computador:

```powershell
git switch main
git pull
```

**Resultado** (recortado):

```text
Already on 'main'
Your branch is up to date with 'origin/main'.
From https://github.com/<usuario>/observatorio-energia
   bd4eb8d..3bd2495  main       -> origin/main
Updating bd4eb8d..3bd2495
Fast-forward
 .gitignore                               |   4 +
 dbt/dbt_project.yml                      |  26 +++
 ...
 src/silver/enerandes.py                  | 364 +++++++++++++++++++++++++++++++
 tests/test_limpieza.py                   | 140 ++++++++++++
 18 files changed, 819 insertions(+)
 create mode 100644 dbt/dbt_project.yml
 ...
 create mode 100644 tests/test_limpieza.py
```

| Lo que aparece | Qué significa |
|---|---|
| `Already on 'main'` | Ya estaban en `main`; si estaban en la rama, dice `Switched to branch 'main'`. |
| `bd4eb8d..3bd2495  main -> origin/main` | `main` en GitHub avanzó hasta `3bd2495`, el commit del merge. En su computador salen otros códigos. |
| `Fast-forward` | git solo mueve su `main` hasta ese commit: no hay nada que mezclar. |
| `18 files changed, 819 insertions(+)` | Llegaron los 18 archivos de la capa plata y la capa oro. Ya los tienen en `main`. |

Es el mismo flujo de la Parte 7 de la clase del 19 de octubre.

> ⚠️ **Se hace una sola forma, no las dos.** Si ya hicieron el merge en GitHub con la Forma A, sáltense la Forma B y sigan en la sección 4.2.

**Forma B · `git merge`** (solo si **no** usaron el Pull Request). Primero se pasan a la rama que va a **recibir** los cambios:

```powershell
git switch main
```

| Parte | Qué significa |
|---|---|
| `git switch main` | Se pasa a la rama `main`. |

**Resultado:**

```text
Switched to branch 'main'
Your branch is up to date with 'origin/main'.
```

| Lo que aparece | Qué significa |
|---|---|
| `Switched to branch 'main'` | Ya están en `main`. Los archivos de la carpeta quedan como están en `main`: todavía **sin** la capa plata ni dbt. |
| `Your branch is up to date with 'origin/main'` | Su `main` está igual a la de GitHub. |

Luego traen a `main` los commits de la rama de hoy:

```powershell
git merge feature/plata-oro
```

| Parte | Qué significa |
|---|---|
| `git merge` | Une a la rama actual (`main`) los commits de otra rama. |
| `feature/plata-oro` | La rama que trae los cambios. El nombre debe estar escrito exacto. |

**Resultado** (recortado):

```text
Updating 64e0580..ccfa3dd
Fast-forward
 .gitignore                               |   3 +
 dbt/dbt_project.yml                      |  26 +++++
 dbt/models/marts/dim_mes.sql             |  20 ++++
 ...
 src/silver/enerandes.py                  | 364 +++++++++++++++++++++++++++++++
 tests/test_limpieza.py                   | 140 ++++++++++++++
 18 files changed, 819 insertions(+)
 create mode 100644 dbt/dbt_project.yml
 ...
 create mode 100644 tests/test_limpieza.py
```

| Lo que aparece | Qué significa |
|---|---|
| `Updating 64e0580..ccfa3dd` | `main` pasa del commit `64e0580` (el último que tenía) al `ccfa3dd` (el último commit de hoy, el de oro). En su computador salen otros códigos. |
| `Fast-forward` | "Avance rápido": `main` no tenía commits nuevos desde que se creó la rama, así que git solo **mueve** `main` hasta el último commit de la rama. No hay nada que mezclar ni conflictos. |
| `dbt/dbt_project.yml \| 26 +++++` | Cada archivo que cambió y cuántas líneas se agregaron (`+`) o quitaron (`-`). Las barras `+++` son un dibujo de esa cantidad. |
| `18 files changed, 819 insertions(+)` | El total de los dos commits (plata y oro): 18 archivos y 819 líneas nuevas. |
| `create mode 100644 ...` | Los archivos nuevos que ahora están en `main`. |

> ⚠️ **Si sale `merge: feature/plata-oro4 - not something we can merge`:** el nombre de la rama está mal escrito (aquí, con un `4` de más). No se cambia nada; escríbanlo bien y repitan.

Por último, suben `main` actualizada a GitHub:

```powershell
git push
```

| Parte | Qué significa |
|---|---|
| `git push` | Sube a GitHub los commits de `main`. No hace falta escribir `origin main`: `main` ya está conectada con la de GitHub. |

**Resultado:**

```text
Total 0 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
To https://github.com/<usuario>/observatorio-energia.git
   64e0580..ccfa3dd  main -> main
```

| Lo que aparece | Qué significa |
|---|---|
| `Total 0 (delta 0)` | No hubo que enviar archivos: GitHub ya los tenía, porque llegaron con el push de la rama. |
| `64e0580..ccfa3dd  main -> main` | `main` en GitHub pasó del commit `64e0580` al `ccfa3dd`. Ya tiene la capa plata, dbt y las pruebas. |


### 4.2 Lo que se hizo hoy frente a lo que se evalúa en la Evidencia 2

El código de esta clase es de todos. La Evidencia 2 evalúa lo que el equipo **agrega y amplía** a partir de él:

| Hecho en clase | Lo que agrega el equipo en la Evidencia 2 |
|---|---|
| Plata: la hoja **2023** de EnerAndes | Las **4 hojas** (2023 a 2026) en una sola tabla: encabezados distintos, títulos y notas en las primeras filas, fechas en 4 formatos (`2024-03`, `mar-24`, `03/2024` y `01/03/2026`, que es día/mes/año) y energía en kWh y MWh en la hoja 2024 |
| — | Plata de **XM** (precio, demanda, generación: de 24 columnas por hora a una fila por hora), **IDEAM**, **NOAA** (con la fase El Niño / La Niña) y la **fuente propia** |
| Esquema de pandera para las ventas | Un esquema de pandera para **cada** tabla de plata |
| 6 pruebas de las reglas de la hoja 2023 | Mínimo **5 pruebas más** con `pytest` sobre sus reglas nuevas: por ejemplo, la conversión de MWh a kWh, las fechas `mar-24` y `03/2024`, la fase ENSO o el paso de XM de 24 columnas a una fila por hora |
| Reporte de calidad con 9 reglas | Un reporte con **todas** las reglas de todas las fuentes, cada una con su métrica antes y después |
| Oro: 1 hecho y 3 dimensiones | Mínimo **3 tablas de hechos** (entre ellas `fact_mercado_horario` y `fact_generacion_recurso`) y **5 dimensiones**, entre ellas `dim_fecha` (día, con fase ENSO) y `dim_recurso` (plantas, de `ListadoRecursos`) |
| 13 pruebas de dbt | Pruebas `unique`, `not_null` y `relationships` en **todos** los modelos |
| — | Diagrama del modelo, **diccionario de datos**, consultas SQL que respondan preguntas de negocio, y plata + oro ejecutándose con **un solo comando** |
| — | Cada integrante: mínimo 3 commits, 1 PR propio, revisar el PR de un compañero y la bitácora al día |
| — | Tag `ea2`: `git tag ea2` y luego `git push origin ea2` |

> 📌 El enunciado completo y la rúbrica están en Canvas: **EA2. Calidad de datos y modelo dimensional**.

---

## Si algo falla

| Síntoma | Causa | Solución |
|---|---|---|
| `ModuleNotFoundError: No module named 'pandera'` | No se instalaron las librerías nuevas, o el entorno virtual no está activo. | `.\.venv\Scripts\Activate.ps1` y `pip install -r requirements.txt`. |
| `ModuleNotFoundError: No module named 'src.silver'` | Falta el archivo `src/silver/__init__.py`, o se ejecutó desde otra carpeta. | Crear el archivo vacío `src/silver/__init__.py` (paso 0.2) y ejecutar desde la raíz del proyecto. |
| `AttributeError: module 'src.config' has no attribute 'DIR_SILVER'` | No se agregaron las 2 líneas a `src/config.py`. | Hacer el paso 0.3. |
| `FileNotFoundError: ... enerandes_ventas_2023.parquet` | No está la capa bronce de EnerAndes. | `python -m src.extract.enerandes`. |
| `KeyError: 'xxxx'` en la regla 6 | Apareció una forma de escribir un municipio que no está en `MUNICIPIOS` ni en `ALIAS_MUNICIPIO`. Pasa al limpiar las otras hojas. | Agregar esa forma a `ALIAS_MUNICIPIO`. |
| `SchemaErrors` de pandera | Una fila limpia no cumple una regla del esquema. | Leer `column`, `check` y `failure cases`, y corregir la regla de limpieza (no el esquema). |
| `ModuleNotFoundError: No module named 'src'` al ejecutar las pruebas | Se ejecutó `pytest` solo. | Ejecutar `python -m pytest`, desde la raíz del proyecto. |
| `collected 0 items` / `no tests ran` | El archivo de pruebas no empieza por `test_`. | Renombrarlo: `tests/test_algo.py`. |
| Salen menos pruebas de las escritas | Una función de prueba no empieza por `test_`. | Renombrarla: `def test_algo():`. |
| `dbt : El término 'dbt' no se reconoce...` | El entorno virtual no está activo. | `.\.venv\Scripts\Activate.ps1`. |
| `Error: Invalid value for '--profiles-dir': Path 'C:\Users\...\.dbt' does not exist.` | Falta `--profiles-dir dbt`: dbt buscó `profiles.yml` en la carpeta del usuario de Windows. | Usar el comando completo de la sección 3.6. |
| `IO Error: No files found that match the pattern "data/silver/..."` | Falta la capa plata, o dbt se ejecutó desde dentro de `dbt/`. | Ejecutar `python -m src.silver.enerandes` y correr dbt desde la raíz del proyecto. |
| `IO Error: Could not set lock on file "data/observatorio.duckdb"` | Otro programa tiene abierta la base (por ejemplo, otra terminal con DuckDB o DBeaver). | Cerrar ese programa y repetir. |
| Una prueba `FAIL` en `dbt build` | Los datos no cumplen una prueba de `schema.yml`. | Ver el nombre de la prueba que falló; `dbt build` muestra cuántas filas no cumplen. |

## Glosario (orden alfabético)

| Término | Significado |
|---|---|
| **Calidad de datos** | Qué tan confiables son los datos para tomar decisiones. Se mide en dimensiones: unicidad, consistencia, completitud, validez, exactitud y oportunidad. |
| **Capa oro** | Los datos organizados para el análisis: aquí, el esquema estrella en DuckDB. |
| **Capa plata** | Los datos limpios y validados, construidos a partir de bronce. |
| **Cuarentena** | Archivo con las filas que no se pueden usar ni corregir. Se apartan, no se borran. |
| **DAMA-DMBOK** | La guía de referencia de la gestión de datos. Define las dimensiones de la calidad. |
| **dbt** | *Data build tool*: herramienta para transformar datos con SQL, con orden de ejecución, pruebas y versionamiento. |
| **Dimensión** | Tabla que describe el contexto de un hecho: cuándo, dónde, quién. |
| **DIVIPOLA** | Codificación oficial de los municipios de Colombia (DANE). |
| **Esquema de validación** | Lista de condiciones que una tabla debe cumplir. Aquí se escribe con pandera. |
| **Esquema estrella** | Modelo con una tabla de hechos en el centro y las dimensiones alrededor. |
| **Grano** | Qué representa una fila de la tabla de hechos. |
| **Integridad referencial** | Que cada llave del hecho exista en su dimensión. dbt lo prueba con `relationships`. |
| **Llave natural** | Una llave que ya existe fuera del modelo, como el código DIVIPOLA. |
| **Llave sustituta** | Un número que el modelo inventa como llave, como `segmento_id`. |
| **Medida** | Un número del hecho que se suma o se promedia. |
| **Medida semiaditiva** | Una medida que no se puede sumar en el tiempo, como el número de clientes. |
| **Métrica antes y después** | El número que mide un problema antes y después de aplicar la regla. |
| **Modelo (dbt)** | Un archivo `.sql` de la carpeta `models/`: dbt lo convierte en una vista o una tabla. |
| **pandera** | Librería de Python para validar tablas de pandas contra un esquema. |
| **Prueba automática** | Un programa pequeño que ejecuta una función con datos de ejemplo y comprueba con `assert` que el resultado es el esperado. |
| **pytest** | Librería de Python que encuentra y ejecuta las pruebas automáticas. |
| **Regla de limpieza** | Una corrección escrita en código, que se aplica igual cada vez. |
| **Tabla de hechos** | Tabla con los eventos que se miden y sus medidas. |
