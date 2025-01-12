FROM python:3.12.0-slim

# Establece el directorio de trabajo
WORKDIR /usr/src/app

# Copia el archivo de dependencias
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación
COPY app .

CMD ["tail", "-f", "/dev/null"]
