import os
import pandas as pd
from utils.normalization import normalize_name
from utils.mappings import codigo_provincias_normalizado

class ReadExcelInicialAsistencia:
    @staticmethod
    def load_route_excel(name):
        return os.path.join(os.path.dirname(__file__), "..", "files", "inicial", name)

    def create_df_inicial_asistencia(self, filename, año):
        sheet_name = "Alu_asistencia 5"
        file_path = self.load_route_excel(filename)

        # Leer archivo
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)

        # Provincias y datos públicos y privados
        df_provincias = df.iloc[41:67, 0].reset_index(drop=True)
        df_publico = df.iloc[41:67, 1:3].reset_index(drop=True)
        df_privado = df.iloc[77:103, 1:3].reset_index(drop=True)

        df_resultado = pd.DataFrame({
            "año": int(año),
            "id_provincia": df_provincias,
            "al_asistencia_publico": df_publico.iloc[:, 0],
            "pcnt_asistencia_publico": df_publico.iloc[:, 1],
            "al_asistencia_privado": df_privado.iloc[:, 0],
            "pcnt_asistencia_privado": df_privado.iloc[:, 1]
        })

        # Normalizar y mapear provincias
        df_resultado["prov_normalizada"] = df_resultado["id_provincia"].apply(normalize_name)
        df_resultado["id_provincia"] = df_resultado["prov_normalizada"].map(codigo_provincias_normalizado)
        df_resultado = df_resultado[df_resultado["id_provincia"].notna()].drop(columns=["prov_normalizada"])

        # Convertir porcentajes a float y cantidades a Int64
        for col in df_resultado.columns:
            if "pcnt" in col:
                df_resultado[col] = pd.to_numeric(df_resultado[col], errors="coerce") / 100
            elif col.startswith("al_"):
                df_resultado[col] = pd.to_numeric(df_resultado[col], errors="coerce").astype("Int64")

        df_resultado["id_provincia"] = df_resultado["id_provincia"].astype("Int64")
        df_resultado["año"] = int(año)

        print("✅ DataFrame de asistencia inicial generado:")
        print(df_resultado)

        return df_resultado
