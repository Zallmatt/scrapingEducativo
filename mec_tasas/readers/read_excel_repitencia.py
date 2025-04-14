import os
import pandas as pd
from utils.normalization import normalize_name
from utils.mappings import codigo_provincias

class ReadDataExcelTasaRepitencia:
    def load_route_excel(self, name):
        file_path = os.path.join(os.path.dirname(__file__), "../files", name)
        print(f"📄 Cargando archivo: {file_path}")
        return file_path

    def create_df_repitencia(self):
        name = "Tasa de Repitencia 2022-2012 según división político-territorial.xlsx"
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

                df_clean["Rep_Estructura_Educativa"] = df[1]
                
                # Primaria
                df_clean["Rep_Total_Primaria"] = pd.to_numeric(df[2], errors='coerce')
                df_clean["Rep_Año1_P"] = pd.to_numeric(df[3], errors='coerce')
                df_clean["Rep_Año2_P"] = pd.to_numeric(df[4], errors='coerce')
                df_clean["Rep_Año3_P"] = pd.to_numeric(df[5], errors='coerce')
                df_clean["Rep_Año4_P"] = pd.to_numeric(df[6], errors='coerce')
                df_clean["Rep_Año5_P"] = pd.to_numeric(df[7], errors='coerce')
                df_clean["Rep_Año6_P"] = pd.to_numeric(df[8], errors='coerce')
                df_clean["Rep_Año7_P"] = pd.to_numeric(df[9], errors='coerce')

                # Secundaria
                df_clean["Rep_Total_Secundaria"] = pd.to_numeric(df[10], errors='coerce')
                df_clean["Rep_Año7_S"] = pd.to_numeric(df[11], errors='coerce')
                df_clean["Rep_Año8_S"] = pd.to_numeric(df[12], errors='coerce')
                df_clean["Rep_Año9_S"] = pd.to_numeric(df[13], errors='coerce')
                df_clean["Rep_Año10_S"] = pd.to_numeric(df[14], errors='coerce')
                df_clean["Rep_Año11_S"] = pd.to_numeric(df[15], errors='coerce')
                df_clean["Rep_Año12_S"] = pd.to_numeric(df[16], errors='coerce')


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
