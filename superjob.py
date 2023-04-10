from time import sleep
from itertools import count

import requests

from predict_rub_salary import predict_rub_salary


def get_vacancies(language, api_token_superjob, page=0, id_city=4):
    superjob_url = "https://api.superjob.ru/2.0/vacancies/"
    headers = {
        "X-Api-App-Id": f"{api_token_superjob}"
    }
    params = {
        "page": page,
        "town": id_city,
        "keyword": f"Разработчик {language}",
        "count": 100,
    }

    response = requests.get(superjob_url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()



def get_language_characteristic(language, api_token_superjob):
    salaries = []
    for page in count(0):
        vacancies = get_vacancies(language, api_token_superjob, page)
        if not vacancies['more']:
            break
        for vacancy in vacancies["objects"]:
            if not vacancy["currency"] == "rub":
                continue
            if vacancy["payment_from"] == 0 and vacancy["payment_to"] == 0:
                continue

            salaries.append(predict_rub_salary(vacancy["payment_from"], vacancy["payment_to"]))
        salaries = [salary for salary in salaries if salary is not None]

    sum_salaries = sum(salaries)
    counts = len(salaries)
    if salaries:
        average_salary = int(sum_salaries / counts)
    else:
        average_salary=0
    language_characteristic={
        "vacancies_found":vacancies["total"],
        "vacancies_processed": counts,
        "average_salary": average_salary,
    }

    return language_characteristic


def get_statistics_vacancies(languages, api_token_superjob):
    languages_stats = {}
    try:
        for language in languages:
            languages_stats[language] = get_language_characteristic(language, api_token_superjob)
        return languages_stats
    except requests.exceptions.ConnectionError:
        sleep(20)
