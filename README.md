# FastAPI-Restaurant
## Установка и запуск

Скопируйте репозиторий используя следующую команду:

```bash
git clone https://github.com/YuryRass/FastAPI_Restaurant.git
```

Затем перейдите в каталог с проектом:

```bash
cd FastAPI_Restaurant
```

В корне проекта переименуйте конфигурационные файлы `.env.example` и `.env_test.example` на `.env` и `.env_test`

На операционной системе Linux переименовать файлы можно следующей командой:

```bash
mv .env.example .env && mv .env_test.example .env_test
```

Для запуска проекта введите команду:

```bash
docker-compose up --build
```

Для запуска проекта в фоновом режиме необходимо добавить флаг `-d`:

```bash
docker-compose up --build -d
```
