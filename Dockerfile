FROM python:3.9.18-bullseye

WORKDIR /app

COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

RUN apt-get update
COPY app/ .




CMD ["python", "-u",  "main.py"]