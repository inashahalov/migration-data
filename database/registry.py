from typing import Dict, Type
from .inspector import DatabaseInspector
from .dialects.postgres import PostgresInspector

# Регистрируем все поддерживаемые СУБД
INSPECTORS: Dict[str, Type[DatabaseInspector]] = {
    "postgresql": PostgresInspector,
}

def get_inspector(dialect: str) -> DatabaseInspector:
    cls = INSPECTORS.get(dialect.lower())
    if not cls:
        raise ValueError(f"Unsupported dialect: {dialect}. Available: {list(INSPECTORS.keys())}")
    return cls()