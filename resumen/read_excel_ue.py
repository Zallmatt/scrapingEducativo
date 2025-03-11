import os
import pandas as pd

class loadExcelUE:
    @staticmethod
    def load_route_excel(name):
        """Obtiene la ruta absoluta del archivo en la carpeta 'files'"""
        file_path = os.path.join(os.path.dirname(__file__), "files", name)
        return file_path  # Retorna la ruta completa del archivo

    @staticmethod
    def create_df_ue(name, sheet_index=1):
        """Carga los datos de la segunda hoja del Excel, tomando provincias de la fila 46 a la 71 y agrega los datos de nivel inicial desde loadEUInicial"""
        file_path = loadExcelUE.load_route_excel(name)

        # Cargar la segunda hoja del archivo Excel
        df = pd.read_excel(file_path, sheet_name=sheet_index, header=None)

        # Extraer las provincias y el año (Columna A, filas 46 a 71 en base 1 → 45 a 70 en base 0)
        df_provincias = df.iloc[45:71, 0].reset_index(drop=True)  # Columna A (Índice 0)

        # Extraer las demás columnas necesarias
        df_data = df.iloc[45:71, 1:].reset_index(drop=True)  # Desde la segunda columna en adelante

        # Crear un DataFrame con la estructura esperada
        columns = [
            "año", "provincia", "ue_establecimientos",
        ]

        # Crear DataFrame con estructura fija
        df_educacion_comun_resumen_ue = pd.DataFrame(columns=columns)
        df_educacion_comun_resumen_ue["provincia"] = df_provincias  # Agregar provincias
        df_educacion_comun_resumen_ue["año"] = 2023
        df_educacion_comun_resumen_ue.iloc[:, 2:] = df_data  # Rellenar con los demás datos

        # Jardin
        df_jardin = loadExcelUE.read_eu_inicial(name, sheet_index)
        df_educacion_comun_resumen_ue = df_educacion_comun_resumen_ue.merge(df_jardin[["provincia", "us_inicial_publico", "us_inicial_privado"]], on="provincia", how="left")
        
        # Primaria
        df_primaria = loadExcelUE.read_eu_primaria(name, sheet_index)
        df_educacion_comun_resumen_ue = df_educacion_comun_resumen_ue.merge(df_primaria[["provincia", "ue_primaria_publico", "ue_primaria_privado"]], on="provincia", how="left")

        # Secundaria
        df_secundaria = loadExcelUE.read_eu_secundaria(name, sheet_index)
        df_educacion_comun_resumen_ue = df_educacion_comun_resumen_ue.merge(df_secundaria[["provincia", "ue_secundaria_publico", "ue_secundaria_privado"]], on="provincia", how="left")

        # Superior no Universitario
        df_superior_no_universitario = loadExcelUE.read_eu_no_universitario(name, sheet_index)
        df_educacion_comun_resumen_ue = df_educacion_comun_resumen_ue.merge(df_superior_no_universitario[["provincia", "ue_sup_nouniv_publico", "ue_sup_nouniv_privado"]], on="provincia", how="left")

        return df_educacion_comun_resumen_ue


    @staticmethod
    def read_eu_inicial(name, sheet_index=1):
        """Carga datos de nivel inicial desde la segunda hoja del Excel (filas 46 a 71) y suma las columnas necesarias."""
        file_path = loadExcelUE.load_route_excel(name)

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
        df_jardin = pd.DataFrame(columns=columns)
        # Asignar valores
        df_jardin["año"] = 2023  # Año fijo
        df_jardin["provincia"] = df_provincias  # Provincias
        df_jardin.iloc[:, 2:5] = df_data_publico  # Asignar datos públicos
        df_jardin.iloc[:, 5:8] = df_data_privado  # Asignar datos privados

        # Crear las columnas sumadas
        df_jardin["us_inicial_publico"] = df_jardin.iloc[:, 2:5].sum(axis=1)
        df_jardin["us_inicial_privado"] = df_jardin.iloc[:, 5:8].sum(axis=1)

        # Eliminar las columnas originales si ya no son necesarias
        df_jardin = df_jardin.drop(columns=columns[2:8])

        return df_jardin
    
    @staticmethod
    def read_eu_primaria(name, sheet_index=1):
        """Carga datos de nivel inicial desde la segunda hoja del Excel (filas 46 a 71) y suma las columnas necesarias."""
        file_path = loadExcelUE.load_route_excel(name)

        # Cargar la segunda hoja del archivo Excel
        df = pd.read_excel(file_path, sheet_name=sheet_index, header=None)

        # Extraer las provincias (Columna A, filas 46 a 71 → Índices 45 a 70)
        df_provincias = df.iloc[45:71, 0].reset_index(drop=True)  # Columna A (Índice 0)

        # Extraer datos de nivel inicial PÚBLICO (Columnas E, F y G → Índices 4, 5 y 6)
        df_data_publico = df.iloc[45:71, 7:9].reset_index(drop=True)

        # Extraer datos de nivel inicial PRIVADO (Columnas E, F y G → Índices 4, 5 y 6)
        df_data_privado = df.iloc[82:108, 7:9].reset_index(drop=True)
        
        df_data_publico = df_data_publico.apply(pd.to_numeric, errors='coerce').fillna(0)
        df_data_privado = df_data_privado.apply(pd.to_numeric, errors='coerce').fillna(0)

        # Definir las columnas esperadas
        columns = [
            "año", "provincia", 
            "primaria_6_años_publico", "primaria_7_años_publico", "primaria_6_años_privado",
            "primaria_7_años_privado"]
        
        # Crear DataFrame con estructura fija
        df_primaria = pd.DataFrame(columns=columns)
        # Asignar valores
        df_primaria["año"] = 2023  # Año fijo
        df_primaria["provincia"] = df_provincias  # Provincias
        df_primaria.iloc[:, 2:4] = df_data_publico  # Asignar datos públicos
        df_primaria.iloc[:, 4:6] = df_data_privado  # Asignar datos privados

        # Crear las columnas sumadas
        df_primaria["ue_primaria_publico"] = df_primaria.iloc[:, 2:4].sum(axis=1)
        df_primaria["ue_primaria_privado"] = df_primaria.iloc[:, 4:6].sum(axis=1)

        # Eliminar las columnas originales si ya no son necesarias
        df_primaria = df_primaria.drop(columns=columns[2:8])

        return df_primaria
    
    @staticmethod
    def read_eu_secundaria(name, sheet_index=1):
        """Carga datos de nivel inicial desde la segunda hoja del Excel (filas 46 a 71) y suma las columnas necesarias."""
        file_path = loadExcelUE.load_route_excel(name)

        # Cargar la segunda hoja del archivo Excel
        df = pd.read_excel(file_path, sheet_name=sheet_index, header=None)

        # Extraer las provincias (Columna A, filas 46 a 71 → Índices 45 a 70)
        df_provincias = df.iloc[45:71, 0].reset_index(drop=True)  # Columna A (Índice 0)

        # Extraer datos de nivel inicial PÚBLICO (Columnas E, F y G → Índices 4, 5 y 6)
        df_data_publico = df.iloc[45:71, 9:12].reset_index(drop=True)

        # Extraer datos de nivel inicial PRIVADO (Columnas E, F y G → Índices 4, 5 y 6)
        df_data_privado = df.iloc[82:108, 9:12].reset_index(drop=True)
        
        df_data_publico = df_data_publico.apply(pd.to_numeric, errors='coerce').fillna(0)
        df_data_privado = df_data_privado.apply(pd.to_numeric, errors='coerce').fillna(0)

        # Definir las columnas esperadas
        columns = [
            "año", "provincia", 
            "secundaria_ciclo_basico_publico", "secundaria_ciclo_orientado_publico", "secundaria_ciclo_basico_y_orientado_publico",
            "secundaria_ciclo_basico_privado", "secundaria_ciclo_orientado_privado", "secundaria_ciclo_basico_y_orientado_privado"
        ]
        
        # Crear DataFrame con estructura fija
        df_secundaria = pd.DataFrame(columns=columns)
        # Asignar valores
        df_secundaria["año"] = 2023  # Año fijo
        df_secundaria["provincia"] = df_provincias  # Provincias
        df_secundaria.iloc[:, 2:5] = df_data_publico  # Asignar datos públicos
        df_secundaria.iloc[:, 5:8] = df_data_privado  # Asignar datos privados

        # Crear las columnas sumadas
        df_secundaria["ue_secundaria_publico"] = df_secundaria.iloc[:, 2:5].sum(axis=1)
        df_secundaria["ue_secundaria_privado"] = df_secundaria.iloc[:, 5:8].sum(axis=1)

        # Eliminar las columnas originales si ya no son necesarias
        df_secundaria = df_secundaria.drop(columns=columns[2:8])

        return df_secundaria
    
    @staticmethod
    def read_eu_no_universitario(name, sheet_index=1):
        """Carga datos de nivel inicial desde la segunda hoja del Excel (filas 46 a 71) y suma las columnas necesarias."""
        file_path = loadExcelUE.load_route_excel(name)

        # Cargar la segunda hoja del archivo Excel
        df = pd.read_excel(file_path, sheet_name=sheet_index, header=None)

        # Extraer las provincias (Columna A, filas 46 a 71 → Índices 45 a 70)
        df_provincias = df.iloc[45:71, 0].reset_index(drop=True)  # Columna A (Índice 0)

        # Extraer datos de nivel inicial PÚBLICO (Columnas E, F y G → Índices 4, 5 y 6)
        df_data_publico = df.iloc[45:71, 12].reset_index(drop=True)

        # Extraer datos de nivel inicial PRIVADO (Columnas E, F y G → Índices 4, 5 y 6)
        df_data_privado = df.iloc[82:108, 12].reset_index(drop=True)
        
        df_data_publico = df_data_publico.apply(pd.to_numeric, errors='coerce').fillna(0)
        df_data_privado = df_data_privado.apply(pd.to_numeric, errors='coerce').fillna(0)

        # Definir las columnas esperadas
        columns = [
            "año", "provincia", 
            "ue_sup_nouniv_publico", 
            "ue_sup_nouniv_privado", 
        ]
        
        # Crear DataFrame con estructura fija
        df_superior_no_universitario = pd.DataFrame(columns=columns)
        # Asignar valores
        df_superior_no_universitario["año"] = 2023  # Año fijo
        df_superior_no_universitario["provincia"] = df_provincias  # Provincias
        df_superior_no_universitario.iloc[:, 2:3] = df_data_publico  # Asignar datos públicos
        df_superior_no_universitario.iloc[:, 3:4] = df_data_privado  # Asignar datos privados
        
        return df_superior_no_universitario