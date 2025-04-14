from dotenv import load_dotenv
import os

# Readers
from readers.read_excel_tasas import ReadDataExcelTasas
from readers.read_excel_tasa_abandono_interanual import ReadDataExcelTasaAbandonoInteranual
from readers.read_excel_promocion_efectiva import ReadDataExcelTasaPromocionEfectiva
from readers.read_excel_repitencia import ReadDataExcelTasaRepitencia  
from readers.read_excel_sobreedad import ReadDataExcelTasaSobreedad
from readers.read_excel_escolarizacion import ReadDataExcelTasaEscolarizacion

# Carga DB
from data.load_data_db import loadDatabase


def cargar_variables_entorno():
    load_dotenv()
    host = os.getenv('HOST_DBB')
    user = os.getenv('USER_DBB')
    password = os.getenv('PASSWORD_DBB')
    db = os.getenv('NAME_DBB')
    if not all([host, user, password, db]):
        raise ValueError("❌ Faltan variables de entorno.")
    return host, user, password, db


def procesar_tasas():
    df = ReadDataExcelTasas().create_df_mec_tasas()
    db.load_data_tasas(df)

def procesar_abandono():
    df = ReadDataExcelTasaAbandonoInteranual().create_df_abandono_interanual()
    db.load_data_tasa_abandono(df)

def procesar_promocion():
    df = ReadDataExcelTasaPromocionEfectiva().create_df_promocion_efectiva()
    exit()
    db.load_data_tasa_promocion_efectiva(df)

def procesar_repitencia():
    df = ReadDataExcelTasaRepitencia().create_df_repitencia()
    db.load_data_tasa_repitencia(df)

def procesar_sobreedad():
    df = ReadDataExcelTasaSobreedad().create_df_sobreedad()
    db.load_data_sobreedad(df)

def procesar_escolarizacion():
    df = ReadDataExcelTasaEscolarizacion().create_df_from_calculos()
    db.load_data_ecolarizacion(df)

def procesar_todo():
    print("🚀 Procesando TODOS los datasets...")
    procesar_tasas()
    procesar_abandono()
    procesar_promocion()
    procesar_repitencia()
    procesar_sobreedad()
    procesar_escolarizacion()
    print("✅ Carga completa de todos los datasets.")

if __name__ == '__main__':
    host, user, password, dbname = cargar_variables_entorno()
    db = loadDatabase(host, user, password, dbname)

    print("📊 Seleccioná qué dataset querés cargar:")
    print("0. 🔁 Todos")
    print("1. Tasas generales MEC")
    print("2. Tasa de abandono interanual")
    print("3. Tasa de promoción efectiva")
    print("4. Tasa de repitencia")
    print("5. Tasa de sobreedad")
    print("6. Tasa de escolarización")
    
    opcion = input("👉 Ingresá el número: ").strip()

    match opcion:
        case "0": procesar_todo()
        case "1": procesar_tasas()
        case "2": procesar_abandono()
        case "3": procesar_promocion()
        case "4": procesar_repitencia()
        case "5": procesar_sobreedad()
        case "6": procesar_escolarizacion()
        case _: print("❌ Opción inválida.")
