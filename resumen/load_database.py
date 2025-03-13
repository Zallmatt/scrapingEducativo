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
            except pymysql.connector.Error as err:
                print(f"Error al conectar a la base de datos: {err}")
                return None
        return self
    
    def cerrar_conexion(self):
        """Cerrar la conexión a la base de datos."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        self.conn = None
        self.cursor = None

    def load_data_ue(self, df):
        """Cargar el DataFrame a la base de datos, reemplazando los datos existentes."""
        try:
            # Crear el motor de conexión a la base de datos
            engine = create_engine(f"mysql+pymysql://{self.user}:{self.password}@{self.host}:3306/{self.database}")
            with engine.connect() as connection:
                # Sobrescribir los datos en la tabla
                df.to_sql(name="educacion_comun_resumen_ue", con=connection, if_exists='replace', index=False)
            print("Datos cargados exitosamente en la base de datos.")
        except Exception as e:
            print(f"Error al cargar datos a la base de datos: {e}")

    def load_data_us(self, df):
        """Cargar el DataFrame a la base de datos, reemplazando los datos existentes."""
        try:
            # Crear el motor de conexión a la base de datos
            engine = create_engine(f"mysql+pymysql://{self.user}:{self.password}@{self.host}:3306/{self.database}")
            with engine.connect() as connection:
                # Sobrescribir los datos en la tabla
                df.to_sql(name="educacion_comun_resumen_us", con=connection, if_exists='replace', index=False)
            print("Datos cargados exitosamente en la base de datos.")
        except Exception as e:
            print(f"Error al cargar datos a la base de datos: {e}")

    def load_data_alumnos(self, df):
        """Cargar el DataFrame a la base de datos, reemplazando los datos existentes."""
        try:
            # Crear el motor de conexión a la base de datos
            engine = create_engine(f"mysql+pymysql://{self.user}:{self.password}@{self.host}:3306/{self.database}")
            with engine.connect() as connection:
                # Sobrescribir los datos en la tabla
                df.to_sql(name="educacion_comun_alumnos", con=connection, if_exists='replace', index=False)
            print("Datos cargados exitosamente en la base de datos.")
        except Exception as e:
            print(f"Error al cargar datos a la base de datos: {e}")

    def load_data_cargos(self, df):
        """Cargar el DataFrame a la base de datos, reemplazando los datos existentes."""
        try:
            # Crear el motor de conexión a la base de datos
            engine = create_engine(f"mysql+pymysql://{self.user}:{self.password}@{self.host}:3306/{self.database}")
            with engine.connect() as connection:
                # Sobrescribir los datos en la tabla
                df.to_sql(name="educacion_comun_cargos", con=connection, if_exists='replace', index=False)
            print("Datos cargados exitosamente en la base de datos.")
        except Exception as e:
            print(f"Error al cargar datos a la base de datos: {e}")

    def load_data_horas(self, df):
        """Cargar el DataFrame a la base de datos, reemplazando los datos existentes."""
        try:
            # Crear el motor de conexión a la base de datos
            engine = create_engine(f"mysql+pymysql://{self.user}:{self.password}@{self.host}:3306/{self.database}")
            with engine.connect() as connection:
                # Sobrescribir los datos en la tabla
                df.to_sql(name="educacion_comun_horas", con=connection, if_exists='replace', index=False)
            print("Datos cargados exitosamente en la base de datos.")
        except Exception as e:
            print(f"Error al cargar datos a la base de datos: {e}")

    def load_data_inicial_asistencia(self, df):
        """Cargar el DataFrame a la base de datos, reemplazando los datos existentes."""
        try:
            # Crear el motor de conexión a la base de datos
            engine = create_engine(f"mysql+pymysql://{self.user}:{self.password}@{self.host}:3306/{self.database}")
            with engine.connect() as connection:
                # Sobrescribir los datos en la tabla
                df.to_sql(name="nivel_inicial_asistencia", con=connection, if_exists='replace', index=False)
            print("Datos cargados exitosamente en la base de datos.")
        except Exception as e:
            print(f"Error al cargar datos a la base de datos: {e}")

    def load_data_primario_repitentes(self, df):
        """Cargar el DataFrame a la base de datos, reemplazando los datos existentes."""
        try:
            # Crear el motor de conexión a la base de datos
            engine = create_engine(f"mysql+pymysql://{self.user}:{self.password}@{self.host}:3306/{self.database}")
            with engine.connect() as connection:
                # Sobrescribir los datos en la tabla
                df.to_sql(name="nivel_primario_repitentes", con=connection, if_exists='replace', index=False)
            print("Datos cargados exitosamente en la base de datos.")
        except Exception as e:
            print(f"Error al cargar datos a la base de datos: {e}")

    def load_data_secundario_repitentes(self, df):
        """Cargar el DataFrame a la base de datos, reemplazando los datos existentes."""
        try:
            # Crear el motor de conexión a la base de datos
            engine = create_engine(f"mysql+pymysql://{self.user}:{self.password}@{self.host}:3306/{self.database}")
            with engine.connect() as connection:
                # Sobrescribir los datos en la tabla
                df.to_sql(name="nivel_secundario_repitentes", con=connection, if_exists='replace', index=False)
            print("Datos cargados exitosamente en la base de datos.")
        except Exception as e:
            print(f"Error al cargar datos a la base de datos: {e}")