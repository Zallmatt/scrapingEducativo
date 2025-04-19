import os
import pandas as pd
from utils.mappings import codigo_provincias_normalizado
from utils.normalization import normalize_name

class ReadExcelCargos:
    def load_route_excel(self, filename):
        """Devuelve la ruta absoluta del archivo dentro de data/files."""
        return os.path.join(os.path.dirname(__file__), "..", "files", "resumen", filename)

    def create_df_cargos(self, filename, anio):
        sheet_name = "Cargos"
        file_path = self.load_route_excel(filename)

        df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)

        df_provincias = df.iloc[44:70, 0].reset_index(drop=True)
        df_publico = df.iloc[44:70, 2:10].reset_index(drop=True)
        df_privado = df.iloc[81:107, 2:10].reset_index(drop=True)

        df_resultado = pd.DataFrame({
            "año": int(anio),
            "id_provincia": df_provincias,
            "c_planta_inicial_publico": df_publico.iloc[:, 0],
            "c_planta_primaria_publico": df_publico.iloc[:, 1],
            "c_planta_secundaria_publico": df_publico.iloc[:, 2],
            "c_planta_sup_nouniv_publico": df_publico.iloc[:, 3],
            "c_fuera_inicial_publico": df_publico.iloc[:, 4],
            "c_fuera_primaria_publico": df_publico.iloc[:, 5],
            "c_fuera_secundaria_publico": df_publico.iloc[:, 6],
            "c_fuera_sup_nouniv_publico": df_publico.iloc[:, 7],
            "c_planta_inicial_privado": df_privado.iloc[:, 0],
            "c_planta_primaria_privado": df_privado.iloc[:, 1],
            "c_planta_secundaria_privado": df_privado.iloc[:, 2],
            "c_planta_sup_nouniv_privado": df_privado.iloc[:, 3],
            "c_fuera_inicial_privado": df_privado.iloc[:, 4],
            "c_fuera_primaria_privado": df_privado.iloc[:, 5],
            "c_fuera_secundaria_privado": df_privado.iloc[:, 6],
            "c_fuera_sup_nouniv_privado": df_privado.iloc[:, 7],
        })

        df_resultado["prov_normalizada"] = df_resultado["id_provincia"].apply(normalize_name)
        df_resultado["id_provincia"] = df_resultado["prov_normalizada"].map(codigo_provincias_normalizado)
        df_resultado = df_resultado[df_resultado["id_provincia"].notna()].drop(columns=["prov_normalizada"])

        for col in df_resultado.columns:
            if col not in ["año", "id_provincia"]:
                df_resultado[col] = pd.to_numeric(df_resultado[col], errors="coerce").astype("Int64")

        df_resultado["id_provincia"] = df_resultado["id_provincia"].astype("Int64")

        print("\n✅ DataFrame de cargos generado:")
        print(df_resultado)

        return df_resultado
