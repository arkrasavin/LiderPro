## LiderPro — Swagger/OpenAPI

    Этот репозиторий ведёт документацию API по микросервисам **как YAML-файлы** рядом с кодом.
    Все сервисы используют **общие компоненты** (`shared_openapi/components.yaml`).

## Структура

    shared_openapi/components.yaml - общие схемы/ошибки/безопасность
    services/*/docs/openapi.yaml - спецификации каждого сервиса
    gateway/openapi.yaml - агрегат (генерится скриптом)
    scripts/merge_openapi.py - скрипт слияния
