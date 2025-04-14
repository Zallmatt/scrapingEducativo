import os
import pandas as pd
from utils.normalization import normalize_name
from utils.mappings import codigo_provincias

class ReadDataExcelTasaSobreedad:
    def load_route_excel(self, name):
        file_path = os.path.join(os.path.dirname(__file__), "../files", name)
        print(f"📄 Cargando archivo: {file_path}")
        return file_path

    def create_df_sobreedad(self):
        name = "Tasa de Sobreedad 2023-2012.xlsx"
        file_path = self.load_route_excel(name)

        xls = pd.ExcelFile(file_path)
        hojas = [h for h in xls.sheet_names if h.isdigit()]
        print(f"Hojas encontradas: {hojas}")

        all_dfs = []

        for hoja in hojas:
            print(f"📑 Procesando hoja: {hoja}")
            try:
                df = pd.read_excel(file_path, sheet_name=hoja, skiprows=11, header=None)
                df = df[df[0].notna()]
                df["nombre_provincia"] = df[0]

                def preprocess_nombre(nombre):
                    nombre = str(nombre).strip()
                    if nombre.lower() == "total país":
                        return "Nacion"
                    return normalize_name(nombre)

                df["prov_normalizada"] = df[0].apply(preprocess_nombre)
                df = df[~df["prov_normalizada"].isin(["Conurbano", "Resto de Bs As"])]

                df_clean = pd.DataFrame()
                df_clean["id_provincia"] = df["prov_normalizada"].map(codigo_provincias).astype("Int64")
                df_clean = df_clean[df_clean["id_provincia"].notna()]

                df_clean["nombre_provincia"] = df["nombre_provincia"]
                df_clean["Año"] = int(hoja)

                df_clean["Sobre_Estructura_Educativa"] = df[1]
                df_clean["Sobre_Total_Primaria"] = df[2]
                df_clean["Sobre_Año1_P"] = df[3]
                df_clean["Sobre_Año2_P"] = df[4]
                df_clean["Sobre_Año3_P"] = df[5]
                df_clean["Sobre_Año4_P"] = df[6]
                df_clean["Sobre_Año5_P"] = df[7]
                df_clean["Sobre_Año6_P"] = df[8]
                df_clean["Sobre_Año7_P"] = df[9]

                df_clean["Sobre_Total_Secundaria"] = df[10]
                df_clean["Sobre_Año7_S"] = df[11]
                df_clean["Sobre_Año8_S"] = df[12]
                df_clean["Sobre_Año9_S"] = df[13]
                df_clean["Sobre_Año10_S"] = df[14]
                df_clean["Sobre_Año11_S"] = df[15]
                df_clean["Sobre_Año12_S"] = df[16]

                df_clean = df_clean.where(pd.notna(df_clean), None)
                all_dfs.append(df_clean)

            except Exception as e:
                print(f"⚠️ Error procesando hoja {hoja}: {e}")
                continue

        if not all_dfs:
            raise ValueError("No se pudieron procesar hojas válidas.")

        df_final = pd.concat(all_dfs, ignore_index=True)
        print("✅ DataFrame final generado correctamente:")
        print(df_final.head())

        print("\n📊 Resumen por año (provincias cargadas):")
        print(df_final.groupby("Año")["id_provincia"].count())

        return df_final
