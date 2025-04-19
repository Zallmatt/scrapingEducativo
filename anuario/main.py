import os
from dotenv import load_dotenv

# Readers
from readers.read_excel_ue import loadExcelUE
from readers.read_excel_us import loadExcelUS
from readers.read_excel_alumnos import ReadExcelAlumnos
from readers.read_excel_cargos import ReadExcelCargos
from readers.read_excel_horas import ReadExcelHoras
from readers.read_excel_inicial import ReadExcelInicialAsistencia
from readers.read_excel_primario import ReadExcelPrimarioRepitentes
from readers.read_excel_secundario import ReadExcelSecundarioRepitentes

# Carga DB
from data.load_database import loadDatabase

def cargar_variables_entorno():
    load_dotenv()
    host = os.getenv('HOST_DBB')
    user = os.getenv('USER_DBB')
    password = os.getenv('PASSWORD_DBB')
    db = os.getenv('NAME_DBB')
    if not all([host, user, password, db]):
        raise ValueError("❌ Faltan variables de entorno.")
    return host, user, password, db

def procesar_ue(resumen, año):
    df = loadExcelUE.create_df_ue(resumen, año)
    print(df)
    exit()
    db.load_data_ue(df)

def procesar_us(resumen, año):
    df = loadExcelUS.create_df_us(resumen, año)
    print(df)
    valor_ingresado = input("¿Desea continuar? (s/n): ").strip().lower()
    if valor_ingresado == "s":
        db.load_data_us(df)
    else:
        print("❌ Proceso cancelado.")
    exit()

def procesar_alumnos(resumen, año):
    df = ReadExcelAlumnos().create_df_alumnos(resumen, año)
    valor_ingresado = input("¿Desea continuar? (s/n): ").strip().lower()
    if valor_ingresado == "s":
        db.load_data_alumnos(df)
    else:
        print("❌ Proceso cancelado.")
    exit()

def procesar_cargos(resumen, año):
    df = ReadExcelCargos().create_df_cargos(resumen, año)
    valor_ingresado = input("¿Desea continuar? (s/n): ").strip().lower()
    if valor_ingresado == "s":
        db.load_data_cargos(df)
    else:
        print("❌ Proceso cancelado.")
    exit()

def procesar_horas(resumen, año):
    df = ReadExcelHoras().create_df_cargos(resumen, año)
    valor_ingresado = input("¿Desea continuar? (s/n): ").strip().lower()
    if valor_ingresado == "s":
        db.load_data_horas(df)
    else:
        print("❌ Proceso cancelado.")
    exit()

def procesar_inicial(nombre, año):
    df = ReadExcelInicialAsistencia().create_df_inicial_asistencia(nombre, año)
    valor_ingresado = input("¿Desea continuar? (s/n): ").strip().lower()
    if valor_ingresado == "s":
        db.load_data_inicial_asistencia(df)
    else:
        print("❌ Proceso cancelado.") 
    exit()

def procesar_primario(nombre, año):
    df = ReadExcelPrimarioRepitentes().create_df_primario_repitentes(nombre, año)
    valor_ingresado = input("¿Desea continuar? (s/n): ").strip().lower()
    if valor_ingresado == "s":
        db.load_data_primario_repitentes(df)
    else:
        print("❌ Proceso cancelado.")
    exit()

def procesar_secundario(nombre, año):
    df = ReadExcelSecundarioRepitentes().create_df_secundario_repitentes(nombre, año)
    valor_ingresado = input("¿Desea continuar? (s/n): ").strip().lower()
    if valor_ingresado == "s":
        db.load_data_secundario_repitentes(df)
    else:  
        print("❌ Proceso cancelado.")
    exit()    

def procesar_todo():
    print("\n🚀 Procesando todos los módulos del Anuario 2023...")
    procesar_ue(resumen, año)
    procesar_us(resumen, año)
    procesar_alumnos(resumen, año)
    procesar_cargos(resumen, año)
    procesar_horas(resumen, año)
    procesar_inicial(name_inicial, año)
    procesar_primario(name_primario, año)
    procesar_secundario(name_secundario, año)
    print("✅ Carga completa del Anuario 2023.")

if __name__ == '__main__':
    host, user, password, dbname = cargar_variables_entorno()
    db = loadDatabase(host, user, password, dbname)

    año = 2018
    resumen = "2.1. RESUMEN 2023.xlsx"
    name_inicial = "2.2. INICIAL 2023.xlsx"
    name_primario = "2.3. PRIMARIO 2023.xlsx"
    name_secundario = "2.4. SECUNDARIO 2018.xlsx"

    print("\n📊 Seleccioná qué dataset querés cargar:")
    print("0. 🔁 Todos")
    print("1. Unidades Educativas (UE)")
    print("2. Unidades de Servicio (US)")
    print("3. Alumnos")
    print("4. Cargos docentes")
    print("5. Horas cátedra")
    print("6. Nivel Inicial - Asistencia")
    print("7. Nivel Primario - Repitencia")
    print("8. Nivel Secundario - Repitencia")

    opcion = input("👉 Ingresá el número: ").strip()

    match opcion:
        case "0": procesar_todo()
        case "1": procesar_ue(resumen, año)
        case "2": procesar_us(resumen, año)
        case "3": procesar_alumnos(resumen, año)
        case "4": procesar_cargos(resumen, año)
        case "5": procesar_horas(resumen, año)
        case "6": procesar_inicial(name_inicial, año)
        case "7": procesar_primario(name_primario, año)
        case "8": procesar_secundario(name_secundario, año)
        case _: print("❌ Opción inválida.")
