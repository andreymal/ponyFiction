# Справка по разработке

Для корректной работы приложения необходимо несколько сервисов.
Управление ими реализовано с помощью vagga (user-space контейнеризатора; впрочем, можно использовать и Docker)

## Процесс разворачивания рабочего окружения

_Пример дан для **Ubuntu 14.04 LTS**_

1. Установка vagga; подробнее — см. на [странице документации Vagga](http://vagga.readthedocs.org/en/latest/installation.html#ubuntu)
2. Клонирование репозитория:
    `git clone https://github.com/RuFimFiction/ponyFiction.git`
    `cd ponyFiction`

3. Создание необходимых каталогов для работы
    `mkdir -p run/storage/{redis,sphinx,mysql}`
    `mkdir -p run/log/{nginx,sphinx,mysql}`

4. Заполнение базы данных
    * Инициализация чистой базы данных: `vagga db_init`
    * Накатывание миграций: `vagga manage.py migrate`
    * Создание суперпользователя: `vagga manage.py createsuperuser`
    * Загрузка фикстур: `vagga manage.py loaddata ponyFiction/fixtures/*`

После успешного заполнения можно запустить весь стек со всеми контейнерами — `vagga run` 

## Запуск сервисов

_Перед началом работы весьма полезно прочесть [справку](http://vagga.readthedocs.org/en/latest/commandline.html)_

Запуск полного стека со всеми контейнерами — `vagga run`

Для запуска только указанных сервисов из стека — `vagga run --only <service1> (<service2> …)`, например, `vagga run --only nginx`

Иногда для отладки бывает полезно исключить какой-то сервис из стека и запустить его отдельно в консоли. 
Чаще всего это касается приложения. Для этого — `vagga run --exclude uwsgi`
