import os
import pandas as pd

class ReadExcelCargos:
    @staticmethod
    def load_route_excel(name):
        """Obtiene la ruta absoluta del archivo en la carpeta 'files'"""
        file_path = os.path.join(os.path.dirname(__file__), "files", name)
        return file_path  # Retorna la ruta completa del archivo
    
    def create_df_cargos(self, name):
        
        sheet_index="Cargos"

        """Carga los datos de la segunda hoja del Excel, tomando provincias de la fila 46 a la 71 y agrega los datos de nivel inicial desde loadEUInicial"""
        file_path = ReadExcelCargos.load_route_excel(name)

        # Cargar la segunda hoja del archivo Excel
        df = pd.read_excel(file_path, sheet_name=sheet_index, header=None)

        # Extraer las provincias y el año (Columna A, filas 46 a 71 en base 1 → 45 a 70 en base 0)
        df_provincias = df.iloc[47:73, 0].reset_index(drop=True)  # Columna A (Índice 0)
        df_datos_publico = df.iloc[47:73, 2:10].reset_index(drop=True)
        df_datos_privado = df.iloc[86:112, 2:10].reset_index(drop=True)

        # Crear un DataFrame con la estructura esperada
        columns = [
            "año", "provincia",
            "c_planta_inicial_publico", "c_planta_inicial_privado",
            "c_planta_primaria_publico", "c_planta_primaria_privado",
            "c_planta_secundaria_publico", "c_planta_secundaria_privado",
            "c_planta_sup_nouniv_publico", "c_planta_sup_nouniv_privado",
            "c_fuera_inicial_publico", "c_fuera_inicial_privado",
            "c_fuera_primaria_publico", "c_fuera_primaria_privado",
            "c_fuera_secundaria_publico", "c_fuera_secundaria_privado",
            "c_fuera_sup_nouniv_publico", "c_fuera_sup_nouniv_privado"
        ]

        # Crear DataFrame con estructura fija
        df_educacion_comun_cargos = pd.DataFrame(columns=columns)
        df_educacion_comun_cargos["provincia"] = df_provincias  # Agregar provincias
        df_educacion_comun_cargos["año"] = 2023

        #Datos publicos
        df_educacion_comun_cargos["c_planta_inicial_publico"] = df_datos_publico.iloc[:, 0]
        df_educacion_comun_cargos["c_planta_primaria_publico"] = df_datos_publico.iloc[:, 1]
        df_educacion_comun_cargos["c_planta_secundaria_publico"] = df_datos_publico.iloc[:, 2]
        df_educacion_comun_cargos["c_planta_sup_nouniv_publico"] = df_datos_publico.iloc[:, 3]
        df_educacion_comun_cargos["c_fuera_inicial_publico"] = df_datos_publico.iloc[:, 4]
        df_educacion_comun_cargos["c_fuera_primaria_publico"] = df_datos_publico.iloc[:, 5]
        df_educacion_comun_cargos["c_fuera_secundaria_publico"] = df_datos_publico.iloc[:, 6]
        df_educacion_comun_cargos["c_fuera_sup_nouniv_publico"] = df_datos_publico.iloc[:, 7]
        #Datos privados
        df_educacion_comun_cargos["c_planta_inicial_privado"] = df_datos_privado.iloc[:, 0]
        df_educacion_comun_cargos["c_planta_primaria_privado"] = df_datos_privado.iloc[:, 1]
        df_educacion_comun_cargos["c_planta_secundaria_privado"] = df_datos_privado.iloc[:, 2]
        df_educacion_comun_cargos["c_planta_sup_nouniv_privado"] = df_datos_privado.iloc[:, 3]
        df_educacion_comun_cargos["c_fuera_inicial_privado"] = df_datos_privado.iloc[:, 4]
        df_educacion_comun_cargos["c_fuera_primaria_privado"] = df_datos_privado.iloc[:, 5]
        df_educacion_comun_cargos["c_fuera_secundaria_privado"] = df_datos_privado.iloc[:, 6]
        df_educacion_comun_cargos["c_fuera_sup_nouniv_privado"] = df_datos_privado.iloc[:, 7]

        # Convertir NaN a None (NULL en la base de datos)
        df_educacion_comun_cargos = df_educacion_comun_cargos.where(pd.notna(df_educacion_comun_cargos), None)

        # Convertir todas las columnas excepto 'provincia' a tipo entero, manteniendo None como NULL
        for col in df_educacion_comun_cargos.columns:
            if col != "provincia":
                df_educacion_comun_cargos[col] = df_educacion_comun_cargos[col].apply(lambda x: None if x is None else int(x))
        
        return df_educacion_comun_cargos
