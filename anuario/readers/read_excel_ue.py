import os
import pandas as pd

class loadExcelUE:
    @staticmethod
    def load_route_excel(name):
        return os.path.join(os.path.dirname(__file__), "..", "files", name)

    @staticmethod
    def create_df_ue(name, año, sheet_index=1):
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
            "año", "id_provincia", "ue_establecimientos_publico",
        ]

        # Crear DataFrame con estructura fija
        df_educacion_comun_resumen_ue = pd.DataFrame(columns=columns)
        df_educacion_comun_resumen_ue["id_provincia"] = df_provincias  # Agregar provincias
        df_educacion_comun_resumen_ue["año"] = año
        df_educacion_comun_resumen_ue.iloc[:, 2:] = df_data  # Rellenar con los demás datos

        #Establecimiento
        df_establecimiento_privado = loadExcelUE.read_ue_establecimientos(name, año, sheet_index)
        df_educacion_comun_resumen_ue = df_educacion_comun_resumen_ue.merge(df_establecimiento_privado[["id_provincia", "ue_establecimientos_privado"]], on="id_provincia", how="left")

        # Jardin
        df_jardin = loadExcelUE.read_eu_inicial(name, año, sheet_index)
        df_educacion_comun_resumen_ue = df_educacion_comun_resumen_ue.merge(df_jardin[["id_provincia", "ue_inicial_publico", "ue_inicial_privado"]], on="id_provincia", how="left")
        
        # Primaria
        df_primaria = loadExcelUE.read_eu_primaria(name, año, sheet_index)
        df_educacion_comun_resumen_ue = df_educacion_comun_resumen_ue.merge(df_primaria[["id_provincia", "ue_primaria_publico", "ue_primaria_privado"]], on="id_provincia", how="left")

        # Secundaria
        df_secundaria = loadExcelUE.read_eu_secundaria(name, año, sheet_index)
        df_educacion_comun_resumen_ue = df_educacion_comun_resumen_ue.merge(df_secundaria[["id_provincia", "ue_secundaria_publico", "ue_secundaria_privado"]], on="id_provincia", how="left")

        # Superior no Universitario
        df_superior_no_universitario = loadExcelUE.read_eu_no_universitario(name, año, sheet_index)
        df_educacion_comun_resumen_ue = df_educacion_comun_resumen_ue.merge(df_superior_no_universitario[["id_provincia", "ue_sup_nouniv_publico", "ue_sup_nouniv_privado"]], on="id_provincia", how="left")

        # Mapa de provincias a códigos INDEC
        codigo_provincias = {
            "Nacion": 1,
            "Ciudad de Buenos Aires": 2,
            "Buenos Aires": 6,
            "Catamarca": 10,
            "Córdoba": 14,
            "Corrientes": 18,
            "Chaco": 22,
            "Chubut": 26,
            "Entre Ríos": 30,
            "Formosa": 34,
            "Jujuy": 38,
            "La Pampa": 42,
            "La Rioja": 46,
            "Mendoza": 50,
            "Misiones": 54,
            "Neuquén": 58,
            "Río Negro": 62,
            "Salta": 66,
            "San Juan": 70,
            "San Luis": 74,
            "Santa Cruz": 78,
            "Santa Fe": 82,
            "Santiago del Estero": 86,
            "Tucumán": 90,
            "Tierra del Fuego": 94
        }

        # Reemplazar las provincias por los códigos correspondientes
        df_educacion_comun_resumen_ue["id_provincia"] = df_educacion_comun_resumen_ue["id_provincia"].replace(codigo_provincias)
        
        # Limpieza
        df_educacion_comun_resumen_ue = df_educacion_comun_resumen_ue[~df_educacion_comun_resumen_ue["id_provincia"].isin(["Conurbano", "Buenos Aires Resto"])]
        
        return df_educacion_comun_resumen_ue

    @staticmethod
    def read_ue_establecimientos(name, año, sheet_index=1):
        """Carga datos de nivel inicial desde la segunda hoja del Excel (filas 46 a 71) y suma las columnas necesarias."""
        file_path = loadExcelUE.load_route_excel(name)

        # Cargar la segunda hoja del archivo Excel
        df = pd.read_excel(file_path, sheet_name=sheet_index, header=None)

        # Extraer las provincias (Columna A, filas 46 a 71 → Índices 45 a 70)
        df_provincias = df.iloc[45:71, 0].reset_index(drop=True)  # Columna A (Índice 0)

        # Extraer datos de nivel inicial PRIVADO (Columnas E, F y G → Índices 4, 5 y 6)
        df_data_privado = df.iloc[82:108, 1].reset_index(drop=True)
        df_data_privado = df_data_privado.apply(pd.to_numeric, errors='coerce').fillna(0)

        # Definir las columnas esperadas
        columns = [
            "año", "id_provincia", "ue_establecimientos_privado"
        ]
        
        # Crear DataFrame con estructura fija
        df_establecimiento_privado = pd.DataFrame(columns=columns)
        # Asignar valores
        df_establecimiento_privado["año"] = int(año)  # Año fijo
        df_establecimiento_privado["id_provincia"] = df_provincias  # Provincias
        df_establecimiento_privado.iloc[:, 2:3] = df_data_privado  # Asignar datos públicos
        
        return df_establecimiento_privado


    @staticmethod
    def read_eu_inicial(name, año, sheet_index=1):
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
            "año", "id_provincia", 
            "inicial_jardin_maternal_publico", "inicial_jardin_infantes_publico", "inicial_jardin_ambos_publico",
            "inicial_jardin_maternal_privado", "inicial_jardin_infantes_privado", "inicial_jardin_ambos_privado"
        ]

        # Crear DataFrame con estructura fija
        df_jardin = pd.DataFrame(columns=columns)
        # Asignar valores
        df_jardin["año"] = int(año)  # Año fijo
        df_jardin["id_provincia"] = df_provincias  # Provincias
        df_jardin.iloc[:, 2:5] = df_data_publico  # Asignar datos públicos
        df_jardin.iloc[:, 5:8] = df_data_privado  # Asignar datos privados

        # Crear las columnas sumadas
        df_jardin["ue_inicial_publico"] = df_jardin.iloc[:, 2:5].sum(axis=1)
        df_jardin["ue_inicial_privado"] = df_jardin.iloc[:, 5:8].sum(axis=1)

        # Eliminar las columnas originales si ya no son necesarias
        df_jardin = df_jardin.drop(columns=columns[2:8])

        return df_jardin
    
    @staticmethod
    def read_eu_primaria(name, año, sheet_index=1):
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
            "año", "id_provincia", 
            "primaria_6_años_publico", "primaria_7_años_publico", "primaria_6_años_privado",
            "primaria_7_años_privado"]
        
        # Crear DataFrame con estructura fija
        df_primaria = pd.DataFrame(columns=columns)
        # Asignar valores
        df_primaria["año"] = int(año)  # Año fijo
        df_primaria["id_provincia"] = df_provincias  # Provincias
        df_primaria.iloc[:, 2:4] = df_data_publico  # Asignar datos públicos
        df_primaria.iloc[:, 4:6] = df_data_privado  # Asignar datos privados

        # Crear las columnas sumadas
        df_primaria["ue_primaria_publico"] = df_primaria.iloc[:, 2:4].sum(axis=1)
        df_primaria["ue_primaria_privado"] = df_primaria.iloc[:, 4:6].sum(axis=1)

        # Eliminar las columnas originales si ya no son necesarias
        df_primaria = df_primaria.drop(columns=columns[2:8])

        return df_primaria
    
    @staticmethod
    def read_eu_secundaria(name, año, sheet_index=1):
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
            "año", "id_provincia", 
            "secundaria_ciclo_basico_publico", "secundaria_ciclo_orientado_publico", "secundaria_ciclo_basico_y_orientado_publico",
            "secundaria_ciclo_basico_privado", "secundaria_ciclo_orientado_privado", "secundaria_ciclo_basico_y_orientado_privado"
        ]
        
        # Crear DataFrame con estructura fija
        df_secundaria = pd.DataFrame(columns=columns)
        # Asignar valores
        df_secundaria["año"] = int(año)  # Año fijo
        df_secundaria["id_provincia"] = df_provincias  # Provincias
        df_secundaria.iloc[:, 2:5] = df_data_publico  # Asignar datos públicos
        df_secundaria.iloc[:, 5:8] = df_data_privado  # Asignar datos privados

        # Crear las columnas sumadas
        df_secundaria["ue_secundaria_publico"] = df_secundaria.iloc[:, 2:5].sum(axis=1)
        df_secundaria["ue_secundaria_privado"] = df_secundaria.iloc[:, 5:8].sum(axis=1)

        # Eliminar las columnas originales si ya no son necesarias
        df_secundaria = df_secundaria.drop(columns=columns[2:8])

        return df_secundaria
    
    @staticmethod
    def read_eu_no_universitario(name, año, sheet_index=1):
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
            "año", "id_provincia", 
            "ue_sup_nouniv_publico", 
            "ue_sup_nouniv_privado", 
        ]
        
        # Crear DataFrame con estructura fija
        df_superior_no_universitario = pd.DataFrame(columns=columns)
        # Asignar valores
        df_superior_no_universitario["año"] = int(año)
        df_superior_no_universitario["id_provincia"] = df_provincias  # Provincias
        df_superior_no_universitario.iloc[:, 2:3] = df_data_publico  # Asignar datos públicos
        df_superior_no_universitario.iloc[:, 3:4] = df_data_privado  # Asignar datos privados
        
        return df_superior_no_universitario