from typing import List, Dict
from database.type_mapping import map_pg_type_to_mssql

def generate_mssql_create_table(table_name: str, columns: List[Dict]) -> str:
    col_defs = []
    pk_cols = []

    for col in columns:
        mssql_type = map_pg_type_to_mssql(col["data_type"])
        nullable = "NULL" if col["is_nullable"] else "NOT NULL"
        col_def = f"[{col['name']}] {mssql_type} {nullable}"
        col_defs.append(col_def)

        if col["is_primary_key"]:
            pk_cols.append(f"[{col['name']}]")

    # Собираем DDL
    ddl = f"CREATE TABLE [{table_name}] (\n  " + ",\n  ".join(col_defs)

    if pk_cols:
        ddl += f",\n  CONSTRAINT [PK_{table_name}] PRIMARY KEY ({', '.join(pk_cols)})"

    ddl += "\n);"
    return ddl