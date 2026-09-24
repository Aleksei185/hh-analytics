# Аналитика вакансий с trudvsem.ru

## Описание проекта

Проект представляет собой ETL-пайплайн для сбора, очистки и анализа вакансий с портала «Работа России» (trudvsem.ru).
Данные собираются через открытый REST API, загружаются в PostgreSQL, очищаются и визуализируются в Apache Superset.

## Архитектура

trudvsem.ru API -> Python → PostgreSQL-> Apache Superset


## Стек технологий

- **Python 3.11**
- **PostgreSQL 15**
- **Apache Superset**
- **Redis**
- **Docker + Docker Compose**

## Структура проекта

```
hh-analytics/
├── docker-compose.yml
├── collect_vacancies.py
├──count_vacancies.py
├── requirements.txt
├── sql/
│ └── analytics_queries.sql
├── .github/
│ └── workflows/
│ └── ci.yml
├── screenshots/
├── .gitignore
└── README.md
```


## Как запустить

### Требования

- Docker Desktop
- Python 3.10+

### Шаги

1. Клонировать репозиторий:
   ```bash
   git clone https://github.com/Aleksei185/hh-analytics.git
   cd hh-analytics
2. Запустить контейнеры
   ```bash
   docker compose up-d
3. Установить библиотеки
   ```bash
   pip install -r requirements.txt
4. Создать таблицу
   ```bash
   docker compose exec postgres psql -U hh_user -d hh_analytics
5. Собрать данные
   ```bash
   python collect_vacancies.py
6. Выполнить SQL из sql/analytics_queries.sql
7. Открыть Superset: http://localhost:8088 (пользователь и пароль - admin)


## Дашборд

![Дашборд](screenshots/HH%20Analytics.png)

## Автор

Алексей Чвирук, 2026
