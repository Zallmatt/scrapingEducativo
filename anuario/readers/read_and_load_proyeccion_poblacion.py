import os
import pandas as pd
import unicodedata
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pymysql

class ProyeccionPoblacional:
    def __init__(self):
        self.host, self.user, self.password, self.database = self._cargar_variables_entorno()

    def _cargar_variables_entorno(self):
        """Carga las variables de entorno necesarias para la conexión."""
        load_dotenv()
        host = os.getenv('HOST_DBB')
        user = os.getenv('USER_DBB')
        password = os.getenv('PASSWORD_DBB')
        db = os.getenv('NAME_DBB')

        if not all([host, user, password, db]):
            raise ValueError("❌ Faltan variables de entorno necesarias para la conexión.")
        return host, user, password, db

    def _remover_tildes(self, texto):
        """Remueve tildes y normaliza texto."""
        if isinstance(texto, str):
            return ''.join(
                c for c in unicodedata.normalize('NFKD', texto)
                if not unicodedata.combining(c)
            )
        return texto

    def _load_route_excel(self, filename):
        """Devuelve ruta absoluta del archivo en carpeta 'files'."""
        return os.path.join(os.path.dirname(__file__), "files", filename)

    def load_data_to_db(self, df):
        """Sube el DataFrame a la base de datos."""
        try:
            engine = create_engine(f"mysql+pymysql://{self.user}:{self.password}@{self.host}:3306/{self.database}")
            with engine.connect() as connection:
                df.to_sql(name="proyeccion_poblacion", con=connection, if_exists='replace', index=False)
            print("✅ Datos cargados exitosamente en la tabla `proyeccion_poblacion`.")
        except Exception as e:
            print(f"❌ Error al cargar datos: {e}")

    def create_df(self, excel_name):
        """Lee el Excel y retorna el DataFrame normalizado."""
        path = self._load_route_excel(excel_name)
        df = pd.read_excel(path, sheet_name=0)

        # Normalizar columnas
        df.columns = [self._remover_tildes(col).lower().strip() for col in df.columns]

        # Renombrar columnas si fuera necesario
        expected_columns = {
            'ano': 'año',
            'id_provincia_indec': 'id_provincia_indec',
            'provincia': 'provincia',
            'poblacion': 'poblacion'
        }
        df = df.rename(columns=expected_columns)

        # Normalizar provincias
        if 'provincia' in df.columns:
            df['provincia'] = df['provincia'].apply(self._remover_tildes)

        print("📊 DataFrame generado:")
        print(df.head())

        return df
