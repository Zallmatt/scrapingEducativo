import os
import pandas as pd

class ReadExcelPrimarioRepitentes:
    @staticmethod
    def load_route_excel(name):
        """Obtiene la ruta absoluta del archivo en la carpeta 'files'"""
        file_path = os.path.join(os.path.dirname(__file__), "files", name)
        return file_path  # Retorna la ruta completa del archivo
    
    def create_df_primario_repitentes(self, name):
        sheet_index = "Alu_Repitientes"

        """Carga los datos de la segunda hoja del Excel, tomando provincias de la fila 46 a la 71 y agrega los datos de nivel inicial desde loadEUInicial"""
        file_path = ReadExcelPrimarioRepitentes.load_route_excel(name)

        # Cargar la segunda hoja del archivo Excel
        df = pd.read_excel(file_path, sheet_name=sheet_index, header=None)

        # Extraer las provincias y el año
        df_provincias = df.iloc[47:73, 0].reset_index(drop=True)  # Columna A (Índice 0)
        df_datos_publico = df.iloc[47:73, 1:9].reset_index(drop=True)
        df_datos_privado = df.iloc[87:113, 1:9].reset_index(drop=True)
        
        print(df_datos_publico)
        print(df_datos_privado)

        # Crear un DataFrame con la estructura esperada
        columns = [
            "año", "id_provincia", "total_publico",
            "1ero_publico", "2do_publico", "3ero_publico", "4to_publico", "5to_publico", "6to_publico", "7mo_publico",
            "total_privado", "1ero_privado", "2do_privado", "3ero_privado", "4to_privado", "5to_privado", "6to_privado", "7mo_privado"
        ]

        # Crear DataFrame con estructura fija
        df_primario_repitentes = pd.DataFrame(columns=columns)
        df_primario_repitentes["id_provincia"] = df_provincias  # Agregar provincias
        df_primario_repitentes["año"] = 2023

        # Datos públicos
        df_primario_repitentes["total_publico"] = df_datos_publico.iloc[:, 0]
        df_primario_repitentes["1ero_publico"] = df_datos_publico.iloc[:, 1]
        df_primario_repitentes["2do_publico"] = df_datos_publico.iloc[:, 2]
        df_primario_repitentes["3ero_publico"] = df_datos_publico.iloc[:, 3]
        df_primario_repitentes["4to_publico"] = df_datos_publico.iloc[:, 4]
        df_primario_repitentes["5to_publico"] = df_datos_publico.iloc[:, 5]
        df_primario_repitentes["6to_publico"] = df_datos_publico.iloc[:, 6]
        df_primario_repitentes["7mo_publico"] = df_datos_publico.iloc[:, 7]


        # Datos privados
        df_primario_repitentes["total_privado"] = df_datos_privado.iloc[:, 0]
        df_primario_repitentes["1ero_privado"] = df_datos_privado.iloc[:, 1]
        df_primario_repitentes["2do_privado"] = df_datos_privado.iloc[:, 2]
        df_primario_repitentes["3ero_privado"] = df_datos_privado.iloc[:, 3]
        df_primario_repitentes["4to_privado"] = df_datos_privado.iloc[:, 4]
        df_primario_repitentes["5to_privado"] = df_datos_privado.iloc[:, 5]
        df_primario_repitentes["6to_privado"] = df_datos_privado.iloc[:, 6]
        df_primario_repitentes["7mo_privado"] = df_datos_privado.iloc[:, 7]

        # Convertir NaN a None (NULL en la base de datos)
        df_primario_repitentes = df_primario_repitentes.where(pd.notna(df_primario_repitentes), None)
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
        df_primario_repitentes["id_provincia"] = df_primario_repitentes["id_provincia"].replace(codigo_provincias)
        
        # Limpieza
        df_primario_repitentes = df_primario_repitentes[~df_primario_repitentes["id_provincia"].isin(["Conurbano", "Buenos Aires Resto"])]
        for col in df_primario_repitentes.columns:
            df_primario_repitentes[col] = df_primario_repitentes[col].apply(lambda x: None if x is None else int(x))
        
        return df_primario_repitentes