# Baddream666-homework_8

# Платформа для онлайн-обучения

## Описание

Проект курса
В домашних заданиях курса вы реализуете платформу для онлайн-обучения,
на которой каждый желающий сможет размещать свои полезные материалы
или курсы.

Вы будете работать над SPA-приложением.
Результатом создания проекта будет бэкенд-сервер,
который возвращает клиенту JSON-структуры.

## Установка:

1. Клонируйте репозиторий:

```
git clone https://github.com/BadDream666/Homework_8.git
```
## Конфигурация
1. Создайте виртуальное окружение poetry.

```
poetry env
```

2. Установите библиотеки Flake8, black, isort, mypy в группу lint.

```commandline
poetry add --group lint flake8
poetry add --group lint black
poetry add --group lint isort
poetry add --group lint mypy
```

3. Создайте файл .flake8 для настройки библиотеки flak8


4. Настройте установленные библиотеки, используя кода ниже

Файл .flake8

```
[flake8]
max-line-length = 119
```

5. Установите требуемые библиотеки:
````commandline
poetry add requests
poetry add python-dotenv
poetry add psycopg2
poetry add django
poetry add redis
pip install djangorestframework
````

6. Инициализируйте django-проект внутри текущей директории
````
django-admin startproject config .
````


## Приложение по рассылки сообщений:

1. Создайте приложение mailing
````
python manage.py startapp mailing
````
2. Зарегистрируйте приложение в settings.py