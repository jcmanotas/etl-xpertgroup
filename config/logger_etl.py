import logging

"""
Este script configura un logger en Python para registrar mensajes de ejecución
tanto en un archivo de log como en la consola.  
El logger está configurado para mostrar mensajes a partir del nivel INFO.

Características:
- Guarda los logs en un archivo: ./logs/log_general_etl.log
- Muestra los logs en la consola
- Formato de log: Fecha y hora - Nivel de severidad - Mensaje
"""

# Configuración del logger principal
logging.basicConfig(
    level=logging.INFO, # Nivel mínimo de mensajes que se registrarán (INFO y superiores)
    format='%(asctime)s - %(levelname)s - %(message)s', # Formato de los mensajes de log
    handlers=[
        logging.FileHandler("./logs/log_general_etl.log"), # Guardar logs en un archivo
        logging.StreamHandler() # Mostrar logs en consola
    ]
)

# Crear una instancia de logger reutilizable en este módulo
# __name__ permite que el logger herede el nombre del módulo desde el cual se ejecuta
loggerETL = logging.getLogger(__name__)
