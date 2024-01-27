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
### Основной запуск проекта

Для основного запуска проекта введите команду:

```bash
docker compose up --build
```

Для запуска проекта в фоновом режиме необходимо добавить флаг `-d`:

```bash
docker compose up --build -d
```
### Запуск проекта с прохождением тестов

Для запуска проекта с прохождением тестов через pytest используйте команду:

```bash
docker compose -f docker-compose-test.yml up --build
```