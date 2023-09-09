import os

from dialog import start

API_KEY = os.getenv('SUPERJOB_API_KEY')  # API ключ superjob
vacancies = "vacancies.json"  # Файл куда будут сохраняться вакансии


if __name__ == '__main__':
    start(API_KEY, vacancies)
