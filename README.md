### 🚀 Как запустить (Быстрый старт)

Вам понадобится только установленный Docker и Docker Compose.

- 1. Клонируй проект и перейди в его папку.

`https://github.com/xash1rama/Luna.git`


- 2. Запусти контейнеры:
bash
`docker-compose up --build`

Готово! 

- 3. Перейдите:
`http://localhost:8000/docs`

Авторизация: В Swagger нажми Authorize и введи ключ из .env (База: luna).


Мы используем Alembic.
Если вы изменили модели в коде (добавил колонку или таблицу), создай новую миграцию:
bash
`docker-compose exec web alembic revision --autogenerate -m "название_изменения"`

Применить миграции к базе (накатить изменения):
bash
`docker-compose exec web alembic upgrade head`

Если база уже создана вручную, пометь её как актуальную:
bash
`docker-compose exec web alembic stamp head`

#ДОПОЛНИТЕЛЬНО:

Данные создаются автоматом
Документацию сильно не делал НАРОЧНО!

