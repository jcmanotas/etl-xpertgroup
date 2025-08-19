import os
import sys
import pandas as pd
import numpy as np
from email_validator import validate_email, EmailNotValidError
from dateutil import parser


def clear_screen():
    """
    Limpia la pantalla de la consola.
    Funciona tanto en Windows como en sistemas tipo Unix (Linux/Mac).
    """
    # Detectar sistema operativo y ejecutar comando correspondiente
    os.system("cls" if os.name == "nt" else "clear")


def print_separator():
    print("=" * 120)


def parse_date_etl(x, fmt="%Y-%m-%d"):
    """Parsea fechas solo si cumplen el formato YYYY-MM-DD"""
    try:
        return pd.to_datetime(x, format=fmt, errors="coerce")
    except Exception:
        try:
            return pd.to_datetime(parser.parse(str(x), dayfirst=True))
        except Exception:
            return pd.NaT
        

def is_valid_email_etl(x):
    """Valida sintaxis de email."""
    if pd.isna(x): return False
    try:
        validate_email(str(x), check_deliverability=False)
        return True
    except EmailNotValidError:
        return False


def validaciones_pacientes(df):
    """Detecta problemas típicos en la tabla pacientes"""
    df = df.copy()
    problemas = {}

    # Edad vs fecha_nacimiento
    if "fecha_nacimiento" in df.columns:
        df["fecha_nacimiento_parsed"] = df["fecha_nacimiento"].apply(parse_date_etl)
        df["edad_calculada"] = (pd.to_datetime("today").year - df["fecha_nacimiento_parsed"].dt.year)
        problemas["fechas_invalidas"] = df["fecha_nacimiento_parsed"].isna().sum()
        if "edad" in df.columns:
            diff = (df["edad"].fillna(df["edad_calculada"]) - df["edad_calculada"]).abs()
            problemas["edad_inconsistente"] = (diff > 2).sum()  # tolerancia 2 años

    # Emails inválidos
    if "email" in df.columns:
        problemas["emails_invalidos"] = (~df["email"].dropna().apply(is_valid_email_etl)).sum()

    # Sexo fuera de catálogo
    if "sexo" in df.columns:
        catalogo = {"M", "F", "MALE", "FEMALE", "O", "ND"}
        problemas["sexo_fuera_catalogo"] = (~df["sexo"].dropna().astype(str).str.upper().isin(catalogo)).sum()

    # Duplicados por id_paciente
    if "id_paciente" in df.columns:
        problemas["id_paciente_duplicado"] = df["id_paciente"].duplicated().sum()

    return problemas


def definitivo_pacientes(df):
    """
    Retorna únicamente un DataFrame limpio de la tabla pacientes:
    - Sin duplicados por id_paciente
    - Con sexo estandarizado (Masculino/Femenino)
    - Con email válido
    - Con fecha de nacimiento válida
    - Con la edad calculada cuando está vacía
    """
    df = df.copy()

    # ---- Validación fechas de nacimiento ----
    if "fecha_nacimiento" in df.columns:
        df["fecha_nacimiento_parsed"] = df["fecha_nacimiento"].apply(parse_date_etl)
    else:
        df["fecha_nacimiento_parsed"] = pd.NaT

    # ---- Calcular edad ----
    hoy = pd.to_datetime("today")
    if "fecha_nacimiento_parsed" in df.columns:
        nac = df["fecha_nacimiento_parsed"]

        # años completos
        edad = hoy.year - nac.dt.year

        # restar 1 si aún no ha cumplido años este año
        cumple_despues = (
            (hoy.month < nac.dt.month)
            | ((hoy.month == nac.dt.month) & (hoy.day < nac.dt.day))
        )
        edad = edad - cumple_despues.astype(int)

        df["edad_calculada"] = edad

        # Si existe columna edad → rellenar los NaN/None con edad_calculada
        if "edad" in df.columns:
            df["edad"] = df["edad"].fillna(df["edad_calculada"])
        else:
            df["edad"] = df["edad_calculada"]

    # ---- Emails válidos ----
    if "email" in df.columns:
        df["email_valido"] = df["email"].apply(is_valid_email_etl)
    else:
        df["email_valido"] = True

    # ---- Sexo válido y estandarizado ----
    if "sexo" in df.columns:
        sexo_norm = df["sexo"].astype(str).str.upper().str.strip()
        mapa_sexo = {
            "M": "Masculino",
            "MALE": "Masculino",
            "F": "Femenino",
            "FEMALE": "Femenino",
        }
        df["sexo_estandarizado"] = sexo_norm.map(mapa_sexo)
        df["sexo_valido"] = df["sexo_estandarizado"].notna()
    else:
        df["sexo_valido"] = True
        df["sexo_estandarizado"] = None

    # ---- Filtrado de registros válidos ----
    df_limpio = df[
        (~df["id_paciente"].duplicated(keep="first"))
        & (df["sexo_valido"])
        & (df["email_valido"])
        & (df["fecha_nacimiento_parsed"].notna())
    ].copy()

    # Reemplazar sexo original por el estandarizado
    df_limpio["sexo"] = df_limpio["sexo_estandarizado"]

    # Eliminar columnas auxiliares que no hacen falta
    df_limpio = df_limpio.drop(
        columns=["email_valido", "sexo_valido", "sexo_estandarizado"], errors="ignore"
    )

    return df_limpio


def validaciones_citas(df, pacientes):
    """Detecta problemas típicos en la tabla citas_medicas"""
    df = df.copy()
    problemas = {}

    # Fechas de cita
    if "fecha_cita" in df.columns:
        df["fecha_cita_parsed"] = df["fecha_cita"].apply(lambda x: parse_date_etl(x))
        problemas["fechas_invalidas"] = df["fecha_cita_parsed"].isna().sum()

    # Estado de cita fuera de catálogo
    if "estado" in df.columns:
        catalogo = {"PROGRAMADA", "COMPLETADA", "CANCELADA", "REPROGRAMADA"}
        problemas["estado_fuera_catalogo"] = (~df["estado"].dropna().astype(str).str.upper().isin(catalogo)).sum()

    # Clave foránea id_paciente
    if "id_paciente" in df.columns and "id_paciente" in pacientes.columns:
        problemas["citas_sin_paciente"] = (~df["id_paciente"].isin(pacientes["id_paciente"])).sum()

    # Duplicados por id_cita
    if "id_cita" in df.columns:
        problemas["id_cita_duplicado"] = df["id_cita"].duplicated().sum()

    return problemas


def definitivo_citas(df, pacientes):
    """
    Retorna únicamente un DataFrame limpio de la tabla citas_medicas:
    - Con fecha válida (parseada correctamente)
    - Con estado dentro del catálogo
    - Con id_paciente existente en pacientes
    - Sin duplicados por id_cita
    """
    df = df.copy()

    # ---- Validación fechas de cita ----
    if "fecha_cita" in df.columns:
        df["fecha_cita_parsed"] = df["fecha_cita"].apply(lambda x: parse_date_etl(x))
    else:
        df["fecha_cita_parsed"] = pd.NaT

    # ---- Estado válido ----
    if "estado" in df.columns:
        catalogo = {"PROGRAMADA", "COMPLETADA", "CANCELADA", "REPROGRAMADA"}
        df["estado_valido"] = df["estado"].astype(str).str.upper().isin(catalogo)
    else:
        df["estado_valido"] = True

    # ---- Relación con pacientes ----
    if "id_paciente" in df.columns and "id_paciente" in pacientes.columns:
        df["paciente_valido"] = df["id_paciente"].isin(pacientes["id_paciente"])
    else:
        df["paciente_valido"] = True

    # ---- Filtrado de registros válidos ----
    df_limpio = df[
        (~df["id_cita"].duplicated(keep="first"))
        & (df["estado_valido"])
        & (df["paciente_valido"])
        & (df["fecha_cita_parsed"].notna())
    ].copy()

    # Reemplazar fecha original con la parseada en formato YYYY-MM-DD
    df_limpio["fecha_cita"] = df_limpio["fecha_cita_parsed"].dt.strftime("%Y-%m-%d")

    # Eliminar columnas auxiliares
    df_limpio = df_limpio.drop(
        columns=["estado_valido", "paciente_valido", "fecha_cita_parsed"],
        errors="ignore"
    )

    return df_limpio


def resumen_basico(df, nombre_tabla):
    # --------------------------
    # Análisis Exploratorio
    # --------------------------
    print(f"\n===== Resumen de {nombre_tabla} =====")
    print("Forma:", df.shape)
    print("\nValores nulos por columna:\n", df.isna().sum())
    print("\nTipos de datos:\n", df.dtypes)
    print("\nDuplicados (filas completas):", df.duplicated().sum())


def exportar_tablas_limpias(df_pacientes, df_citas, outdir="output"):
    """
    Exporta las versiones limpias de las tablas en CSV y Parquet.

    Parámetros
    ----------
    df_pacientes : pd.DataFrame
        DataFrame limpio de pacientes.
    df_citas : pd.DataFrame
        DataFrame limpio de citas médicas.
    outdir : str, opcional
        Carpeta donde se guardarán los archivos (por defecto 'output').
    """
    os.makedirs(outdir, exist_ok=True)

    # Exportar pacientes
    df_pacientes.to_csv(os.path.join(outdir, "pacientes_clean.csv"), index=False, encoding="utf-8")
    df_pacientes.to_parquet(os.path.join(outdir, "pacientes_clean.parquet"), index=False)

    # Exportar citas
    df_citas.to_csv(os.path.join(outdir, "citas_medicas_clean.csv"), index=False, encoding="utf-8")
    df_citas.to_parquet(os.path.join(outdir, "citas_medicas_clean.parquet"), index=False)

    print(f"✅ Tablas exportadas en la carpeta: {outdir}")
