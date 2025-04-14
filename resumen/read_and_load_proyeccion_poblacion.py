import os
import pandas as pd
from dotenv import load_dotenv
import unicodedata
from sqlalchemy import create_engine
import pymysql

class ProyeccionPoblacional:
    def __init__(self):
        self.host, self.user, self.password, self.database = self.cargar_variables_entorno()

    def cargar_variables_entorno(self):
        """Carga las variables de entorno necesarias para la conexión."""
        load_dotenv()

        host_dbb = os.getenv('HOST_DBB')
        user_dbb = os.getenv('USER_DBB')
        pass_dbb = os.getenv('PASSWORD_DBB')
        dbb_datalake = os.getenv('NAME_DBB')

        if not all([host_dbb, user_dbb, pass_dbb, dbb_datalake]):
            raise ValueError("Faltan variables de entorno necesarias para la conexión.")

        return host_dbb, user_dbb, pass_dbb, dbb_datalake
    
    def remover_tildes(self, texto):
        if isinstance(texto, str):
            texto_normalizado = unicodedata.normalize('NFKD', texto)
            return ''.join(c for c in texto_normalizado if not unicodedata.combining(c))
        return texto
    
    def load_route_excel(self, name):
        """Obtiene la ruta absoluta del archivo en la carpeta 'files'"""
        file_path = os.path.join(os.path.dirname(__file__), "files", name)
        return file_path

    def load_data_proyeccion_poblacion(self, df):
        """Cargar el DataFrame a la base de datos, reemplazando los datos existentes."""
        try:
            engine = create_engine(f"mysql+pymysql://{self.user}:{self.password}@{self.host}:3306/{self.database}")
            with engine.connect() as connection:
                df.to_sql(name="proyeccion_poblacion", con=connection, if_exists='replace', index=False)
            print("✅ Datos cargados exitosamente en la base de datos.")
        except Exception as e:
            print(f"❌ Error al cargar datos a la base de datos: {e}")

    def create_df_alumnos(self, name):
        file_path = self.load_route_excel(name)
        df = pd.read_excel(file_path, sheet_name=0)
        df.columns = [self.remover_tildes(col).lower().strip() for col in df.columns]
        df = df.rename(columns={
            'ano': 'año',
            'id_provincia_indec': 'id_provincia_indec',
            'provincia': 'provincia',
            'poblacion': 'poblacion'
        })
        df['provincia'] = df['provincia'].apply(self.remover_tildes)
        return df
    
def main():
    name = "Proyeccion_Poblacion_Anual.xlsx"
    proy = ProyeccionPoblacional()
    df = proy.create_df_alumnos(name)
    proy.load_data_proyeccion_poblacion(df)

if __name__ == "__main__":
    main()
