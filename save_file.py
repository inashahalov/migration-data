with open("all_tables_ddl.sql", "w", encoding="utf-8") as f:
    for table in tables:
        columns = inspector.get_columns(conn, table)
        ddl = generate_mssql_create_table(table, columns)
        f.write(f"-- Таблица: {table}\n{ddl}\n\n")
        print(f"Добавлена таблица {table}")

print("Все DDL сохранены в all_tables_ddl.sql")