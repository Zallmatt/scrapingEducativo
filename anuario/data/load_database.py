from sqlalchemy import create_engine
import pymysql
import pandas as pd

class loadDatabase:

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None

    def connect_db(self):
        """Conectar a la base de datos MySQL si no está ya conectada."""
        if not self.conn or not self.cursor:
            try:
                self.conn = pymysql.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database
                )
                self.cursor = self.conn.cursor()
            except pymysql.MySQLError as err:
                print(f"❌ Error al conectar a la base de datos: {err}")
        return self

    def cerrar_conexion(self):
        """Cerrar la conexión a la base de datos."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        self.conn = None
        self.cursor = None

    def _upload_df_to_table(self, df: pd.DataFrame, table_name: str):
        """Sube un DataFrame a una tabla, reemplazando los datos existentes."""
        try:
            engine = create_engine(f"mysql+pymysql://{self.user}:{self.password}@{self.host}:3306/{self.database}")
            with engine.connect() as connection:
                df.to_sql(name=table_name, con=connection, if_exists='replace', index=False)
            print(f"✅ Datos cargados correctamente en la tabla `{table_name}`.")
        except Exception as e:
            print(f"❌ Error al cargar datos a `{table_name}`: {e}")

    # Métodos públicos para cada tabla
    def load_data_ue(self, df): self._upload_df_to_table(df, "educacion_comun_resumen_ue")
    def load_data_us(self, df): self._upload_df_to_table(df, "educacion_comun_resumen_us")
    def load_data_alumnos(self, df): self._upload_df_to_table(df, "educacion_comun_alumnos")
    def load_data_cargos(self, df): self._upload_df_to_table(df, "educacion_comun_cargos")
    def load_data_horas(self, df): self._upload_df_to_table(df, "educacion_comun_horas")
    def load_data_inicial_asistencia(self, df): self._upload_df_to_table(df, "nivel_inicial_asistencia")
    def load_data_primario_repitentes(self, df): self._upload_df_to_table(df, "nivel_primario_repitentes")
    def load_data_secundario_repitentes(self, df): self._upload_df_to_table(df, "nivel_secundario_repitentes")
