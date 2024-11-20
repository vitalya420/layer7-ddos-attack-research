FROM python:3.9-slim

WORKDIR /app

COPY app.py .
COPY gunicorn_config.py .

RUN pip install Flask gunicorn psutil orjson ujson simplejson

EXPOSE 8000

CMD ["gunicorn", "-c", "gunicorn_config.py", "app:app"]
