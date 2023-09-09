import json
from abc import ABC

import requests
from datetime import datetime


class Parsers(ABC):

    def data_collector(self) -> list:
        pass


class Savers(ABC):

    def save(self):
        pass


class Deleters(ABC):

    def del_vac(self, vacancy: dict) -> None:
        pass


class Loaders(ABC):

    def load(self):
        pass


class SuperJobParser(Parsers):
    """
    Получение списка вакансий с сайта superjob
    """

    def __init__(self, count_vacancy, keyword, API_KEY):
        self.count_vacancy = count_vacancy
        self.keywords = keyword
        self.url = f'https://api.superjob.ru/2.0/vacancies'
        response = requests.get(self.url, headers={"X-Api-App-Id": API_KEY},
                                params={"keyword": keyword,
                                        "count": self.count_vacancy,
                                        "currency": "rub",
                                        "no_agreement": "1"})
        self.vacancies = response.json()

    def data_collector(self) -> list:
        """
        Сбор дранных о вакансиях superjob
        :return: список словарей с вакансиями
        """
        list_vacancies = []
        try:
            for i in range(self.count_vacancy + 1):
                if int(self.vacancies["objects"][i]["payment_from"]) == 0:
                    payment_from = self.vacancies["objects"][i]["payment_to"]
                else:
                    payment_from = self.vacancies["objects"][i]["payment_from"]  # Зарплата от...
                if int(self.vacancies["objects"][i]["payment_to"]) == 0:
                    payment_to = "Зарплата до..., не указана"

                else:
                    payment_to = self.vacancies["objects"][i]["payment_to"]  # Зарплата до...
                date_published = datetime.fromtimestamp(self.vacancies["objects"][i]["date_published"]). \
                    strftime("%d.%b.%Y %H:%M:%S")  # Время публикации
                profession = self.vacancies["objects"][i]["profession"]  # Профессия
                description = self.vacancies["objects"][i]["candidat"]  # Информация кандидату
                currency = self.vacancies["objects"][i]["currency"]  # Оплата в валюте

                if currency == "KZT":
                    if payment_from != "Зарплата до... не указана":
                        payment_from = int(payment_from)
                        payment_from *= 0.21
                    if payment_to != "Зарплата до... не указана":
                        payment_to = int(payment_to)
                        payment_to *= 0.21
                    currency = "RUB"
                if currency == "USD":
                    if payment_from != "Зарплата до... не указана":
                        payment_from = int(payment_from)
                        payment_from *= 98
                    if payment_to != "Зарплата до... не указана":
                        payment_to = int(payment_to)
                        payment_to *= 98
                    currency = "RUB"

                link_to_vacancy = self.vacancies["objects"][i]["link"]  # Ссылка на вакансию
                vacancy_dict = {"profession": profession,
                                "date_published": date_published,
                                "payment_from": payment_from,
                                "payment_to": payment_to,
                                "currency": currency,
                                "description": description,
                                "link_to_vacancy": link_to_vacancy,
                                }
                list_vacancies.append(vacancy_dict)
        except IndexError:
            print(f"По данному ключевому слову на superjob найдено {i} вакансий")
        return list_vacancies

    def __repr__(self):
        return f"{self.__class__.__name__},{self.count_vacancy},{self.keywords}"


class HHParser(Parsers):
    """
    Получение списка вакансий с сайта superjob
    """

    def __init__(self, count_vacancy, keyword) -> None:
        self.count_vacancy = count_vacancy
        self.keyword = " ".join(keyword)
        self.url = f"https://api.hh.ru/vacancies"
        response = requests.get(self.url, params={"text": keyword,
                                                  "per_page": self.count_vacancy,
                                                  "page": 1})
        self.vacancies = response.json()
        try:
            self.vacancy_url = self.vacancies["items"][0]["url"]
        except IndexError:
            self.vacancy = False
            print("IndexError: По данному ключевому слову вакансий на hh.ru не найдено")
        except KeyError:
            self.vacancy = False
            print("KeyError: По данному ключевому слову вакансий на hh.ru не найдено")
        else:
            self.vacancy_data = requests.get(self.vacancies["items"][0]["url"]).json()
            for i in range(self.count_vacancy):
                self.vacancy = requests.get(self.vacancies["items"][i]["url"]).json()

    def data_collector(self) -> list:
        """
        Сбор дранных о вакансиях hh.ru
        :return: список словарей с вакансиями
        """
        list_vacancies = []
        if self.vacancy:
            for i in range(self.count_vacancy + 1):
                try:
                    self.vacancy = requests.get(self.vacancies["items"][i]["url"]).json()
                except IndexError:
                    print(f"По данному ключевому слову на hh.ru найдено {i} вакансий")

                if self.vacancy["salary"] is None:
                    payment_from = "Зарплата не указана"
                    payment_to = "Зарплата не указана"
                    currency = "валюта не указана"  # Оплата в валюте
                else:
                    if self.vacancy["salary"]["from"] is None:
                        payment_from = self.vacancy["salary"]["to"]
                    else:
                        payment_from = self.vacancy["salary"]["from"]  # Зарплата от...
                    if self.vacancy["salary"]["to"] is None:
                        payment_to = "Зарплата до... не указана"
                    else:
                        payment_to = self.vacancy["salary"]["to"]  # Зарплата до...
                    currency = self.vacancy["salary"]["currency"]  # Оплата в валюте
                    if currency == "KZT":
                        if payment_from != "Зарплата до... не указана":
                            payment_from = int(payment_from)
                            payment_from *= 0.21
                        if payment_to != "Зарплата до... не указана":
                            payment_to = int(payment_to)
                            payment_to *= 0.21
                        currency = "RUB"
                    if currency == "USD":
                        if payment_from != "Зарплата до... не указана":
                            payment_from = int(payment_from)
                            payment_from *= 98
                        if payment_to != "Зарплата до... не указана":
                            payment_to = int(payment_to)
                            payment_to *= 98
                        currency = "RUB"

                date_from_json = self.vacancy["published_at"][:-5]
                import_data = datetime.strptime(date_from_json, "%Y-%m-%dT%H:%M:%S")
                date_published = import_data.strftime("%d.%b.%Y %H:%M:%S")  # Время публикации

                profession = self.vacancy["name"]  # Профессия
                description = self.vacancy["description"]  # Описание

                link_to_vacancy = self.vacancy["alternate_url"]  # Ссылка на вакансию

                vacancy_dict = {"profession": profession,
                                "date_published": date_published,
                                "payment_from": payment_from,
                                "payment_to": payment_to,
                                "currency": currency,
                                "description": description,
                                "link_to_vacancy": link_to_vacancy,
                                }
                list_vacancies.append(vacancy_dict)
            return list_vacancies

    def __repr__(self):
        return f"{self.__class__.__name__},{self.count_vacancy},{self.keyword}"


class Saver(Savers):
    """
    Объединение списков словарей с данными о вакансиях и
    сохранение информации о вакансии в файл в формате json
    """

    def __init__(self, file: str, list_vacancies: list) -> None:
        self.file = file
        self.list_vacancies = list_vacancies

    def save(self) -> None:
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(self.list_vacancies, f, indent=2, ensure_ascii=False)
        print(f"Список вакансий сохранен в файл {self.file}")


class Deleter(Deleters):

    def __init__(self, file: str, list_vacancies: list) -> None:
        self.file = file
        self.list_vacancies = list_vacancies

    def del_vac(self, vacancy: dict) -> None:
        """
        Удаляет вакансию из списка словарей.
        В случае отсутствия вакансии ничего не делает
        :return:
        """
        try:
            self.list_vacancies.remove(vacancy)
        except ValueError:
            pass


class Loader(Loaders):
    """
    Класс загрузчик получает список словарей с вакансиями из файла json
    """

    def __init__(self, file: str) -> None:
        self.file = file

    def load(self) -> list:
        with open(self.file, 'r', encoding="utf-8") as f:
            data_vacancies = json.load(f)
        return data_vacancies
