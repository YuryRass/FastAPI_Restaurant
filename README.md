# FastAPI-Restaurant
## Установка и запуск

Скопируйте репозиторий используя следующую команду:

`git clone https://github.com/YuryRass/FastAPI_Restaurant.git`

Затем перейдите в каталог с проектом:

`cd FastAPI_Restaurant`

В корне проекта переименуйте конфигурационные файлы `.env.psql-example` и `.env-example` на `.env.psql` и `.env`

На операционной системе Linux переименовать файлы можно следующей командой:

`mv .env.psql-example .env.psql && mv .env-example .env`

Для запуска проекта введите команду:

`docker-compose up --build`

Для запуска проекта в фоновом режиме необходимо добавить флаг `-d`:

`docker-compose up --build -d`
