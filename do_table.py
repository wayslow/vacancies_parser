from terminaltables import DoubleTable

import superjob, hhru
def do_table(languages_stats, title):
    table_data = [
        ["languages", "vacancies_found", "vacancies_processed", "average_salary"],
    ]
    for language in languages_stats:
        language_stats = [language]
        for key in table_data[0][1:]:
            language_stats.append(languages_stats[language][key])
        table_data.append(language_stats)

    table_instance = DoubleTable(table_data, title)
    table_instance.justify_columns[2] = 'right'
    print(table_instance.table)
    print()


def main():
    languages = [
        "Objective-C",
        "GO",
        "C",
        "C#",
        "C++",
        "PHP",
        "Ruby",
        "Python",
        "Java",
        "JavaScript",
    ]
    superjob_statistics=superjob.get_statistics_vacancies(languages)
    hhru_statistics=hhru.get_statistics_vacancies(languages)
    do_table(superjob_statistics, "superjob")
    do_table(hhru_statistics, "hh.ru")


if __name__ == '__main__':
    main()
