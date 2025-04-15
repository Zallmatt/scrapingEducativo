import os
import pandas as pd
from utils.normalization import normalize_name
from utils.mappings import codigo_provincias_normalizado

class ReadExcelSecundarioRepitentes:
    @staticmethod
    def load_route_excel(name):
        return os.path.join(os.path.dirname(__file__), "..", "files", name)

    def create_df_secundario_repitentes(self, name, año):
        sheet_name = "Repitientes"
        file_path = self.load_route_excel(name)

        df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)

        df_provincias = df.iloc[48:74, 0].reset_index(drop=True)
        df_publico = df.iloc[48:74, 1:10].reset_index(drop=True)
        df_privado = df.iloc[88:114, 1:10].reset_index(drop=True)

        df_resultado = pd.DataFrame({
            "año": int(año),
            "id_provincia": df_provincias,
            "total_publico": df_publico.iloc[:, 0],
            "7mo_publico": df_publico.iloc[:, 1],
            "8vo_publico": df_publico.iloc[:, 2],
            "9no_publico": df_publico.iloc[:, 3],
            "10mo_publico": df_publico.iloc[:, 4],
            "11vo_publico": df_publico.iloc[:, 5],
            "12vo_publico": df_publico.iloc[:, 6],
            "13vo_y_14vo_publico": df_publico.iloc[:, 7],
            "planes_no_graduados_publico": df_publico.iloc[:, 8],
            "total_privado": df_privado.iloc[:, 0],
            "7mo_privado": df_privado.iloc[:, 1],
            "8vo_privado": df_privado.iloc[:, 2],
            "9no_privado": df_privado.iloc[:, 3],
            "10mo_privado": df_privado.iloc[:, 4],
            "11vo_privado": df_privado.iloc[:, 5],
            "12vo_privado": df_privado.iloc[:, 6],
            "13vo_y_14vo_privado": df_privado.iloc[:, 7],
            "planes_no_graduados_privado": df_privado.iloc[:, 8],
        })

        # Normalizar nombres de provincia y mapear
        df_resultado["prov_normalizada"] = df_resultado["id_provincia"].apply(normalize_name)
        df_resultado["id_provincia"] = df_resultado["prov_normalizada"].map(codigo_provincias_normalizado)
        df_resultado = df_resultado[df_resultado["id_provincia"].notna()].drop(columns=["prov_normalizada"])

        # Conversión segura a Int64
        columnas_numericas = [col for col in df_resultado.columns if col not in ["año", "id_provincia"]]
        for col in columnas_numericas:
            df_resultado[col] = pd.to_numeric(df_resultado[col], errors="coerce").astype("Int64")

        df_resultado["id_provincia"] = df_resultado["id_provincia"].astype("Int64")
        df_resultado["año"] = int(año)

        print("✅ DataFrame de repitencia secundaria generado:")
        print(df_resultado.head())

        return df_resultado
