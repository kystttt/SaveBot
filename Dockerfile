FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

ENV BOT_TOKEN=${BOT_TOKEN}
ENV APP_URL=${APP_URL}
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]