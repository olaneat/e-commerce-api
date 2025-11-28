FROM python:3.12

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["sh", "-c", "gunicorn commerce.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]
