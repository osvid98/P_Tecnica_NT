"""
    Este código se utiliza para gestionar la inserción del dataset (archivo CSV) en la base de datos MySQL.
    Se emplea MySQL debido a que el dataset proporcionado muestra claramente una relación de muchos a muchos en los datos.
    Por lo tanto, es más conveniente emplear una base de datos relacional que permita gestionar y mantener de manera eficiente
    estas relaciones entre los registros.

    Se utiliza Pandas para leer el archivo CSV, lo que facilita la manipulación y extracción de datos desde un archivo plano.
    La conexión con la base de datos MySQL se establece utilizando SQLAlchemy.
"""

import pandas as pd
from DatabaseHandler import DatabaseHandler

# Leer archivo CSV
data = pd.read_csv('data_prueba_tecnica.csv')

# Crear instancia del manejador de base de datos y conectar a la BD
db_handler = DatabaseHandler("mysql", "root", "123", "mydb")
engine = db_handler.engine

# Insertar datos en la tabla, se crea si no existe
table_name = 'Cargo'
try:
    data.to_sql(table_name, con=engine, if_exists='replace', index=False)
    print(f"Datos insertados en la tabla {table_name}.")
except exc.SQLAlchemyError as e:
    print(f"Error al insertar datos en la tabla {table_name}: {e}")
finally:
    db_handler.close()  # Asegurarse de cerrar la conexión después de usarla.
