import psycopg2
from database.registry import get_inspector
from ddl.generator import generate_mssql_create_table

# 1. Подключаемся к PostgreSQL (в реальности — через Airflow Hook)
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="migrator",
    password="secure_password123",
    dbname="migration_source"
)

try:
    # 2. Получаем инспектор для PostgreSQL
    inspector = get_inspector("postgresql")

    # 3. Получаем список таблиц
    tables = inspector.get_tables(conn)
    print("Таблицы:", tables)

    # 4. Для первой таблицы генерируем DDL для MS SQL
    if tables:
        table = tables[0]
        columns = inspector.get_columns(conn, table)
        ddl = generate_mssql_create_table(table, columns)
        print(f"\nDDL для таблицы '{table}':\n{ddl}")

        # 5. Показываем размер
        size = inspector.get_table_size(conn, table)
        print(f"\nРазмер таблицы: {size / 1024:.2f} КБ")

finally:
    conn.close()

