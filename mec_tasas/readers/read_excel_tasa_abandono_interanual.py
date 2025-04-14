import os
import pandas as pd
from utils.normalization import normalize_name
from utils.mappings import codigo_provincias

class ReadDataExcelTasaAbandonoInteranual:
    def load_route_excel(self, name):
        """Obtiene la ruta absoluta del archivo en la carpeta 'files'"""
        file_path = os.path.join(os.path.dirname(__file__), "../files", name)
        print(f"📄 Cargando archivo: {file_path}")
        return file_path

    def create_df_abandono_interanual(self):
        name = "Tasa de Abandono Interanual 2023-2012 según división político-territorial.xlsx"
        file_path = self.load_route_excel(name)

        xls = pd.ExcelFile(file_path)
        hojas = xls.sheet_names
        print(f"Hojas encontradas: {hojas}")

        all_dfs = []

        for hoja in hojas:
            print(f"📑 Procesando hoja: {hoja}")
            try:
                df = pd.read_excel(file_path, sheet_name=hoja, header=10)
                df.columns = [' '.join(str(col).split()) for col in df.columns]

                # Eliminar filas vacías o basura
                df = df[df["División Político Territorial"].notna()]
                df = df[~df["División Político Territorial"].astype(str).str.match(
                    r"^(Tasa|Fuente|Ley|Estructura|Educacion|Realizacion|Realizado)", case=False
                )]

                df["nombre_provincia"] = df["División Político Territorial"]

                def preprocess_nombre(nombre):
                    nombre = str(nombre).strip()
                    if nombre.lower() == "total país":
                        return "Nacion"
                    return normalize_name(nombre)

                df["prov_normalizada"] = df["nombre_provincia"].apply(preprocess_nombre)
                df = df[~df["prov_normalizada"].isin(["Conurbano", "Resto de Bs As"])]

                df_clean = pd.DataFrame()
                df_clean["id_provincia"] = df["prov_normalizada"].map(codigo_provincias).astype("Int64")
                df_clean = df_clean[df_clean["id_provincia"].notna()]
                df_clean["nombre_provincia"] = df["nombre_provincia"]

                try:
                    anio = int(hoja.split("-")[1])
                except:
                    anio = None
                df_clean["Año"] = anio

                # Cargar columnas de datos
                df_clean["Ab_Estructura_Educativa"] = df["Estructura Educativa"]
                df_clean["Ab_Total_Primaria"] = df["Primaria"]
                df_clean["Ab_Año1_P"] = df["Unnamed: 3"]
                df_clean["Ab_Año2_P"] = df["Unnamed: 4"]
                df_clean["Ab_Año3_P"] = df["Unnamed: 5"]
                df_clean["Ab_Año4_P"] = df["Unnamed: 6"]
                df_clean["Ab_Año5_P"] = df["Unnamed: 7"]
                df_clean["Ab_Año6_P"] = df["Unnamed: 8"]
                df_clean["Ab_Año7_P"] = df["Unnamed: 9"]
                df_clean["Ab_Total_Secundaria"] = df["Secundaria"]
                df_clean["Ab_Año7_S"] = df["Unnamed: 11"]
                df_clean["Ab_Año8_S"] = df["Unnamed: 12"]
                df_clean["Ab_Año9_S"] = df["Unnamed: 13"]
                df_clean["Ab_Año10_S"] = df["Unnamed: 14"]
                df_clean["Ab_Año11_S"] = df["Unnamed: 15"]
                df_clean["Ab_Año12_S"] = df["Unnamed: 16"]

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
