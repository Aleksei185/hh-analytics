import requests

def count_vacancies(query):
    url = 'http://opendata.trudvsem.ru/api/v1/vacancies'
    params = {
        'text': query,
        'limit': 1,
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data['meta']['total']

if __name__ == '__main__':
    queries = ['Data Analyst', 'Python', 'SQL', 'Аналитик', 'Аналитик данных', 'Data Scientist']

    print(f"{'Профессия':<25} | {'Вакансий':>10}")
    print("-" * 40)
    for q in queries:
        total = count_vacancies(q)
        print(f"{q:<25} | {total:>10}")