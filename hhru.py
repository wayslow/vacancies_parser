import requests


def get_vacancies(language="Python", id_city=1, page=0):
    hh_url = "https://api.hh.ru/vacancies"
    params = {
        "text": language,
        "area": id_city,
        "per_page":100,
        'page': page
    }
    response = requests.get(hh_url, params=params)
    response.raise_for_status()
    return response.json()


def get_salary_info(language):
    vacances=get_vacancies(language)
    salares = []
    for page in range(vacances["pages"]):
        vacances = get_vacancies(language, page=page)
        for vacancy in vacances["items"]:
            try:
                salares.append(predict_rub_salary(vacancy["salary"]))
            except TypeError:
                pass
    salares = [salary for salary in salares if salary is not None]
    return salares


def predict_rub_salary(salary_ivfo):
    if salary_ivfo["currency"] == "RUR":
        return salary_ivfo["from"]


def count_average_salary(language):
    salares = get_salary_info(language)
    sum_salares = sum(salares)
    count= len(salares)
    average_salary = sum_salares/count
    return average_salary, count


def get_statistics_vacancies(languages):
    languages_stats = {}
    for language in languages:
        average, average_count = count_average_salary(language)
        average = int(average)
        all_cuont = get_vacancies(language)["found"]
        languages_stats[language] = {
            "vacancies_found": all_cuont,
            "vacancies_processed": average_count,
            "average_salary": average,
        }

    return languages_stats
