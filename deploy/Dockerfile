FROM python:3.12-slim AS builder

WORKDIR /app

RUN pip install torch transformers # this is heavy
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "manage.py"]
