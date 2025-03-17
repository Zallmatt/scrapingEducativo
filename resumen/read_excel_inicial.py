import os
import pandas as pd

class ReadExcelInicialAsistencia:
    @staticmethod
    def load_route_excel(name):
        """Obtiene la ruta absoluta del archivo en la carpeta 'files'"""
        file_path = os.path.join(os.path.dirname(__file__), "files", name)
        return file_path  # Retorna la ruta completa del archivo
    
    def create_df_inicial_asistencia(self, name):
        sheet_index = "Alu_asistencia 5"

        """Carga los datos de la segunda hoja del Excel, tomando provincias de la fila 46 a la 71 y agrega los datos de nivel inicial desde loadEUInicial"""
        file_path = ReadExcelInicialAsistencia.load_route_excel(name)

        # Cargar la segunda hoja del archivo Excel
        df = pd.read_excel(file_path, sheet_name=sheet_index, header=None)

        # Extraer las provincias y el año
        df_provincias = df.iloc[41:67, 0].reset_index(drop=True)  # Columna A (Índice 0)
        df_datos_publico = df.iloc[41:67, 1:3].reset_index(drop=True)
        df_datos_privado = df.iloc[76:102, 1:3].reset_index(drop=True)

        # Crear un DataFrame con la estructura esperada
        columns = [
            "año", "id_provincia",
            "al_asistencia_publico", "al_asistencia_privado",
            "pcnt_asistencia_publico", "pcnt_asistencia_privado"
        ]

        # Crear DataFrame con estructura fija
        df_inicial_asistencia = pd.DataFrame(columns=columns)
        df_inicial_asistencia["id_provincia"] = df_provincias  # Agregar provincias
        df_inicial_asistencia["año"] = 2023

        # Datos públicos
        df_inicial_asistencia["al_asistencia_publico"] = df_datos_publico.iloc[:, 0]
        df_inicial_asistencia["pcnt_asistencia_publico"] = df_datos_publico.iloc[:, 1]

        # Datos privados
        df_inicial_asistencia["al_asistencia_privado"] = df_datos_privado.iloc[:, 0]
        df_inicial_asistencia["pcnt_asistencia_privado"] = df_datos_privado.iloc[:, 1]

        # Convertir NaN a None (NULL en la base de datos)
        df_inicial_asistencia = df_inicial_asistencia.where(pd.notna(df_inicial_asistencia), None)
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
        df_inicial_asistencia["id_provincia"] = df_inicial_asistencia["id_provincia"].replace(codigo_provincias)
        
        # Limpieza
        df_inicial_asistencia = df_inicial_asistencia[~df_inicial_asistencia["id_provincia"].isin(["Conurbano", "Buenos Aires Resto"])]

        # 🔹 Convertir columnas de porcentaje a float y dividir por 100
        for col in df_inicial_asistencia.columns:
            if "pcnt" in col:
                df_inicial_asistencia[col] = pd.to_numeric(df_inicial_asistencia[col], errors="coerce") / 100
            elif col in ["id_provincia", "año"]:  # Convertir el resto a int
                df_inicial_asistencia[col] = pd.to_numeric(df_inicial_asistencia[col], errors="coerce", downcast="integer")
        
        return df_inicial_asistencia
