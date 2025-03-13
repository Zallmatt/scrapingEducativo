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
            "año", "provincia",
            "al_asistencia_publico", "al_asistencia_privado",
            "pcnt_asistencia_publico", "pcnt_asistencia_privado"
        ]

        # Crear DataFrame con estructura fija
        df_inicial_asistencia = pd.DataFrame(columns=columns)
        df_inicial_asistencia["provincia"] = df_provincias  # Agregar provincias
        df_inicial_asistencia["año"] = 2023

        # Datos públicos
        df_inicial_asistencia["al_asistencia_publico"] = df_datos_publico.iloc[:, 0]
        df_inicial_asistencia["pcnt_asistencia_publico"] = df_datos_publico.iloc[:, 1]

        # Datos privados
        df_inicial_asistencia["al_asistencia_privado"] = df_datos_privado.iloc[:, 0]
        df_inicial_asistencia["pcnt_asistencia_privado"] = df_datos_privado.iloc[:, 1]

        # Convertir NaN a None (NULL en la base de datos)
        df_inicial_asistencia = df_inicial_asistencia.where(pd.notna(df_inicial_asistencia), None)

        # 🔹 Convertir columnas de porcentaje a float y dividir por 100
        for col in df_inicial_asistencia.columns:
            if "pcnt" in col:
                df_inicial_asistencia[col] = df_inicial_asistencia[col].apply(lambda x: None if x is None else float(x) / 100)
            elif col not in ["provincia", "año"]:  # Convertir el resto a int
                df_inicial_asistencia[col] = df_inicial_asistencia[col].apply(lambda x: None if x is None else int(x))
        
        return df_inicial_asistencia
