import os
import pandas as pd

class loadExcel:
    @staticmethod
    def loadRoute(name):
        """Obtiene la ruta absoluta del archivo en la carpeta 'files'"""
        file_path = os.path.join(os.path.dirname(__file__), "files", name)
        return file_path  # Retorna la ruta completa del archivo

    @staticmethod
    def loadUE(name, sheet_index=1):
        """Carga los datos de la segunda hoja del Excel, tomando provincias de la fila 46 a la 71"""
        file_path = loadExcel.loadRoute(name)

        # Cargar la segunda hoja del archivo Excel
        df = pd.read_excel(file_path, sheet_name=sheet_index, header=None)

        # Extraer las provincias y el año (Columna A, filas 46 a 71 en base 1 → 45 a 70 en base 0)
        df_provincias = df.iloc[45:71, 0].reset_index(drop=True)  # Columna A (Índice 0)

        # Extraer las demás columnas necesarias (ajustar si es necesario según la estructura del Excel)
        df_data = df.iloc[45:71, 1:].reset_index(drop=True)  # Desde la segunda columna en adelante

        # Crear un DataFrame con la estructura esperada
        columns = [
            "año", "provincia", "ue_establecimientos",
            "us_inicial_publico", "us_inicial_privado",
            "us_primaria_publico", "us_primaria_privado",
            "us_secundaria_publico", "us_secundaria_privado",
            "us_sup_nouniv_publico", "us_sup_nouniv_privado"
        ]

        # Agregar el año y la provincia como columnas fijas
        df_estructura = pd.DataFrame(columns=columns)
        df_estructura["provincia"] = df_provincias  # Agregar provincias
        df_estructura["año"] = 2023
        df_estructura.iloc[:, 2:] = df_data  # Rellenar con los demás datos

        return df_estructura

    @staticmethod
    def loadEUInicial(name, sheet_index=1):
        """Carga datos de nivel inicial desde la segunda hoja del Excel (filas 46 a 71) y suma las columnas necesarias."""
        file_path = loadExcel.loadRoute(name)

        # Cargar la segunda hoja del archivo Excel
        df = pd.read_excel(file_path, sheet_name=sheet_index, header=None)

        # Extraer las provincias (Columna A, filas 46 a 71 → Índices 45 a 70)
        df_provincias = df.iloc[45:71, 0].reset_index(drop=True)  # Columna A (Índice 0)

        # Extraer datos de nivel inicial PÚBLICO (Columnas E, F y G → Índices 4, 5 y 6)
        df_data_publico = df.iloc[45:71, 4:7].reset_index(drop=True)

        # Extraer datos de nivel inicial PRIVADO (Columnas E, F y G → Índices 4, 5 y 6)
        df_data_privado = df.iloc[82:108, 4:7].reset_index(drop=True)
        
        df_data_publico = df_data_publico.apply(pd.to_numeric, errors='coerce').fillna(0)
        df_data_privado = df_data_privado.apply(pd.to_numeric, errors='coerce').fillna(0)

        # Definir las columnas esperadas
        columns = [
            "año", "provincia", 
            "inicial_jardin_maternal_publico", "inicial_jardin_infantes_publico", "inicial_jardin_ambos_publico",
            "inicial_jardin_maternal_privado", "inicial_jardin_infantes_privado", "inicial_jardin_ambos_privado"
        ]

        # Crear DataFrame con estructura fija
        df_estructura = pd.DataFrame(columns=columns)
        # Asignar valores
        df_estructura["año"] = 2023  # Año fijo
        df_estructura["provincia"] = df_provincias  # Provincias
        df_estructura.iloc[:, 2:5] = df_data_publico  # Asignar datos públicos
        df_estructura.iloc[:, 5:8] = df_data_privado  # Asignar datos privados

        print(df_estructura)
        # Crear las columnas sumadas
        df_estructura["us_inicial_publico"] = df_estructura.iloc[:, 2:5].sum(axis=1)
        df_estructura["us_inicial_privado"] = df_estructura.iloc[:, 5:8].sum(axis=1)

        # Eliminar las columnas originales si ya no son necesarias
        df_estructura = df_estructura.drop(columns=columns[2:8])

        return df_estructura