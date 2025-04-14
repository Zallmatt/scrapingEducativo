import os
import pandas as pd
from utils.normalization import normalize_name
from utils.mappings import codigo_provincias

class ReadDataExcelTasaEscolarizacion:
    def load_route_excel(self, name):
        """Devuelve la ruta absoluta al archivo Excel."""
        file_path = os.path.join(os.path.dirname(__file__), "../files", name)
        print(f"📄 Cargando archivo: {file_path}")
        return file_path

    def create_df_from_calculos(self):
        """Carga y procesa la hoja 'Calculos' con los datos finales de escolarización."""
        name = "Tasas de Escolarizacion 2022-2011.xlsx"
        file_path = self.load_route_excel(name)

        df = pd.read_excel(file_path, sheet_name="Calculos")

        # Normalizar nombres de provincias
        df["prov_normalizada"] = df["Provincia"].apply(normalize_name)

        # Mapear a códigos INDEC
        df["id_provincia"] = df["prov_normalizada"].map(codigo_provincias).astype("Int64")

        # Seleccionar y renombrar columnas finales
        df_final = df[[
            "id_provincia",
            "Año",
            "Esc_Total_Inicial",
            "Esc_Estructura_Educativa_P",
            "Esc_Total_Primaria",
            "Esc_Estructura_Educativa_S",
            "Esc_Total_Secundaria",
        ]]

        df_final = df_final[df_final["id_provincia"].notna()]

        print("✅ DataFrame escolarización final generado:")
        print(df_final.head())
        return df_final
