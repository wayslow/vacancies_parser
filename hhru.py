from time import sleep

import requests
from itertools import count

from predict_rub_salary import predict_rub_salary


def get_vacancies(language, city_id=1, page=0):
    hh_url = "https://api.hh.ru/vacancies"
    params = {
        "text": language,
        "area": city_id,
        "per_page": 100,
        'page': page
    }
    response = requests.get(hh_url, params=params)
    response.raise_for_status()
    return response.json()


def get_language_characteristic(language):
    salaries = []
    for page in count(0):
        vacancies = get_vacancies(language, page=page)
        if page == vacancies['pages'] or page == 19:
            break
        for vacancy in vacancies["items"]:
            if not vacancy["salary"]:
                continue
            if not vacancy["salary"]["currency"] == "RUR":
                continue
            pred = predict_rub_salary(vacancy["salary"]["from"], vacancy["salary"]["to"])
            salaries.append(pred)
    salaries = [salary for salary in salaries if salary is not None]
    sum_salaries = sum(salaries)
    counts = len(salaries)
    if salaries:
        average_salary = int(sum_salaries / counts)
    else:
        average_salary = None

    language_characteristic = {
        "vacancies_found": vacancies["found"],
        "vacancies_processed": counts,
        "average_salary": average_salary,
    }

    return language_characteristic


def get_statistics_vacancies(languages):
    languages_stats = {}
    try:
        for language in languages:
            languages_stats[language] = get_language_characteristic(language)

        return languages_stats
    except requests.exceptions.ConnectionError:
        sleep(20)
