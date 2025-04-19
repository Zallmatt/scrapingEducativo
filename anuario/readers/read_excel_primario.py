import os
import pandas as pd
from utils.normalization import normalize_name
from utils.mappings import codigo_provincias_normalizado

class ReadExcelPrimarioRepitentes:
    @staticmethod
    def load_route_excel(name):
        return os.path.join(os.path.dirname(__file__), "..", "files", "primario", name)

    def create_df_primario_repitentes(self, name, año):
        sheet_index = "Alu_Repitientes"
        file_path = self.load_route_excel(name)

        df = pd.read_excel(file_path, sheet_name=sheet_index, header=None)

        df_provincias = df.iloc[44:70, 0].reset_index(drop=True)
        df_publico = df.iloc[44:70, 1:9].reset_index(drop=True)
        df_privado = df.iloc[82:108, 1:9].reset_index(drop=True)

        df_resultado = pd.DataFrame({
            "año": int(año),
            "id_provincia": df_provincias,
            "total_publico": df_publico.iloc[:, 0],
            "1ero_publico": df_publico.iloc[:, 1],
            "2do_publico": df_publico.iloc[:, 2],
            "3ero_publico": df_publico.iloc[:, 3],
            "4to_publico": df_publico.iloc[:, 4],
            "5to_publico": df_publico.iloc[:, 5],
            "6to_publico": df_publico.iloc[:, 6],
            "7mo_publico": df_publico.iloc[:, 7],
            "total_privado": df_privado.iloc[:, 0],
            "1ero_privado": df_privado.iloc[:, 1],
            "2do_privado": df_privado.iloc[:, 2],
            "3ero_privado": df_privado.iloc[:, 3],
            "4to_privado": df_privado.iloc[:, 4],
            "5to_privado": df_privado.iloc[:, 5],
            "6to_privado": df_privado.iloc[:, 6],
            "7mo_privado": df_privado.iloc[:, 7],
        })

        # Normalizar y mapear provincias
        df_resultado["prov_normalizada"] = df_resultado["id_provincia"].apply(normalize_name)
        df_resultado["id_provincia"] = df_resultado["prov_normalizada"].map(codigo_provincias_normalizado)
        df_resultado = df_resultado[df_resultado["id_provincia"].notna()].drop(columns=["prov_normalizada"])

        # Conversión segura a numérico
        columnas_numericas = [col for col in df_resultado.columns if col not in ["año", "id_provincia"]]
        for col in columnas_numericas:
            df_resultado[col] = pd.to_numeric(df_resultado[col], errors="coerce").astype("Int64")

        df_resultado["id_provincia"] = df_resultado["id_provincia"].astype("Int64")
        df_resultado["año"] = int(año)

        print("✅ DataFrame de repitencia primaria generado:")
        print(df_resultado)

        return df_resultado
