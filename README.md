# elt-xpertgroup
## PRUEBA JUAN CARLOS MANOTAS
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![JSON](https://img.shields.io/badge/JSON-000000?style=for-the-badge&logo=json&logoColor=white)](https://www.json.org/json-es.html)
[![email_validator](https://img.shields.io/badge/email__validator-4B8BBE?style=for-the-badge&logo=mail.ru&logoColor=white)](https://pypi.org/project/email-validator/)
[![Parquet](https://img.shields.io/badge/Apache%20Parquet-50C878?style=for-the-badge&logo=apache&logoColor=white)](https://parquet.apache.org/)

⚡ Powered by: [jmanotas@gmail.com](mailto:jmanotas@gmail.com)

## 🏥 Documentacion ETL - Calidad de Datos Hospitalarios
Este proyecto implementa un flujo **ETL (Extract, Transform, Load)** para analizar, limpiar y validar datos de pacientes y citas médicas provenientes del archivo `dataset_hospital.json`. 

El objetivo es garantizar la **calidad de los datos** aplicando reglas de validación, estandarización y control de duplicados, además de dejar preparado el entorno para pruebas y auditoría.

---

## 📂 Estructura del Proyecto

├── config/ # Configuración del proyecto<br>
│ ├── db_conect.py # Carga de datos desde JSON definido en .env<br>
│ └── logger_etl.py # Configuración centralizada de logging<br>
├── data/ # Archivos de datos originales y limpios<br>
├── logs/ # Carpeta donde se almacenan los logs de ejecución<br>
├── utils/ # Funciones auxiliares para validación y limpieza<br>
├── .env # Variables de entorno (ej: ruta al dataset)<br>
├── main.py # Script principal del pipeline ETL<br>

### ⚙️ `config/db_conect.py`
Contiene la función `load_data_pacientes` que permite cargar los datos desde el archivo `dataset_hospital.json`.  
El archivo JSON se encuentra en la ruta especificada por la variable de entorno `PATH_DATA_FILE` definida en `.env`.

### 📂 data/
Aquí se ubican tanto los datasets originales (dataset_hospital.json) como las versiones limpias exportadas en CSV/Parquet luego del proceso ETL.

### 📂 logs/
Contiene los archivos de log generados por logger_etl.py.

Ejemplo: log_general_etl.log.

### 📂 utils/
Funciones auxiliares para:
- Validación de calidad de datos.
- Limpieza y estandarización.
- Cálculo de indicadores.

### 📂 output/
- salida de la data en formato parquet y csv