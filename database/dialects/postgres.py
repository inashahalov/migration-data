from typing import List, Dict, Any

from ..inspector import DatabaseInspector


class PostgresInspector(DatabaseInspector):
    @classmethod
    def dialect_name(cls) -> str:
        return "postgresql"

    def get_tables(self, conn) -> List[str]:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT tablename
                FROM pg_tables
                WHERE schemaname = 'public'
            """)
            return [row[0] for row in cur.fetchall()]

    def get_columns(self, conn, table: str) -> List[Dict[str, Any]]:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    a.attname AS name,
                    pg_catalog.format_type(a.atttypid, a.atttypmod) AS data_type,
                    NOT a.attnotnull AS is_nullable,
                    i.indisprimary AS is_primary_key
                FROM pg_attribute a
                JOIN pg_class c ON a.attrelid = c.oid
                JOIN pg_namespace n ON c.relnamespace = n.oid
                LEFT JOIN pg_index i ON a.attnum = ANY(i.indkey) AND c.oid = i.indrelid AND i.indisprimary
                WHERE c.relname = %s
                  AND n.nspname = 'public'
                  AND a.attnum > 0
                  AND NOT a.attisdropped
                ORDER BY a.attnum;
            """, (table,))
            return [
                {
                    "name": row[0],
                    "data_type": row[1],
                    "is_nullable": row[2],
                    "is_primary_key": bool(row[3])
                }
                for row in cur.fetchall()
            ]

    def get_table_size(self, conn, table: str) -> int:
        with conn.cursor() as cur:
            cur.execute("SELECT pg_total_relation_size(%s)", (table,))
            return cur.fetchone()[0]

    def get_table_dependencies(self, conn) -> Dict[str, List[str]]:
        """
        Возвращает словарь: {таблица: [от каких таблиц зависит]}
        Например: {"orders": ["users", "products"]}
        """
        cur = conn.cursor()
        cur.execute("""
            SELECT
                tc.table_name,
                ccu.table_name AS foreign_table_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
              ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage ccu
              ON ccu.constraint_name = tc.constraint_name
            WHERE tc.constraint_type = 'FOREIGN KEY'
        """)
        deps = {}
        for child, parent in cur.fetchall():
            deps.setdefault(child, []).append(parent)
        return deps