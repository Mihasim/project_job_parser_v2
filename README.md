# project_job_parser_v2
Программа для парсинга сайтов superjob.ru и hh.ru

При первои запуске программа попросит выбрать одно из действий: 
"Введите - 1, чтобы загрузить новый список вакансий, 
Введите - 2, чтобы редактировать существующий список. 
Введите 'exit' чтобы завершить работу программы"

Для того чтобы загрузить список вакансий необходимо выбрать первый вариант.

Далее программа попросит ввести ключевое слово по которому будет производить поиск. 
"Введите ключевое слово для фильтрации вакансий:" 
Вводим ключевое слово например "python"

Затем программа спросит сколько вакансий необходимо загрузить. 
"Сколько вакансий вы хотите вывести (не более 100):" 
Ввобим значение (не более 100). Программа разделит это значение на пополам между сайтами juperjob.ru и hh.ru. 
Полученные с сайтов значения сохранятся в формате json в файл "vacancies.json".

Далее необходимо выбрать по какому критерию сортировать данные: 
"Укажите по какому критерию провести сортировку: 
1 -зарплата, 2 -дата публикации: " 
затем в зависимости от выбранного варианта выбрать как сортировать: 
"Сортировать вакансии: 1 -по убыванию, 2 - по возрастанию:"

Полученный список перезаписывается в файл "vacancies.json"

Теперь программа снова попросит выбрать одно из действий: 
"Введите - 1, чтобы загрузить новый список вакансий, 
Введите - 2, чтобы редактировать существующий список. 
Введите 'exit' чтобы завершить работу программы"

При выборе второго варианта на экран выводится первая вакансия из списка и варианты последующих действий:

Введите 1 чтобы перейти к следующей вакансии, Выведит на экран следующую вакансию

Введите 2 чтобы вернуться к предыдущей вакансии Выведит на экран предыдущую вакансию

Введите 0 чтобы удалить текущую вакансию из списка 
Удалит вакансию из файла "vacancies.json"

Введите 'exit' чтобы завершить работу программы завершит работу программы