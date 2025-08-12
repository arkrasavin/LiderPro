Директория /frontend добавлена под фронт.
В директории /services находится backend микросервисов.
В /services/shared_schemas DTO для фронта и работы микросервисов в целом.

Сервисы auth и admin готовы к тестированию endpoints. 
Запуск из корня проекта с помощью docker-compose.yml. 
В каждом приложении свой Dockerfile который его запускает и устанавливает requirements.


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
