import os
import pandas as pd

class ReadExcelSecundarioRepitentes:
    @staticmethod
    def load_route_excel(name):
        """Obtiene la ruta absoluta del archivo en la carpeta 'files'"""
        file_path = os.path.join(os.path.dirname(__file__), "files", name)
        return file_path  # Retorna la ruta completa del archivo
    
    def create_df_secundario_repitentes(self, name, año):
        sheet_index = "Repitientes"

        """Carga los datos de la segunda hoja del Excel, tomando provincias de la fila 46 a la 71 y agrega los datos de nivel inicial desde loadEUInicial"""
        file_path = ReadExcelSecundarioRepitentes.load_route_excel(name)

        # Cargar la segunda hoja del archivo Excel
        df = pd.read_excel(file_path, sheet_name=sheet_index, header=None)

        # Extraer las provincias y el año
        df_provincias = df.iloc[48:74, 0].reset_index(drop=True)  # Columna A (Índice 0)
        df_datos_publico = df.iloc[48:74, 1:10].reset_index(drop=True)
        df_datos_privado = df.iloc[88:114, 1:10].reset_index(drop=True)
        
        print(df_datos_publico)
        print(df_datos_privado)

        # Crear un DataFrame con la estructura esperada
        columns = [
            "año", "id_provincia", 
            "total_publico", "7mo_publico", "8vo_publico", "9no_publico", "10mo_publico", "11vo_publico", "12vo_publico", "13vo_y_14vo_publico", "planes_no_graduados_publico",
            "total_privado", "7mo_privado", "8vo_privado", "9no_privado", "10mo_privado", "11vo_privado", "12vo_privado", "13vo_y_14vo_privado", "planes_no_graduados_privado"
        ]

        # Crear DataFrame con estructura fija
        df_nivel_secundario_repitentes = pd.DataFrame(columns=columns)
        df_nivel_secundario_repitentes["id_provincia"] = df_provincias  # Agregar provincias
        df_nivel_secundario_repitentes["año"] = año

        # Datos públicos
        df_nivel_secundario_repitentes["total_publico"] = df_datos_publico.iloc[:, 0]
        df_nivel_secundario_repitentes["7mo_publico"] = df_datos_publico.iloc[:, 1]
        df_nivel_secundario_repitentes["8vo_publico"] = df_datos_publico.iloc[:, 2]
        df_nivel_secundario_repitentes["9no_publico"] = df_datos_publico.iloc[:, 3]
        df_nivel_secundario_repitentes["10mo_publico"] = df_datos_publico.iloc[:, 4]
        df_nivel_secundario_repitentes["11vo_publico"] = df_datos_publico.iloc[:, 5]
        df_nivel_secundario_repitentes["12vo_publico"] = df_datos_publico.iloc[:, 6]
        df_nivel_secundario_repitentes["13vo_y_14vo_publico"] = df_datos_publico.iloc[:, 7]
        df_nivel_secundario_repitentes["planes_no_graduados_publico"] = df_datos_publico.iloc[:, 8]

        # Datos privados
        df_nivel_secundario_repitentes["total_privado"] = df_datos_privado.iloc[:, 0]
        df_nivel_secundario_repitentes["7mo_privado"] = df_datos_privado.iloc[:, 1]
        df_nivel_secundario_repitentes["8vo_privado"] = df_datos_privado.iloc[:, 2]
        df_nivel_secundario_repitentes["9no_privado"] = df_datos_privado.iloc[:, 3]
        df_nivel_secundario_repitentes["10mo_privado"] = df_datos_privado.iloc[:, 4]
        df_nivel_secundario_repitentes["11vo_privado"] = df_datos_privado.iloc[:, 5]
        df_nivel_secundario_repitentes["12vo_privado"] = df_datos_privado.iloc[:, 6]
        df_nivel_secundario_repitentes["13vo_y_14vo_privado"] = df_datos_privado.iloc[:, 7]
        df_nivel_secundario_repitentes["planes_no_graduados_privado"] = df_datos_privado.iloc[:, 8]


        # Convertir NaN a None (NULL en la base de datos)
        df_nivel_secundario_repitentes = df_nivel_secundario_repitentes.where(pd.notna(df_nivel_secundario_repitentes), None)
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
        df_nivel_secundario_repitentes["id_provincia"] = df_nivel_secundario_repitentes["id_provincia"].replace(codigo_provincias)
        
        # Limpieza
        df_nivel_secundario_repitentes = df_nivel_secundario_repitentes[~df_nivel_secundario_repitentes["id_provincia"].isin(["Conurbano", "Buenos Aires Resto"])]

        for col in df_nivel_secundario_repitentes.columns:
            df_nivel_secundario_repitentes[col] = df_nivel_secundario_repitentes[col].apply(lambda x: None if x is None else int(x))
        
        return df_nivel_secundario_repitentes