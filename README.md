ponyFiction
===========

CMS библиотеки на stories.everypony.ru


## Быстрый старт (развёртывание минимального окружения для разработки)

* Ставим Linux, на него какой-нибудь почтовый сервер, Python 3 и virtualenv

* Скачиваем ponyFiction, выполнив команду `git clone` или скачав и распаковав архив с репозитория

* Создаём виртуальное окружение и далее работаем в нём:

 `cd ponyFiction`

 `virtualenv --no-site-packages env`

 `source env/bin/activate` (выход через команду `deactivate`)

* Устанавливаем зависимости:

 `pip install -r requirements.txt`

* Указываем окружение, скопировав файл `environment.example.txt` в `environment.txt` и `sphinxroot.example.txt` в `sphinxroot.txt`

* Инициализируем базу (будет создан файл `db.sqlite3`), создаём суперпользователя и заполняем базу данными (персонажи, рейтинги, жанры, события):

 `python manage.py migrate`

 `python manage.py createsuperuser`

 `python manage.py loaddata ponyFiction/fixtures/*`

* Запускаем сервер:

 `python manage.py runserver`

* Заходим на `http://localhost:8000/`. После входа как суперпользователь можно обнаружить админку по адресу `http://localhost:8000/admin/`.


## Развёртывание приближенного к production окружения (с поиском и прочим)

* Выполняем первые пять пунктов из предыдущего списка

* Дополнительно устанавливаем Redis (для cacheops), memcached и Sphinx

* Устанавливаем и настраиваем MySQL, создаём пользователя и базу данных для сайта

* Создаём файл `ponyFiction/environments/local.py` (в local-файлах хранятся локальные настройки, которые нет смысла публиковать) и включаем в нём всё установленное ранее:

```
DATABASES['default'] = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'название базы mysql',
    'USER': 'имя пользователя mysql',
    'PASSWORD': 'пароль',
    'HOST': '',
    'PORT': '',
}

CACHES['default'] = {
    'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
    'LOCATION': '127.0.0.1:11211',
}

# Включаем кэширование объектов в Redis
CACHEOPS_FAKE = False

# Включаем поиск Sphinx
SPHINX_DISABLED = False

# Если хочется запустить отдельный воркер Celery, который будет обновлять индекс Sphinx, то прописываем это
CELERY_ALWAYS_EAGER = False
```

* Инициализируем базу, создаём суперпользователя, заполняем базу данными:

 `python manage.py migrate`

 `python manage.py createsuperuser`

 `python manage.py loaddata ponyFiction/fixtures/*`

* Запускаем Sphinx:

 `searchd --config sphinxconf.py`

* Если база данных уже не пустая, а поиск ещё пустой, то загружаем данные в индексы Sphinx:

 `python manage.py initsphinx`

* Запускаем воркер Celery, который будет обновлять индекс поиска (тоже в virtualenv):

* `celery worker -A ponyFiction --loglevel=INFO`

* Запускаем сервер:

 `python manage.py runserver`

* Если хочется запускать всё через Supervisor, то есть заранее заготовленные файлы `gunicorn_start` и `celery_start`

Для окружения production приведённые выше настройки (кроме базы данных) уже прописаны по умолчанию в `settings.py`.
