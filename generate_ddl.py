import psycopg2
from database.registry import get_inspector
from ddl.generator import generate_mssql_create_table

# 1. Подключаемся к PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="migrator",  # ← замените на ваши креды
    password="secure_password123",
    dbname="migration_source"
)

try:
    # 2. Получаем инспектор
    inspector = get_inspector("postgresql")

    # 3. Получаем список таблиц
    tables = inspector.get_tables(conn)
    print("Таблицы:", tables)

    # 4. Сохраняем DDL всех таблиц в файл
    with open("all_tables_ddl.sql", "w", encoding="utf-8") as f:
        for table in tables:
            columns = inspector.get_columns(conn, table)
            ddl = generate_mssql_create_table(table, columns)
            f.write(f"-- Таблица: {table}\n{ddl}\n\n")
            print(f"✅ Добавлена таблица {table}")

    print("\n🎉 Все DDL сохранены в all_tables_ddl.sql")

finally:
    conn.close()