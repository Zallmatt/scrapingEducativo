import os
import pandas as pd
from utils.mappings import codigo_provincias_normalizado
from utils.normalization import normalize_name

class ReadExcelAlumnos:
    def load_route_excel(self, filename):
        """Retorna la ruta absoluta del archivo en la carpeta 'files'."""
        return os.path.join(os.path.dirname(__file__), "..", "files", "resumen", filename)

    def create_df_alumnos(self, filename, año):
        sheet_name = "Alumnos"
        file_path = self.load_route_excel(filename)

        df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)

        # Extraer datos desde celdas específicas
        df_provincias = df.iloc[41:67, 0].reset_index(drop=True)
        df_publico = df.iloc[41:67, 2:6].reset_index(drop=True)
        df_privado = df.iloc[76:102, 2:6].reset_index(drop=True)

        # Crear DataFrame base
        df_resultado = pd.DataFrame({
            "año": int(año),
            "id_provincia": df_provincias,
            "al_inicial_publico": df_publico.iloc[:, 0],
            "al_primaria_publico": df_publico.iloc[:, 1],
            "al_secundaria_publico": df_publico.iloc[:, 2],
            "al_sup_nouniv_publico": df_publico.iloc[:, 3],
            "al_inicial_privado": df_privado.iloc[:, 0],
            "al_primaria_privado": df_privado.iloc[:, 1],
            "al_secundaria_privado": df_privado.iloc[:, 2],
            "al_sup_nouniv_privado": df_privado.iloc[:, 3],
        })

        # Normalizar y mapear provincias
        df_resultado["prov_normalizada"] = df_resultado["id_provincia"].apply(normalize_name)
        df_resultado["id_provincia"] = df_resultado["prov_normalizada"].map(codigo_provincias_normalizado)

        # Filtrar filas válidas
        df_resultado = df_resultado[df_resultado["id_provincia"].notna()].drop(columns=["prov_normalizada"])

        # Convertir columnas numéricas a Int64 (excepto 'año' y 'id_provincia')
        columnas_numericas = [col for col in df_resultado.columns if col not in ["año", "id_provincia"]]
        for col in columnas_numericas:
            df_resultado[col] = pd.to_numeric(df_resultado[col], errors="coerce").astype("Int64")

        df_resultado["id_provincia"] = df_resultado["id_provincia"].astype("Int64")

        print("✅ DataFrame de alumnos generado:")
        print(df_resultado)

        return df_resultado
