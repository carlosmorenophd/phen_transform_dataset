FROM python:3.12-slim-bookworm

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src src/

COPY tasks.py .

COPY test_task.py .

COPY run.sh .

RUN chmod +x run.sh

ENTRYPOINT sh ./run.sh

