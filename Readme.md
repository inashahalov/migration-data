система для анализа структуры PostgreSQL и генерации DDL для MS SQL.

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

## Как пользоваться 
## Локальный анализ БД

Конечно! Вот готовый блок для `README.md` с **сворачиваемыми разделами**, включающий краткое содержание шагов 1–6:

```markdown
<details>
<summary><b>1. Подготовка окружения</b></summary>

Создайте виртуальное окружение и установите зависимости:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# или .venv\Scripts\activate (Windows)
pip install psycopg2-binary
```
</details>

<details>
<summary><b>2. Запуск тестовой БД в Docker</b></summary>

Используйте `docker-compose.yml`, чтобы развернуть PostgreSQL:
```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: migration_source
      POSTGRES_USER: migrator
      POSTGRES_PASSWORD: secure_password123
    ports:
      - "5432:5432"
```
Запустите:  
```bash
docker-compose up -d
```
</details>

<details>
<summary><b>3. Разработка архитектуры</b></summary>

Проект использует модульную структуру:
- `database/inspector.py` — абстрактный класс `DatabaseInspector`
- `database/dialects/postgres.py` — реализация для PostgreSQL
- `database/registry.py` — фабрика `get_inspector()`
- `database/type_mapping.py` — преобразование типов PG → MS SQL
- `ddl/generator.py` — генерация DDL для MS SQL

Архитектура расширяема: легко добавить поддержку MySQL, Oracle и др.
</details>

<details>
<summary><b>4. Первый запуск (анализ)</b></summary>

Обновите креды в `example.py` и запустите:
```bash
python example.py
```
Скрипт подключится к БД, прочитает структуру и выведет:
- Список таблиц
- DDL для первой таблицы
- Размер таблицы в КБ
</details>

<details>
<summary><b>5. Сохранение результата</b></summary>

Используйте скрипт вроде `save_file.py`, чтобы сохранить DDL всех таблиц в файл:
```sql
-- Таблица: users
CREATE TABLE [users] (...);
```
Результат: файл `all_tables_ddl.sql` в корне проекта — готов к использованию в MS SQL.
</details>

