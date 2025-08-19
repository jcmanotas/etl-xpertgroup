import os
from config.logger_etl import loggerETL
from utils.util_etl import clear_screen, print_separator, resumen_basico, validaciones_pacientes, validaciones_citas, definitivo_pacientes, definitivo_citas, exportar_tablas_limpias
from config.db_conect import load_data_pacientes


def main():
    clear_screen()
    print("PRUEBAS JUAN CARLOS MANOTAS - PROCESO ETL")
    print_separator()
    df_pacientes = load_data_pacientes("pacientes")
    df_citas = load_data_pacientes("citas_medicas")
    
    #RESUMEN BASICO
    resumen_basico(df_pacientes, "Pacientes")

    if not df_citas.empty:
        resumen_basico(df_citas, "Citas Medicas")
    
    # Hallazgos de calidad
    print_separator()
    print("\n>>> Problemas en pacientes:", validaciones_pacientes(df_pacientes))
    print_separator()

    # DF Definitivo pacientes
    final_pacientes = definitivo_pacientes(df_pacientes)

    if not df_citas.empty:
        print_separator()
        print("\n>>> Problemas en citas médicas:", validaciones_citas(df_citas, df_pacientes))
        print_separator()

    final_citas = definitivo_citas(df_citas, final_pacientes)

    exportar_tablas_limpias(final_pacientes, final_citas)

    #print(final_pacientes.head())
    #print(final_citas.head())


if __name__ == "__main__":
    main()
