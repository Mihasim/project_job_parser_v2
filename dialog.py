from parsers import SuperJobParser, HHParser, Saver, Loader, Deleter


def start(api, vacancies_file):
    while True:
        user_input = input("Введите - 1, чтобы загрузить новый список вакансий,\n"
                           "Введите - 2, чтобы редактировать существующий список. \n"
                           "Введите 'exit' чтобы завершить работу программы\n")

        if user_input == "exit":
            print("Завершение работы")
            quit()

        elif user_input == "1":
            load_vac(api, vacancies_file)


        elif user_input == "2":
            editing_file(vacancies_file)

        else:
            print("неизвестная команда, повторите попытку")


def load_vac(api, vacancies_file):
    keyword = input("Введите ключевое слово для фильтрации вакансий: ")
    count_vac = int(input("Сколько вакансий вы хотите вывести (не более 100): "))

    if count_vac > 100:
        print("Будет выведено максимальное значение вакансий (100шт)")
        count_vac = 100

    superjob_parser = SuperJobParser((int(count_vac / 2)), keyword, api)
    hh_parser = HHParser((int(count_vac / 2)), keyword)

    try:
        list_vacancies = superjob_parser.data_collector() + hh_parser.data_collector()
        saver = Saver(vacancies_file, list_vacancies)
        saver.save()
    except TypeError:
        print("TypeError: Невозможно сохранить данные по этому запросу")
        quit()

    sort_vacancies(vacancies_file)


def sort_vacancies(vacancies_file) -> list:
    """
    В зависимости от того по какому признаку пользователю необходимо
    отсортировать вакансии функция сортирует вакансии и возвращает
    отсортированный список
    :param tipe_sort:
    :return:
    """
    loader = Loader(vacancies_file)
    data_vacancies = loader.load()  # Открываем список вакансий

    while True:
        tipe_sort = int(input("Укажите по какому критерию провести сортировку:\n"
                              "1 -зарплата, 2 -дата публикации: "))
        if tipe_sort == 1 or tipe_sort == 2:
            break
        else:
            print("Введено неверное значение, попробуйте снова")

    while True:
        revers_sort = int(input("Сортировать вакансии:\n"
                                "1 -по убыванию, 2 - по возрастанию: "))
        if revers_sort == 1:
            rev = True
            break
        elif revers_sort == 2:
            rev = False
            break
        else:
            print("Команда не распознана")

    while True:
        if tipe_sort == 1:
            none_payment = []

            for i in range(len(data_vacancies)):
                for data in data_vacancies:
                    # Удаляем из списка вакансии в которых зарплата не указана чтобы добавить их в конец
                    if isinstance(data['payment_from'], str):
                        none_payment.append(data)
                        data_vacancies.remove(data)

            # Сортировка по зарплате
            sort_with_payment = sorted(data_vacancies, key=lambda k: k['payment_from'], reverse=rev)
            all_sorted = sort_with_payment + none_payment
            return all_sorted

        elif tipe_sort == 2:
            # Сортировка по дате публикации
            sort_with_date = sorted(data_vacancies, key=lambda k: k['date_published'], reverse=rev)
            return sort_with_date

        else:
            print("Команда не распознана")


def editing_file(vacancies_file):
    loader = Loader(vacancies_file)
    data_vacancies = loader.load()
    i = 0
    while True:
        data = data_vacancies[i]
        print(data["profession"])
        print("дата публикации", data["date_published"], "\n",
              "Зарплата от: ", data["payment_from"], data["currency"], "\n",
              "Зарплата до: ", data["payment_to"], data["currency"], "\n",
              "Описание:\n", data["description"], "\n",
              "Ссылка на вакансию", data["link_to_vacancy"], "\n\n"
              )

        user_input = input("Введите 1 чтобы перейти к следующей вакансии,\n"
                           "Введите 2 чтобы вернуться к предыдущей вакансии\n"
                           "Введите 0 чтобы удалить текущую вакансию из списка\n"
                           "Введите 'exit' чтобы завершить работу программы\n")

        if user_input == "exit":
            print("Завершение работы")
            quit()

        if user_input == "1":

            if i < len(data):
                i += 1
            else:
                print("Это последняя вакансия")

        elif user_input == "2":
            if i > 0:
                i -= 1
            else:
                print("Это первая вакансия")

        elif user_input == "0":
            deleter = Deleter(vacancies_file, data_vacancies)
            deleter.del_vac(data)
            saver = Saver(vacancies_file, data_vacancies)
            saver.save()
