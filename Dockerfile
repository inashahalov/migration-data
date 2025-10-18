# Dockerfile
FROM apache/airflow:2.9.3-python3.11

# Копируем файл зависимостей
COPY requirements.txt /requirements.txt

# Устанавливаем зависимости
USER root
RUN pip install --no-cache-dir -r /requirements.txt
USER airflow