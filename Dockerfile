# Imagen base con Python
FROM python:3.10-slim

# Establecer directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar todos los archivos del proyecto al contenedor
COPY . /app

# Instalar dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Crear carpeta para cargas (por si no existe)
RUN mkdir -p uploads

# Exponer el puerto de Flask
EXPOSE 5000

# Definir variable de entorno por defecto
ENV APP_ENV=dev

# Ejecutar Flask al iniciar el contenedor
CMD ["python", "main.py"]
