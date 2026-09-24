import requests
import psycopg2
from datetime import datetime
import time

DB_CONFIG = {
    'host': 'localhost',
    'port': 5434,
    'database': 'hh_analytics',
    'user': 'hh_user',
    'password': 'hh_password'
}

def fetch_vacancies(query='Аналитик', pages=5):
    vacancies = []
    url = 'http://opendata.trudvsem.ru/api/v1/vacancies'
    limit = 100

    for page in range(pages):
        params = {
            'text': query,
            'limit': limit,
            'offset': page * limit,
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"Ошибка: {response.status_code}")
            break
        data = response.json()
        items = data.get('results', {}).get('vacancies', [])
        vacancies.extend(items)
        print(f"Страница {page + 1}: собрано {len(items)} вакансий")
        time.sleep(10)

    return vacancies

def save_to_db(vacancies):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    inserted = 0
    for item in vacancies:
        v = item['vacancy']
        salary_min = v.get('salary_min')
        salary_max = v.get('salary_max')
        region = v.get('region', {}).get('name', '')
        company = v.get('company', {}).get('name', '')
        skills = ', '.join(v.get('skills', []))
        published = v.get('creation-date')

        try:
            cur.execute("""
                INSERT INTO vacancies (
                    vacancy_id, title, company, city, salary_from, salary_to,
                    currency, experience, schedule, key_skills, published_at, url
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (vacancy_id) DO NOTHING
            """, (
                v.get('id'),
                v.get('job-name'),
                company,
                region,
                salary_min,
                salary_max,
                v.get('currency'),
                v.get('requirement', {}).get('experience'),
                v.get('schedule'),
                skills,
                published,
                v.get('vac_url')
            ))
            inserted += 1
        except Exception as e:
            print(f"Ошибка при вставке: {e}")
            conn.rollback()
            continue

    conn.commit()
    cur.close()
    conn.close()
    return inserted

if __name__ == '__main__':
    QUERIES = [
        'Аналитик',
        'Аналитик данных',
        'Бизнес-аналитик',
        'Системный аналитик',
        'Продуктовый аналитик',
    ]
    
    total_inserted = 0
    for query in QUERIES:
        print(f"\n=== Запрос: {query} ===")
        vacancies = fetch_vacancies(query=query, pages=1)
        print(f"Собрано: {len(vacancies)} вакансий")
        
        if vacancies:
            inserted = save_to_db(vacancies)
            print(f"Загружено: {inserted} записей")
            total_inserted += inserted
    
    print(f"\nВсего загружено: {total_inserted} записей")