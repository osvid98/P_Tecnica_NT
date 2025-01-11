"""
    Este script realiza la transformación y ajuste de datos extraídos desde un archivo CSV.
    Las transformaciones incluyen la generación de nuevos IDs, la limitación de nombres y cantidades,
    la normalización de estados y fechas, y el manejo de valores nulos.
    Finalmente, los datos ajustados se exportan a un nuevo archivo CSV.

    El formato de restricciones que se llevo a cabo para la tranformacion de datos fue el siguiente:
    - id varchar(24) NOT NULL
    - company_name varchar(130) NULL
    - company_id varchar(24) NOT NULL
    - amount decimal(16,2) NOT NULL
    - status varchar(30) NOT NULL
    - created_at timestamp NOT NULL
    - updated_at timestamp NULL

    Estas transformaciones fueron varios retos ya que requerieron un enfoque cuidadoso en la validación
    y manipulación de datos, combinando lógica flexible con restricciones claras para asegurar que la
    transformación fuera efectiva y segura (sin eliminar registros).
"""


import pandas as pd
import random, string
from datetime import datetime

# Leer el archivo CSV
df = pd.read_csv('datos_extraccion.csv')
print("Transformando... Espere un momento.")


# Función para generar un nuevo ID de exactamente 24 caracteres
def generar_nuevo_id():
    random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=14))
    return f"recovered_{random_part}"  # 'recovered_' tiene 10 caracteres, el total será 24

# Ajustar los IDs para cumplir con el formato deseado
def ajustar_id(id_value):
    if pd.isnull(id_value):  # Si el ID es nulo, generar un nuevo ID
        return generar_nuevo_id()

    id_value = str(id_value)

    if len(id_value) < 24:  # Si es más corto, rellenar con caracteres aleatorios
        faltantes = 24 - len(id_value)
        id_value += ''.join(random.choices(string.ascii_letters + string.digits, k=faltantes))
    elif len(id_value) > 24:  # Si es más largo, recortar a los primeros 24 caracteres
        id_value = id_value[:24]

    return id_value

# Ajustar los nombres de la compañía para cumplir con el formato deseado
def ajustar_company_name(name):
    if pd.isnull(name):  # Si el nombre es nulo, mantenerlo como está
        return name
    name = str(name)
    return name[:120] if len(name) > 120 else name  # Recortar a 120 caracteres si excede

# Ajustar las cantidades para cumplir con el formato deseado
def ajustar_amount(amount):
    if pd.isnull(amount):  # Verificar si es nulo
        return 0.00

    amount = float(amount)

    # Limitar a 16 dígitos y 2 decimales
    amount = round(amount, 2)
    amount_str = f"{amount:.2f}"  # Formatear con 2 decimales

    if len(amount_str.replace('.', '').replace('-', '')) > 16:  # Excluir punto y signo negativo
        return 0.00

    return amount

# Ajustar el estado para cumplir con el formato deseado
def ajustar_status(status):
    if pd.isnull(status):  # Si el valor es nulo
        return "Indeterminado"

    status = str(status)
    return status[:30]  # Si es más largo, recortar a 30 caracteres

# Ajustar las fechas de creación para cumplir con el formato deseado
def ajustar_created_at(created_at):
    if pd.isnull(created_at):  # Si es nulo, asignar un valor por defecto
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        timestamp = pd.to_datetime(created_at)
        return timestamp.strftime('%Y-%m-%d %H:%M:%S')  # Asegurar formato estándar
    except (ValueError, TypeError):
        # Si falla, asignar un valor por defecto
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Ajustar las fechas de pago para cumplir con el formato deseado
def ajustar_paid_at(paid_at):
    try:
        timestamp = pd.to_datetime(paid_at)
        return timestamp.strftime('%Y-%m-%d %H:%M:%S')  # Asegurar formato estándar
    except (ValueError, TypeError):
        # Si falla, asignar un valor por defecto
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


# Aplicar la transformación a las columnas
df['id'] = df['id'].apply(ajustar_id)
df['name'] = df['name'].apply(ajustar_company_name)
df['company_id'] = df['company_id'].apply(ajustar_id)
df['amount'] = df['amount'].apply(ajustar_amount)
df['status'] = df['status'].apply(ajustar_status)
df['created_at'] = df['created_at'].apply(ajustar_created_at)
df['paid_at'] = df['paid_at'].apply(ajustar_paid_at)

# Cambiar el nombre de la columna 'paid_at' por 'updated_at'
df.rename(columns={'paid_at': 'updated_at'}, inplace=True)

# Exportar los datos a un CSV con las transformaciones aplicadas
csv_output_transformed = 'datos_transformados.csv'
df.to_csv(csv_output_transformed, index=False)
print(f"Datos transformados exportados a {csv_output_transformed}.")
