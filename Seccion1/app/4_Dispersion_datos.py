"""
    Este script realiza la conexión a una base de datos MySQL y lleva a cabo la creación de tablas necesarias
    para almacenar los cargos, compañias y las relaciones entre estas. Además, se leen datos desde un archivo CSV el cual
    fue ya previamente transformado (limpiado/normalizado) y se insertan en las tablas correspondientes.

    El diagrama de la BD se puede observar en el archivo "4_Diagrama.jpg"
"""

import pandas as pd
from DatabaseHandler import DatabaseHandler

# Crear instancia del manejador de base de datos y conectar a la BD
db_handler = DatabaseHandler("mysql", "root", "123", "mydb")
engine = db_handler.engine

# Crear conexión para crear tablas
connection = engine.raw_connection()
cursor = connection.cursor()

# Función para crear tablas si no existen
def crear_tablas(cursor):
    # Crear la tabla 'charges' si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS charges (
          id VARCHAR(24) NOT NULL,
          amount DECIMAL(16,2) NOT NULL,
          status VARCHAR(30) NOT NULL,
          created_at DATETIME NOT NULL,
          updated_at DATETIME NULL,
          PRIMARY KEY (id)
        )
    ''')

    # Crear la tabla 'companies' si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS companies (
          company_id VARCHAR(24) NOT NULL,
          name VARCHAR(130) NULL,
          PRIMARY KEY (company_id)
        )
    ''')

    # Crear la tabla 'companies_has_charges' si no existe, con las relaciones necesarias
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS companies_has_charges (
          company_id VARCHAR(24) NOT NULL,
          charges_id VARCHAR(24) NOT NULL,
          PRIMARY KEY (company_id, charges_id),
          INDEX fk_companies_has_charges_charges1_idx (charges_id ASC) VISIBLE,
          INDEX fk_companies_has_charges_companies_idx (company_id ASC) VISIBLE,
          CONSTRAINT fk_companies_has_charges_companies
            FOREIGN KEY (company_id)
            REFERENCES companies (company_id)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
          CONSTRAINT fk_companies_has_charges_charges1
            FOREIGN KEY (charges_id)
            REFERENCES charges (id)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
        )
    ''')

# Función para insertar datos en la tabla 'charges'
def insertar_charges(df, engine):
    df[['id', 'amount', 'status', 'created_at', 'updated_at']].to_sql('charges', con=engine, if_exists='append', index=False)
    print("Datos insertados en la tabla 'charges'.")

# Función para insertar datos en la tabla 'companies'
def insertar_companies(df, engine):
    filtered_df = df[~df['company_id'].str.startswith(('recovered', '*'))]
    unique_companies = filtered_df[['company_id', 'name']].drop_duplicates(subset='company_id')
    unique_companies.to_sql('companies', con=engine, if_exists='append', index=False)
    print("Datos insertados en la tabla 'companies'.")
    return filtered_df

# Función para insertar datos en la tabla 'companies_has_charges'
def insertar_companies_has_charges(df, engine, filtered_df):
    charges_ids = df['id'].tolist()
    company_ids = filtered_df['company_id'].tolist()
    companies_has_charges = list(zip(company_ids, charges_ids))
    insert_data = pd.DataFrame(companies_has_charges, columns=['company_id', 'charges_id'])
    insert_data.to_sql('companies_has_charges', con=engine, if_exists='append', index=False)
    print("Datos insertados en la tabla 'companies_has_charges'.")

# Crear las tablas en la base de datos
crear_tablas(cursor)

# Leer el CSV con los datos transformados
csv_input_file = 'datos_transformados.csv'
df = pd.read_csv(csv_input_file)

# Insertar datos en cada tabla
insertar_charges(df, engine)
filtered_df = insertar_companies(df, engine)
insertar_companies_has_charges(df, engine, filtered_df)

# Confirmar los cambios en la base de datos
connection.commit()
