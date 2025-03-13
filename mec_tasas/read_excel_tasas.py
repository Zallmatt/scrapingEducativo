import os
import pandas as pd

class ReadDataExcelTasas:
    def load_route_excel(self, name):
        """Obtiene la ruta absoluta del archivo en la carpeta 'files'"""
        file_path = os.path.join(os.path.dirname(__file__), "files", name)
        print(f"Cargando archivo: {file_path}")
        return file_path  
    
    def create_df_mec_tasas(self):
        name = "Evolucion_2011-2024.xlsx"
        sheet_name = "Tasas 2011-2024"  # Nombre de la hoja en el Excel

        """Carga los datos de la hoja específica del Excel sin tomar la primera fila como nombres de columna"""
        file_path = self.load_route_excel(name)

        # Cargar la hoja con su nombre, sin tomar la primera fila como nombres de columnas
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)

        # Eliminar la primera fila que contiene los encabezados originales
        df = df.iloc[1:].reset_index(drop=True)

        # Verificar cuántas columnas tiene realmente
        print(f"Número de columnas en el archivo: {df.shape[1]}")

        # Definir los nombres de las columnas (12 columnas porque va de A a L)
        column_names = [
            "tasas", "ra_ano", "div_geografica", "sector", "nivel", "total", 
            "1er_ano", "2do_ano", "3er_ano", "4to_ano", "5to_ano", "6to_ano"
        ]

        # Asegurar que la cantidad de nombres de columna coincida con las columnas del DataFrame
        if len(column_names) == df.shape[1]:
            df.columns = column_names
        else:
            print("⚠️ Advertencia: El número de columnas en el Excel no coincide con la cantidad de nombres definidos.")
        
        df = df.where(pd.notna(df), None)
        print(df)  # Muestra las primeras filas para verificar la carga
        return df