# 1. Usar una imagen base oficial de Python
FROM python:3.9-slim

# 2. Establecer el directorio de trabajo
WORKDIR /app

# 3. Copiar y instalar requisitos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar todo el código fuente
COPY ./src /app/src

# 5. Comando para ejecutar la API
# Usamos el comando "python -m" que nos funcionó
CMD ["python", "-m", "uvicorn", "main:app", "--app-dir", "src/api", "--host", "0.0.0.0", "--port", "8000"]