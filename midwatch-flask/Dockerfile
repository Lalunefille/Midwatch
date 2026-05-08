FROM docker.arvancloud.ir/python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

WORKDIR /app/app

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]