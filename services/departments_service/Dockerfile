FROM python:3.12-slim

WORKDIR /app

COPY services/departments_service/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY services/departments_service /app/

COPY shared_schemas/ /app/shared_schemas/

ENV PYTHONPATH=/app

CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port=8013", "--reload"]