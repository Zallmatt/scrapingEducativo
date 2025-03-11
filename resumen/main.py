from read_excel_ue import loadExcelUE
from read_excel_us import loadExcelUS
from load_database import loadDatabase
from dotenv import load_dotenv
import os

excel_name="RESUMEN_2023.xlsx"

def cargar_variables_entorno():
    """Carga las variables de entorno necesarias para la conexión."""
    load_dotenv()

    # Obtener las variables de entorno
    host_dbb = os.getenv('HOST_DBB')
    user_dbb = os.getenv('USER_DBB')
    pass_dbb = os.getenv('PASSWORD_DBB')
    dbb_datalake = os.getenv('NAME_DBB')

    # Verificar que todas las variables de entorno están cargadas
    if not all([host_dbb, user_dbb, pass_dbb, dbb_datalake]):
        raise ValueError("Faltan variables de entorno necesarias para la conexión.")
    
    return host_dbb, user_dbb, pass_dbb, dbb_datalake

if __name__ == '__main__':
    #UE
    df_ue = loadExcelUE.create_df_ue(excel_name)
    print(df_ue)
    host_dbb, user_dbb, pass_dbb, dbb_ministerio_educacion = cargar_variables_entorno()
    loadDatabase(host_dbb, user_dbb, pass_dbb, dbb_ministerio_educacion).load_data_ue(df_ue)

    #US 
    df_us = loadExcelUS.create_df_us(excel_name)
    print(df_us)
    host_dbb, user_dbb, pass_dbb, dbb_ministerio_educacion = cargar_variables_entorno()
    loadDatabase(host_dbb, user_dbb, pass_dbb, dbb_ministerio_educacion).load_data_us(df_us)