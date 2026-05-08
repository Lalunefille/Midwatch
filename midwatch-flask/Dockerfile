FROM docker.arvancloud.ir/python:3.11-slim

WORKDIR /app

COPY midwatch-flask/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY midwatch-flask/ .

EXPOSE 5000

CMD ["python", "app.py"]