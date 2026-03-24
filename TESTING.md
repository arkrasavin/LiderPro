# TESTING.md

## Цель:
 Автоматизированные проверки API для ключевых сервисов.

Текущее покрытие:

- `auth_service`:
  - successful login
  - invalid credentials
  - refresh token
  - logout
  - forgot-password for unknown email
- `employees_service`
  - list employees as admin
  - list employees as observer
  - list employees as participant -> 403
  - get employee not found -> 404
  - create employee as admin -> 201
  - invalid email -> 422
  - delete employee as observer -> 403

Запуск тестов:
```bash
docker compose build auth_service employees_service
docker compose run --rm auth_service pytest tests -q
docker compose run --rm employees_service pytest tests -q
```