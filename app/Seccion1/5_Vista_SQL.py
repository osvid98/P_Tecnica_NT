"""
    Este script realiza la conexión a una base de datos MySQL y crea una vista llamada 'daily_transaction_summary'
    que ofrece un resumen diario de las transacciones por compañía. Además, extrae los datos de la vista utilizando
    Pandas para su visualización en consola.
"""

import pandas as pd
from DatabaseHandler import DatabaseHandler

# Crear instancia del manejador de base de datos y conectar a la BD
db_handler = DatabaseHandler("mysql", "root", "123", "mydb")
engine = db_handler.engine

# Función para crear la vista 'daily_transaction_summary'
def crear_vista_daily_transaction_summary():
    connection = engine.raw_connection()
    cursor = connection.cursor()

    create_view_sql = '''
    CREATE VIEW daily_transaction_summary AS
    SELECT
      c.name AS company_name,
      DATE(ch.created_at) AS transaction_date,
      SUM(ch.amount) AS total_amount_transacted
    FROM
      charges ch
    JOIN
      companies_has_charges chc ON ch.id = chc.charges_id
    JOIN
      companies c ON chc.company_id = c.company_id
    GROUP BY
      c.name,
      DATE(ch.created_at)
    ORDER BY
      transaction_date ASC,
      company_name ASC;
    '''

    # Ejecutar la consulta para crear la vista
    cursor.execute(create_view_sql)
    connection.commit()
    print("Vista 'daily_transaction_summary' creada exitosamente.")

# Función para visualizar la vista utilizando pandas
def visualizar_resumen_transacciones():
    query = "SELECT * FROM daily_transaction_summary"
    df = pd.read_sql_query(query, con=engine)

    # Visualizar el resultado en un print
    print("Resumen diario de transacciones por compañía:")
    print(df)

# Ejecutar las funciones
crear_vista_daily_transaction_summary()
visualizar_resumen_transacciones()
