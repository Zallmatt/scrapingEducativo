from read_excel_ue import loadExcelUE
from read_excel_us import loadExcelUS
from read_excel_alumnos import ReadExcelAlumnos
from read_excel_cargos import ReadExcelCargos
from read_excel_horas import ReadExcelHoras
from read_excel_inicial import ReadExcelInicialAsistencia
from read_excel_primario import ReadExcelPrimarioRepitentes
from read_excel_secundario import ReadExcelSecundarioRepitentes
from load_database import loadDatabase
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

if __name__ == '__main__':
    año = 2023
    excel_name="RESUMEN_2023.xlsx"
    name_inicial = "INICIAL_2023.xlsx"
    name_primario = "PRIMARIO_2023.xlsx"
    name_secundario = "SECUNDARIO_2023.xlsx"

    #UE
    df_ue = loadExcelUE.create_df_ue(excel_name, año)
    print(df_ue)
    host_dbb, user_dbb, pass_dbb, dbb_ministerio_educacion = cargar_variables_entorno()
    loadDatabase(host_dbb, user_dbb, pass_dbb, dbb_ministerio_educacion).load_data_ue(df_ue)

    #US 
    df_us = loadExcelUS.create_df_us(excel_name, año)
    print(df_us)
    host_dbb, user_dbb, pass_dbb, dbb_ministerio_educacion = cargar_variables_entorno()
    loadDatabase(host_dbb, user_dbb, pass_dbb, dbb_ministerio_educacion).load_data_us(df_us)

    #Alumnos
    df_alumnos = ReadExcelAlumnos().create_df_alumnos(excel_name, año)
    print(df_alumnos)
    host_dbb, user_dbb, pass_dbb, dbb_ministerio_educacion = cargar_variables_entorno()
    loadDatabase(host_dbb, user_dbb, pass_dbb, dbb_ministerio_educacion).load_data_alumnos(df_alumnos)

    #Cargos
    df_educacion_comun_cargos= ReadExcelCargos().create_df_cargos(excel_name, año)
    print(df_educacion_comun_cargos)
    host_dbb, user_dbb, pass_dbb, dbb_ministerio_educacion = cargar_variables_entorno()
    loadDatabase(host_dbb, user_dbb, pass_dbb, dbb_ministerio_educacion).load_data_cargos(df_educacion_comun_cargos)

    #Horas
    df_educacion_comun_horas= ReadExcelHoras().create_df_cargos(excel_name, año)
    print(df_educacion_comun_horas)
    host_dbb, user_dbb, pass_dbb, dbb_ministerio_educacion = cargar_variables_entorno()
    loadDatabase(host_dbb, user_dbb, pass_dbb, dbb_ministerio_educacion).load_data_horas(df_educacion_comun_horas)

    #Inicial 
    df_inicial_asistencia= ReadExcelInicialAsistencia().create_df_inicial_asistencia(name_inicial, año)
    print(df_inicial_asistencia)
    host_dbb, user_dbb, pass_dbb, dbb_ministerio_educacion = cargar_variables_entorno()
    loadDatabase(host_dbb, user_dbb, pass_dbb, dbb_ministerio_educacion).load_data_inicial_asistencia(df_inicial_asistencia)

    #Primario
    df_primario_repitentes = ReadExcelPrimarioRepitentes().create_df_primario_repitentes(name_primario, año)
    print(df_primario_repitentes)
    host_dbb, user_dbb, pass_dbb, dbb_ministerio_educacion = cargar_variables_entorno()
    loadDatabase(host_dbb, user_dbb, pass_dbb, dbb_ministerio_educacion).load_data_primario_repitentes(df_primario_repitentes)

    #Secundario
    df_nivel_secundario_repitentes = ReadExcelSecundarioRepitentes().create_df_secundario_repitentes(name_secundario, año)
    print(df_nivel_secundario_repitentes)
    host_dbb, user_dbb, pass_dbb, dbb_ministerio_educacion = cargar_variables_entorno()
    loadDatabase(host_dbb, user_dbb, pass_dbb, dbb_ministerio_educacion).load_data_secundario_repitentes(df_nivel_secundario_repitentes)