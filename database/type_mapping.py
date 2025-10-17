PG_TO_MSSQL = {
    "serial": "INT IDENTITY(1,1)",
    "bigserial": "BIGINT IDENTITY(1,1)",
    "integer": "INT",
    "bigint": "BIGINT",
    "boolean": "BIT",
    "text": "NVARCHAR(MAX)",
    "character varying": "NVARCHAR",  # обрабатываем длину отдельно
    "uuid": "UNIQUEIDENTIFIER",
    "timestamp without time zone": "DATETIME2",
    "timestamp with time zone": "DATETIMEOFFSET",
    "date": "DATE",
    "jsonb": "NVARCHAR(MAX)",
}


def map_pg_type_to_mssql(pg_type: str) -> str:
    """
    Преобразует тип из PostgreSQL в MS SQL.
    Пример: "character varying(255)" → "NVARCHAR(255)"
    """
    pg_type = pg_type.lower().strip()

    # Обработка типов с длиной: VARCHAR(255)
    if pg_type.startswith("character varying"):
        if "(" in pg_type:
            length = pg_type.split("(")[1].rstrip(")")
            return f"NVARCHAR({length})"
        return "NVARCHAR(255)"  # default

    # Простой маппинг
    base_type = pg_type.split("(")[0].rstrip()
    return PG_TO_MSSQL.get(base_type, "NVARCHAR(MAX)")