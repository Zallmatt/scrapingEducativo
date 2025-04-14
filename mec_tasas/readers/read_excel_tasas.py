import os
import pandas as pd

class ReadDataExcelTasas:
    def load_route_excel(self, name):
        """Obtiene la ruta absoluta del archivo en la carpeta 'files'"""
        file_path = os.path.join(os.path.dirname(__file__), "files", name)
        print(f"📄 Cargando archivo: {file_path}")
        return file_path  
    
    def create_df_mec_tasas(self):
        name = "Evolucion_2011-2024.xlsx"
        sheet_name = "Tasas 2011-2024"

        file_path = self.load_route_excel(name)

        try:
            # Cargar hoja sin encabezado y eliminar la primera fila (títulos visuales)
            df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
            df = df.iloc[1:].reset_index(drop=True)

            print(f"🧾 Número de columnas detectadas: {df.shape[1]}")

            column_names = [
                "tasas", "ra_ano", "div_geografica", "sector", "nivel", "total", 
                "1er_ano", "2do_ano", "3er_ano", "4to_ano", "5to_ano", "6to_ano"
            ]

            if len(column_names) == df.shape[1]:
                df.columns = column_names
            else:
                raise ValueError("❌ El número de columnas no coincide con el esperado.")

            df = df.where(pd.notna(df), None)

            print("✅ DataFrame MEC tasas generado correctamente:")
            print(df.head())

            return df

        except Exception as e:
            print(f"⚠️ Error al procesar el archivo: {e}")
            return pd.DataFrame()  # Devuelve un DataFrame vacío en caso de error
