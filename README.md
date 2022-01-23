# VK bot

Бот VK (сообщения сообщества) - витрина выпечки (разделы товаров и
непосредственно сами товары с описанием и фотографией). Из раздела можно
возвращаться назад. Для навигации используются кнопки.

Используются библиотеки _VKWave_, _SQLAlchemy_ и база _PostgreSQL_.

Запуск:

1. Скопировать файл '.env.example' в '.env'

    `make prepare-files`

1. Добавить в файл '.env' токен и id  сообщества

1. Запустить _Docker Compose_ сервисы

    `make up`

## Prerequisites

- pipenv
- make
- docker
- docker-compose

## Commands

- Copy '.env.example' file to '.env'

  `make prepare-files`

- Start _Docker Compose_ services

  `make up`

- Setup a working environment using _Pipenv_

  `make setup`

- Start application (with database)

  `make start`

- Run linter

  `make lint`

- List all available _Make_ commands

  `make help`
