import os
import pandas as pd

class ReadExcelHoras:
    @staticmethod
    def load_route_excel(name):
        return os.path.join(os.path.dirname(__file__), "..", "files", "resumen", name)
    
    def create_df_cargos(self, name, año):
        
        sheet_index="Horas"

        """Carga los datos de la segunda hoja del Excel, tomando provincias de la fila 46 a la 71 y agrega los datos de nivel inicial desde loadEUInicial"""
        file_path = ReadExcelHoras.load_route_excel(name)

        # Cargar la segunda hoja del archivo Excel
        df = pd.read_excel(file_path, sheet_name=sheet_index, header=None)

        # Extraer las provincias y el año (Columna A, filas 46 a 71 en base 1 → 45 a 70 en base 0)
        df_provincias = df.iloc[50:76, 0].reset_index(drop=True)  # Columna A (Índice 0)
        df_datos_publico = df.iloc[50:76, 2:10].reset_index(drop=True)
        df_datos_privado = df.iloc[92:118, 2:10].reset_index(drop=True)

        # Crear un DataFrame con la estructura esperada
        columns = [
            "año", "id_provincia",
            "h_planta_inicial_publico", "h_planta_inicial_privado",
            "h_planta_primaria_publico", "h_planta_primaria_privado",
            "h_planta_secundaria_publico", "h_planta_secundaria_privado",
            "h_planta_sup_nouniv_publico", "h_planta_sup_nouniv_privado",
            "h_fuera_inicial_publico", "h_fuera_inicial_privado",
            "h_fuera_primaria_publico", "h_fuera_primaria_privado",
            "h_fuera_secundaria_publico", "h_fuera_secundaria_privado",
            "h_fuera_sup_nouniv_publico", "h_fuera_sup_nouniv_privado"
        ]

        # Crear DataFrame con estructura fija
        df_educacion_comun_horas = pd.DataFrame(columns=columns)
        df_educacion_comun_horas["id_provincia"] = df_provincias  # Agregar provincias
        df_educacion_comun_horas["año"] = año

        #Datos publicos
        df_educacion_comun_horas["h_planta_inicial_publico"] = df_datos_publico.iloc[:, 0]
        df_educacion_comun_horas["h_planta_primaria_publico"] = df_datos_publico.iloc[:, 1]
        df_educacion_comun_horas["h_planta_secundaria_publico"] = df_datos_publico.iloc[:, 2]
        df_educacion_comun_horas["h_planta_sup_nouniv_publico"] = df_datos_publico.iloc[:, 3]
        df_educacion_comun_horas["h_fuera_inicial_publico"] = df_datos_publico.iloc[:, 4]
        df_educacion_comun_horas["h_fuera_primaria_publico"] = df_datos_publico.iloc[:, 5]
        df_educacion_comun_horas["h_fuera_secundaria_publico"] = df_datos_publico.iloc[:, 6]
        df_educacion_comun_horas["h_fuera_sup_nouniv_publico"] = df_datos_publico.iloc[:, 7]
        #Datos privados
        df_educacion_comun_horas["h_planta_inicial_privado"] = df_datos_privado.iloc[:, 0]
        df_educacion_comun_horas["h_planta_primaria_privado"] = df_datos_privado.iloc[:, 1]
        df_educacion_comun_horas["h_planta_secundaria_privado"] = df_datos_privado.iloc[:, 2]
        df_educacion_comun_horas["h_planta_sup_nouniv_privado"] = df_datos_privado.iloc[:, 3]
        df_educacion_comun_horas["h_fuera_inicial_privado"] = df_datos_privado.iloc[:, 4]
        df_educacion_comun_horas["h_fuera_primaria_privado"] = df_datos_privado.iloc[:, 5]
        df_educacion_comun_horas["h_fuera_secundaria_privado"] = df_datos_privado.iloc[:, 6]
        df_educacion_comun_horas["h_fuera_sup_nouniv_privado"] = df_datos_privado.iloc[:, 7]

        # Convertir NaN a None (NULL en la base de datos)
        df_educacion_comun_horas = df_educacion_comun_horas.where(pd.notna(df_educacion_comun_horas), None)
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
        df_educacion_comun_horas["id_provincia"] = df_educacion_comun_horas["id_provincia"].replace(codigo_provincias)
        
        # Limpieza
        df_educacion_comun_horas = df_educacion_comun_horas[~df_educacion_comun_horas["id_provincia"].isin(["Conurbano", "Buenos Aires Resto"])]

        # Convertir todas las columnas excepto 'provincia' a tipo entero, manteniendo None como NULL
        for col in df_educacion_comun_horas.columns:
            df_educacion_comun_horas[col] = df_educacion_comun_horas[col].apply(lambda x: None if x is None else int(x))
        
        print(df_educacion_comun_horas)
        
        return df_educacion_comun_horas

    