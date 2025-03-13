from read_excel_tasas import ReadDataExcelTasas
from load_data_db import loadDatabase
from dotenv import load_dotenv
import os

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

if __name__=='__main__':
    df_tasas = ReadDataExcelTasas().create_df_mec_tasas()
    print(df_tasas)
    host_dbb, user_dbb, pass_dbb, dbb_ministerio_educacion = cargar_variables_entorno()
    loadDatabase(host_dbb, user_dbb, pass_dbb, dbb_ministerio_educacion).load_data_tasas(df_tasas)