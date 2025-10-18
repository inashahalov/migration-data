from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook
from database.registry import get_inspector
from ddl.generator import generate_mssql_create_table
from utils.dag_utils import topological_sort


def analyze_and_generate_ddl(**context):
    # 1. Получаем подключения
    pg_hook = PostgresHook("pg_source")
    pg_conn = pg_hook.get_conn()

    try:
        inspector = get_inspector("postgresql")

        # 2. Получаем таблицы и зависимости
        tables = inspector.get_tables(pg_conn)
        dependencies = inspector.get_table_dependencies(pg_conn)

        # 3. Определяем порядок миграции
        migration_order = topological_sort(tables, dependencies)
        context["task_instance"].xcom_push(key="migration_order", value=migration_order)

        # 4. Генерируем DDL
        ddls = {}
        for table in migration_order:
            columns = inspector.get_columns(pg_conn, table)
            ddls[table] = generate_mssql_create_table(table, columns)

        context["task_instance"].xcom_push(key="ddls", value=ddls)
        print(f"✅ Сгенерирован DDL для {len(ddls)} таблиц. Порядок: {migration_order}")

    finally:
        pg_conn.close()


def apply_ddl_to_mssql(**context):
    ddls = context["task_instance"].xcom_pull(task_ids="analyze_schema", key="ddls")
    order = context["task_instance"].xcom_pull(task_ids="analyze_schema", key="migration_order")

    mssql_hook = MsSqlHook("mssql_target")

    for table in order:
        ddl = ddls[table]
        print(f"Применяю DDL для {table}...")
        mssql_hook.run(ddl)


with DAG(
        "pg_to_mssql_schema_migration",
        start_date=datetime(2025, 1, 1),
        schedule="@once",
        catchup=False,
        tags=["migration", "ddl"]
) as dag:
    analyze_schema = PythonOperator(
        task_id="analyze_schema",
        python_callable=analyze_and_generate_ddl
    )

    create_tables = PythonOperator(
        task_id="create_tables_in_mssql",
        python_callable=apply_ddl_to_mssql
    )

    analyze_schema >> create_tables