import os
import json
import pandas as pd
from config.logger_etl import loggerETL
from dotenv import load_dotenv

def load_data_pacientes(tabla: str = "pacientes") -> pd.DataFrame:
    """
    Carga el JSON dataset_hospital.json,
    cuya ruta está definida en un archivo .env como PATH_DATA_FILE.

    Parámetros
    ----------
    tabla : str, opcional
        Nombre de la tabla a cargar ("pacientes" o "citas_medicas").
        Por defecto "pacientes".

    Retorna
    -------
    pd.DataFrame
        DataFrame con los datos de la tabla solicitada.
    """
    # Cargar variables de entorno
    load_dotenv()
    dataset_path = os.getenv("PATH_DATA_FILE")

    if not dataset_path:
        loggerETL.error("No se encontró la variable PATH_DATA_FILE en el archivo .env")
        raise ValueError("No se encontró la variable PATH_DATA_FILE en el archivo .env")

    # Leer JSON
    with open(dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if tabla not in data:
        loggerETL.error(f"La tabla '{tabla}' no existe en {dataset_path}. Tablas disponibles: {list(data.keys())}")
        raise KeyError(f"La tabla '{tabla}' no existe en {dataset_path}. Tablas disponibles: {list(data.keys())}")
    else:
        loggerETL.info(f"La tabla '{tabla}' fue cargada exitosamente.")

    return pd.DataFrame(data[tabla])