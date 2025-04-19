import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

class DatabaseUploader:
    def __init__(self):
        self.host, self.user, self.password, self.database = self._load_env()

    def _load_env(self):
        load_dotenv()
        host = os.getenv('HOST_DBB')
        user = os.getenv('USER_DBB')
        password = os.getenv('PASSWORD_DBB')
        database = os.getenv('NAME_DBB')
        if not all([host, user, password, database]):
            raise ValueError("❌ Faltan variables de entorno.")
        return host, user, password, database

    def get_engine(self):
        return create_engine(f"mysql+pymysql://{self.user}:{self.password}@{self.host}:3306/{self.database}")

    def clean_and_replace_table(self, table_name: str, filas_a_borrar: list):
        try:
            engine = self.get_engine()
            df = pd.read_sql_table(table_name, con=engine)

            print(f"🔎 Total de filas antes: {len(df)}")
            df = df.reset_index(drop=True)
            print(df)

            # Borrar filas específicas
            df_clean = df.drop(index=filas_a_borrar)
            print(df_clean)
            print(f"🧹 Filas eliminadas: {filas_a_borrar}")
            print(f"✅ Total después de limpieza: {len(df_clean)}")

            # Reemplazar tabla completa
            with engine.connect() as connection:
                df_clean.to_sql(name=table_name, con=connection, if_exists='replace', index=False)

            print(f"✅ Tabla `{table_name}` reemplazada exitosamente.")
        except Exception as e:
            print(f"❌ Error: {e}")

# 👉 Ejecutar limpieza
if __name__ == "__main__":
    uploader = DatabaseUploader()
    uploader.clean_and_replace_table(
        table_name='educacion_comun_horas',
        filas_a_borrar=list(range(24))  # 🗑️ Elimina las primeras 24 filas
    )
