import os
import pandas as pd

class ReadExcelAlumnos:
    def load_route_excel(self, name):
        """Obtiene la ruta absoluta del archivo en la carpeta 'files'"""
        file_path = os.path.join(os.path.dirname(__file__), "files", name)
        return file_path  # Retorna la ruta completa del archivo
    
    def create_df_alumnos(self):
        name = "RESUMEN_2023.xlsx"
        sheet_name = "Alumnos"  # Nombre de la hoja en el Excel

        file_path = self.load_route_excel(name)

        # Cargar la hoja sin tomar la primera fila como nombres de columnas
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
        
        # Extraer las provincias y el año
        df_provincias = df.iloc[42:68, 0].reset_index(drop=True)  # Columna A (Índice 0)
        
        df_datos_publico = df.iloc[42:68, 2:6].reset_index(drop=True)  # Columnas C a F (Índices 2 a 5)
        df_datos_privado = df.iloc[77:103, 2:6].reset_index(drop=True)  # Columnas C a F (Índices 2 a 5)

        # Crear un DataFrame con la estructura esperada
        columns = [
            "año", "provincia", 
            "al_inicial_publico", "al_inicial_privado", 
            "al_primaria_publico", "al_primaria_privado", 
            "al_secundaria_publico", "al_secundaria_privado", 
            "al_sup_nouniv_publico", "al_sup_nouniv_privado"
        ]

        df_alumnos = pd.DataFrame(columns=columns)
        df_alumnos["provincia"] = df_provincias
        df_alumnos["año"] = 2023  # Año fijo

        # Asignar los datos públicos y privados
        df_alumnos["al_inicial_publico"] = df_datos_publico.iloc[:, 0]
        df_alumnos["al_primaria_publico"] = df_datos_publico.iloc[:, 1]
        df_alumnos["al_secundaria_publico"] = df_datos_publico.iloc[:, 2]
        df_alumnos["al_sup_nouniv_publico"] = df_datos_publico.iloc[:, 3]

        df_alumnos["al_inicial_privado"] = df_datos_privado.iloc[:, 0]
        df_alumnos["al_primaria_privado"] = df_datos_privado.iloc[:, 1]
        df_alumnos["al_secundaria_privado"] = df_datos_privado.iloc[:, 2]
        df_alumnos["al_sup_nouniv_privado"] = df_datos_privado.iloc[:, 3]

        # Convertir NaN a None (NULL en la base de datos)
        df_alumnos = df_alumnos.where(pd.notna(df_alumnos), None)

        # Convertir todas las columnas excepto 'provincia' a tipo entero, manteniendo None como NULL
        for col in df_alumnos.columns:
            if col != "provincia":
                df_alumnos[col] = df_alumnos[col].apply(lambda x: None if x is None else int(x))

        return df_alumnos
