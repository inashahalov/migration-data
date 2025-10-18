from abc import ABC, abstractmethod
from typing import List, Dict, Any

class DatabaseInspector(ABC):
    @classmethod
    @abstractmethod
    def dialect_name(cls) -> str:
        """Название диалекта: 'postgresql', 'mssql' и т.д."""
        pass

    @abstractmethod
    def get_tables(self, conn) -> List[str]:
        """Получить список таблиц."""
        pass

    @abstractmethod
    def get_columns(self, conn, table: str) -> List[Dict[str, Any]]:
        """
        Вернуть список колонок. Обязательные ключи:
        - name: str
        - data_type: str (в терминах ИСТОЧНИКА)
        - is_nullable: bool
        - is_primary_key: bool
        """
        pass

    @abstractmethod
    def get_table_size(self, conn, table: str) -> int:
        """Размер таблицы в байтах."""
        pass

    @abstractmethod
    def get_table_dependencies(self, conn) -> Dict[str, List[str]]:
        pass