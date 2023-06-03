FROM python:3.12.0a7-alpine3.16
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN addgroup app && adduser -S -G app app
USER app
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py makemigrations
RUN rm db.sqlite3
RUN python manage.py migrate
