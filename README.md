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
docker compose up --build -d
```
### Запуск проекта с прохождением тестов

Тестовые сценарии расположены в каталоге `app/tests`

В файле `app/tests/test_all.py` реализован тестовый сценарий «Проверка количества блюд и подменю в меню»

Во всех остальных файлах каталога написаны CRUD тесты для разработанных API:
> * test_menu.py
> * test_submenu.py
> * test_dish.py

Для запуска проекта с прохождением тестов через pytest используйте команду:

```bash
docker compose -f docker-compose-test.yml up --build -d && docker logs --follow test_rest_app && docker compose -f docker-compose-test.yml down -v
```

## Количество подменю и блюд

Вывод количества подменю и блюд для Меню через один (сложный) ORM запрос реализован в файле `app/menu/dao.py` в методе `show` класса `MenuDAO`

## Контакты

**telegram** [@YurySundown](https://t.me/YurySundown)

**e-mail** <yurchik1997yurchik@gmail.com>