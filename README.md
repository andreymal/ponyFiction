# Поднятие ponyFiction

1. Ставим Linux, на него MySQL, Sphinx, Redis, какой-нибудь почтовый сервер, memcached, Python 2 и virtualenv

2. Поднимаем виртуальное окружение и далее работаем в нём:

 `cd ponyFiction`

 `virtualenv --no-site-packages env`

 `source env/bin/activate` (выход через команду `deactivate`)

3. Устанавливаем зависимости:

 `pip install -r requirements.txt`

4. В файлах конфигурации `ponyFiction/settings.py` и `sphinx.conf` прописываем название базы данных MySQL, имя пользователя и пароль (и создаём их в самом MySQL)

5. Инициализируем базу и попутно создаём пользователя:

 `python manage.py syncdb`

6. Запускаем сервер:

 `python manage.py runserver`

7. Заходим на `http://localhost:8000/admin/` и заполняем базу, создавая объекты:

 - Группы персонажей

 - Персонажи

 - Категории (Жанры)

 - Классификаторы (События)

 - Рейтинги
