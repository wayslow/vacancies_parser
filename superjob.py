import os

import requests
from dotenv import load_dotenv


load_dotenv()
API_TOKEN = os.getenv('SUPERJOB_API_TOKEN')


def get_vacancies(language , id_city=4, page=0):
    superjob_url = "https://api.superjob.ru/2.0/vacancies/"
    headers = {
        "X-Api-App-Id": f"{API_TOKEN}"
    }
    params = {
        "page":page,
        "town":id_city,
        "keyword":f"Разработчик {language}",
        "count":100,
    }
    response = requests.get(superjob_url, headers=headers, params=params)
    response.raise_for_status()

    return response.json()


def get_salary_info(language):
    salares = []
    vacancies_found = 0
    for page in range(5):
        vacances = get_vacancies(language, page=page)["objects"]
        vacancies_found += len(vacances)
        for vacancy in vacances:
            try:
                salares.append(predict_rub_salary(vacancy))
            except TypeError:
                pass
    salares = [salary for salary in salares if salary is not None]
    return salares ,vacancies_found


def count_average_salary(language):
    salares, vacancies_found = get_salary_info(language)
    sum_salares = sum(salares)
    count= len(salares)
    average_salary = sum_salares/count
    return average_salary, count , vacancies_found


def predict_rub_salary(vacancy):
    if vacancy["currency"] == "rub" and vacancy["payment_from"] !=0 :
        return vacancy["payment_from"]


def get_statistics_vacancies(languages):
    languages_stats ={}

    for language in languages:
        average, average_count, vacancies_found = count_average_salary(language)
        average = int(average)
        languages_stats[language] = {
            "vacancies_found": vacancies_found,
            "vacancies_processed": average_count,
            "average_salary": average,
        }
    return languages_stats
