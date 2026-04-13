FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y portaudio19-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8002

CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn Bassinga.wsgi:application --bind 0.0.0.0:8002"]