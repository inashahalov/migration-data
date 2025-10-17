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