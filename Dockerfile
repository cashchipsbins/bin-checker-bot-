FROM python:3.10-slim

RUN apt-get update && apt-get install -y gcc

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
