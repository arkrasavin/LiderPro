FROM python:3.12-slim

WORKDIR /app

COPY services/ewallet_service/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY services/ewallet_service/ /app/

COPY shared_schemas/ /app/shared_schemas

ENV PYTHONPATH=/app

CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port=8017", "--reload"]