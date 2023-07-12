FROM python:3.11
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app/static
WORKDIR /app/staticfiles
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY run.sh .

COPY . .

EXPOSE 8000
