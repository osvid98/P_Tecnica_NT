"""
    Este código se utiliza para extraer datos desde una tabla en una base de datos MySQL y exportarlos a un archivo CSV.
    Se realiza una consulta sobre la tabla 'Cargo' para recuperar los registros almacenados, luego se convierte
    estos datos en un DataFrame de Pandas y, finalmente, se exportan a un archivo CSV.
"""

import pandas as pd
from DatabaseHandler import DatabaseHandler

# Crear instancia del manejador de base de datos y conectar a la BD
db_handler = DatabaseHandler("mysql", "root", "123", "mydb")
engine = db_handler.engine

# Realizar la consulta para extraer los datos
table_name = 'Cargo'
try:
    # Crear un DataFrame con los datos de la tabla Cargo
    df = pd.read_sql_query(f'SELECT * FROM {table_name}', con=engine)
    print("Datos extraídos con éxito:")
    print(df)

    # Exportar los datos a un archivo CSV
    csv_output_file = 'datos_extraccion.csv'
    df.to_csv(csv_output_file, index=False)
    print(f"Datos exportados exitosamente a {csv_output_file}.")
except Exception as e:
    print(f"Error al extraer datos de la tabla {table_name}: {e}")
