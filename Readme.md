Система для анализа структуры PostgreSQL и генерации DDL для MS SQL.

Цель: Добавить возможность работы с новой системой управления базами данных (в моем случае — PostgreSQL), не нарушая существующую логику приложения, за счёт заранее предусмотренной гибкой архитектуры. 
Создать расширяемую систему для анализа структуры БД, чтения метаданных и генерации DDL, поддерживающую разные СУБД через единый интерфейс.

Абстрактный класс BaseDatabase (database/base.py) Это контракт — то, что обязана уметь любая поддерживаемая СУБД.Чтобы любой код, работающий с БД (миграция), мог вызывать db.get_tables() независимо от того, PostgreSQL это или MS SQL

Фабрика factory.py позволяет создавать нужную реализацию по имени СУБД.

Согласование нейминга — любой код, использующий BaseDatabase, знает, что ожидать.

Функция проверки доступа  -Реализована в check_read_access() — минимальная проверка: может ли пользователь читать из системных таблиц или хотя бы одну таблицу.?


##  Файлы в проекте

```
migration-data/
├── database/
│   ├── __init__.py
│   ├── inspector.py
│   ├── registry.py
│   ├── type_mapping.py
│   └── dialects/
│       ├── __init__.py
│       └── postgres.py
├── ddl/
│   ├── __init__.py
│   └── generator.py
├── dags/                 ← для Airflow
│   └── pg_ddl_dag.py
├── docker-compose.yml    ← для тестовой БД
└── example.py            ← локальный запуск
```


# Система анализа структуры PostgreSQL и генерации DDL для MS SQL

Инструмент для безопасного и расширяемого анализа метаданных PostgreSQL и автоматической генерации совместимых DDL-скриптов для Microsoft SQL Server. Поддерживает правильную последовательность миграции (справочники → факты) и интеграцию с Apache Airflow.

---

## Структура проекта

```
migration-data/
├── database/                 # Абстракции и реализации СУБД
│   ├── __init__.py
│   ├── inspector.py          # Абстрактный класс DatabaseInspector
│   ├── registry.py           # Фабрика get_inspector()
│   ├── type_mapping.py       # Преобразование типов PG → MS SQL
│   └── dialects/
│       ├── __init__.py
│       └── postgres.py       # Реализация для PostgreSQL
├── ddl/
│   ├── __init__.py
│   └── generator.py          # Генерация DDL для MS SQL
├── utils/
│   └── dag_utils.py          # Топологическая сортировка таблиц
├── dags/                     # DAG-файлы для Airflow
│   └── pg_to_mssql_ddl.py
├── docker-compose.yaml       # Запуск Airflow + PostgreSQL
├── example.py                # Локальный запуск (анализ + вывод в консоль)
└── save_file.py              # Локальный запуск с сохранением DDL в файл
```

---

## Быстрый старт 

<details>
<summary><b>1. Подготовка окружения</b></summary>

```bash
# Создать и активировать виртуальное окружение
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# или .venv\Scripts\activate (Windows)

# Установить зависимости
pip install psycopg2-binary
```
</details>

<details>
<summary><b>2. Запуск тестовой БД</b></summary>

Запустите PostgreSQL в Docker:

```bash
docker run -d \
  --name pg-migration-source \
  -e POSTGRES_DB=migration_source \
  -e POSTGRES_USER=migrator \
  -e POSTGRES_PASSWORD=secure_password123 \
  -p 5432:5432 \
  postgres:15
```

Или используйте `docker-compose` из проекта (см. ниже).
</details>

<details>
<summary><b>3. Настройка кредов</b></summary>

В файлах `example.py` или `save_file.py` замените:

```python
user="your_user",
password="your_password",
dbname="your_db"
```

на:

```python
user="migrator",
password="secure_password123",
dbname="migration_source"
```
</details>

<details>
<summary><b>4. Запуск анализа</b></summary>

```bash
python example.py        # вывод в консоль
python save_file.py      # сохранение в all_tables_ddl.sql
```

Результат: файл `all_tables_ddl.sql` с готовыми скриптами для MS SQL.
</details>

---

## Запуск с Airflow 

<details>
<summary><b>1. Подготовка</b></summary>

Убедитесь, что Docker и Docker Compose установлены.

Создайте файл `.env` для Airflow UID:

```bash
echo "AIRFLOW_UID=$(id -u)" > .env
```
</details>

<details>
<summary><b>2. Запуск Airflow + PostgreSQL</b></summary>

```bash
docker-compose up -d
```

Дождитесь запуска (~1–2 мин).  
Откройте: http://localhost:8080  
Логин: `admin` / Пароль: `admin`
</details>

<details>
<summary><b>3. Подготовка DAG</b></summary>

Скопируйте ваш код в папку `dags/`:

```bash
cp -r database dags/
cp -r ddl dags/
cp -r utils dags/
cp dags/pg_to_mssql_ddl.py dags/
```

Airflow автоматически обнаружит DAG.
</details>

<details>
<summary><b>4. Настройка Connections</b></summary>

В UI Airflow (**Admin → Connections**) создайте:

- **Conn Id**: `pg_source`
  - **Conn Type**: `PostgreSQL`
  - **Host**: `postgres-source`
  - **Port**: `5432`
  - **Login**: `migrator`
  - **Password**: `secure_password123`
  - **Database**: `migration_source`

> Хост — `postgres-source` (имя сервиса в `docker-compose.yaml`), не `localhost`!
</details>

<details>
<summary><b>5. Запуск миграции</b></summary>

1. Включите DAG `pg_to_mssql_schema_migration`.
2. Нажмите **Trigger DAG**.
3. Результат:
   - Анализ структуры,
   - Построение зависимостей,
   - Генерация DDL в правильном порядке,
   - (Опционально) создание таблиц в MS SQL.
</details>



