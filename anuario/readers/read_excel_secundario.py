import os
import pandas as pd
from utils.normalization import normalize_name
from utils.mappings import codigo_provincias_normalizado

class ReadExcelSecundarioRepitentes:
    @staticmethod
    def load_route_excel(name):
        return os.path.join(os.path.dirname(__file__), "..", "files", "secundario", name)

    def create_df_secundario_repitentes(self, name, año):
        sheet_name = "Repitientes"
        file_path = self.load_route_excel(name)

        df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)

        df_provincias = df.iloc[42:68, 0].reset_index(drop=True)
        df_publico = df.iloc[42:68, 1:10].reset_index(drop=True)
        df_privado = df.iloc[78:104, 1:10].reset_index(drop=True)

        # Chequear si existen las columnas de "planes no graduados"
        tiene_planes_no_graduados = df_publico.shape[1] >= 9 and df_privado.shape[1] >= 9

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
            "planes_no_graduados_publico": df_publico.iloc[:, 8] if tiene_planes_no_graduados else pd.NA,
            "total_privado": df_privado.iloc[:, 0],
            "7mo_privado": df_privado.iloc[:, 1],
            "8vo_privado": df_privado.iloc[:, 2],
            "9no_privado": df_privado.iloc[:, 3],
            "10mo_privado": df_privado.iloc[:, 4],
            "11vo_privado": df_privado.iloc[:, 5],
            "12vo_privado": df_privado.iloc[:, 6],
            "13vo_y_14vo_privado": df_privado.iloc[:, 7],
            "planes_no_graduados_privado": df_privado.iloc[:, 8] if tiene_planes_no_graduados else pd.NA,
        })

        # Normalizar nombres de provincia y mapear
        df_resultado["prov_normalizada"] = df_resultado["id_provincia"].apply(normalize_name)
        df_resultado["id_provincia"] = df_resultado["prov_normalizada"].map(codigo_provincias_normalizado)
        df_resultado = df_resultado[df_resultado["id_provincia"].notna()].drop(columns=["prov_normalizada"])

        # Orden final fijo (para asegurar consistencia con la base)
        columnas_ordenadas = [
            "año", "id_provincia",
            "total_publico", "7mo_publico", "8vo_publico", "9no_publico", "10mo_publico",
            "11vo_publico", "12vo_publico", "13vo_y_14vo_publico", "planes_no_graduados_publico",
            "total_privado", "7mo_privado", "8vo_privado", "9no_privado", "10mo_privado",
            "11vo_privado", "12vo_privado", "13vo_y_14vo_privado", "planes_no_graduados_privado"
        ]

        # Asegurar que todas estén presentes
        for col in columnas_ordenadas:
            if col not in df_resultado.columns:
                df_resultado[col] = pd.NA

        # Reordenar
        df_resultado = df_resultado[columnas_ordenadas]

        # Convertir tipos a Int64
        for col in columnas_ordenadas:
            if col not in ["año", "id_provincia"]:
                df_resultado[col] = pd.to_numeric(df_resultado[col], errors="coerce").astype("Int64")

        df_resultado["id_provincia"] = df_resultado["id_provincia"].astype("Int64")
        df_resultado["año"] = int(año)

        print("✅ DataFrame de repitencia secundaria generado:")
        print(df_resultado)

        return df_resultado
