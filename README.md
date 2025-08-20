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

## 📊 Resumen de hallazgos de calidad de datos

### 🧑‍⚕️ Tabla: `pacientes`
- **`fechas_invalidas`: 4**  
  → Se encontraron 4 registros con **fechas de nacimiento no válidas** o imposibles de parsear.  
- **`edad_inconsistente`: 1,615**  
  → En 1,615 pacientes la **edad no coincide** con la calculada a partir de la fecha de nacimiento.  
- **`emails_invalidos`: 0**  
  → No se detectaron correos electrónicos inválidos.  
- **`sexo_fuera_catalogo`: 0**  
  → Todos los valores de la columna `sexo` están dentro del catálogo esperado (M, F, O, ND).  
- **`id_paciente_duplicado`: 10**  
  → Existen 10 registros con **ID de paciente duplicado**, lo que compromete la unicidad de la clave primaria.  

### 📅 Tabla: `citas_medicas`
- **`fechas_invalidas`: 6,592**  
  → Hay 6,592 registros con **fechas de cita no válidas** (errores de formato o imposibles de interpretar).  
- **`citas_sin_paciente`: 190**  
  → Se encontraron 190 citas que hacen referencia a un **`id_paciente` inexistente** en la tabla `pacientes` (violación de integridad referencial).  
- **`id_cita_duplicado`: 0**  
  → No se detectaron duplicados en los identificadores de cita (`id_cita`).  

---

## ✅ Conclusión
- La **tabla de pacientes** presenta principalmente problemas en la consistencia de la edad y algunos duplicados en la clave primaria.  
- La **tabla de citas médicas** tiene un número muy alto de fechas inválidas y algunas referencias a pacientes inexistentes.  
- Estos hallazgos sugieren la necesidad de:  
  1. **Normalizar y validar fechas** en ambas tablas.  
  2. **Depurar duplicados** en `pacientes`.  
  3. Implementar **controles de integridad referencial** entre citas y pacientes.  
  