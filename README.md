Директория /frontend добавлена под фронт.
В директории /services находится backend микросервисов.
В /services/shared_schemas DTO для фронта и работы микросервисов в целом.
Запуск из корня проекта с помощью docker-compose.yml. 
В каждом приложении свой Dockerfile который его запускает и устанавливает requirements.


Что уже работает:

Сотрудники — список, карточка, фильтры по отделу/городу, пагинация.
Отделы — справочник и связи с сотрудниками.
Обучение/явка — фиксация посещаемости и начислений баллов.
Статистика — агрегаты по явке и баллам, чтобы сразу видеть динамику.
Безопасность: интеграция с Keycloak — сервисы принимают JWT, включён RBAC по ролям админ/наблюдатель/участник.
Валидации: проверка форматов (email, даты) и бизнес-правило по «лавке» — списание баллов ≥ 0.
Инфраструктура: health-checks, миграции через Alembic — всё готово для CI/CD и подключения фронта.

### API всех сервисов:

Auth (порт 8011):

    POST /auth/login — логин по корпоративной почте/паролю (Keycloak Direct Access Grants).
    POST /auth/refresh — обновить access по refresh.
    POST /auth/forgot-password — отправить ссылку на сброс пароля на корпоративную почту.
    POST /auth/logout — выход из учетной записи.

Admin (порт 8000):

    GET /api/users/me/roles — вернуть роли текущего пользователя и «эффективную» роль (с учётом X-Act-As).
    CRUD /users отсутствует — аккаунты создаёт/меняет только Keycloak.

Employees (порт 8012):

    GET /api/employees_info — список с фильтрами и пагинацией.
    GET /api/employees_info/{id} — карточка.
    POST /api/employees_info — создать (только admin).
    PATCH /api/employees_info/{id} — частичное обновление (admin/observer).
    DELETE /api/employees_info/{id} — удалить (admin).

Departments (порт 8013):

    GET /api/departments (+ фильтры), 
    GET /api/departments/{id}, POST, PATCH, DELETE.

Observers (порт 8014):

    GET /api/observers — список.
    GET /api/observers/{id}, POST, PATCH, DELETE.

Trainings (порт 8015):

    GET /api/trainings/{employee_id}/{year} — «снимок года» по сотруднику.
    PUT /api/trainings/{employee_id}/{year} — upsert этого снимка (части полей не реализованы в MVP; модель хранит агрегаты: mentee_number, mentee_points, conference_presence, certification, introductory_conf_points).

Statistics (порт 8016):

    GET /api/statistics — сводка по году: counts/rates/суммы.
    GET /api/statistics/top?metric=points_sum|points_efficiency|points_proactive&limit=10 — топ.
    GET /api/statistics/{employee_id}?year=YYYY — ранги и баллы сотрудника.
    GET /api/statistics/demographics?year=YYYY — возрастные группы, города.

### Подсказки по разработке:

### docker

Одновременная сборка и запуск контейнера:
```bash
docker compose up --build app
```

Пересборка и перезапуск одновременно (флаг '-d' указывает на фоновый режим контейнера):
```bash
docker compose up --build -d
```

Логи приложений docker compose
```bash
docker compose logs -f  # можно добавить имя приложения для более конкретных логов
```

Остановка и удаление запущенных контейнеров docker-compose:
```bash
docker compose down -v
```

Просмотр запущенных контейнеров (с флагом '-a' покажет все существующие):
```bash
docker ps
```

Перезапуск контейнера:
```bash
docker restart <container_id>
```

Остановить контейнер:
```bash
docker stop <container_id>
```

Логи и диагностика контейнера:
```bash
docker logs <container_id>
```


### Миграции


Требования:
- контейнеры подняты: `docker compose up -d`
- в `docker-compose.yml` прописаны `PYTHONPATH=/app`, `ALEMBIC_CONFIG=/app/alembic.ini` и volume: - `.:/app`

Сгенерировать миграцию
```bash
docker compose exec admin_service alembic revision --autogenerate -m "комментарий"
```
Применить миграции
```bash
docker compose exec admin_service alembic upgrade head
```
