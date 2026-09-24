CREATE TABLE vacancies (
    id              SERIAL PRIMARY KEY,
    vacancy_id      TEXT UNIQUE,
    title           TEXT,
    company         TEXT,
    city            TEXT,
    salary_from     INTEGER,
    salary_to       INTEGER,
    currency        TEXT,
    experience      TEXT,
    schedule        TEXT,
    key_skills      TEXT,
    published_at    TIMESTAMP,
    url             TEXT,
    created_at      TIMESTAMP DEFAULT NOW()
);

-- Топ городов по количеству вакансий


SELECT city, COUNT(*) AS vacancy_count
FROM vacancies
GROUP BY city
ORDER BY vacancy_count DESC
LIMIT 10;


-- Средняя зарплата по городам

SELECT 
    city, 
    ROUND(AVG(salary_from), 0) AS avg_salary
FROM vacancies
WHERE salary_from IS NOT NULL
GROUP BY city
ORDER BY avg_salary DESC
LIMIT 10;

-- Топ навыков

SELECT 
    TRIM(unnest(string_to_array(key_skills, ','))) AS skill,
    COUNT(*) AS cnt
FROM vacancies
WHERE key_skills IS NOT NULL 
  AND key_skills != ''
GROUP BY skill
ORDER BY cnt DESC
LIMIT 20;
