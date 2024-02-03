FROM python:3.9.18-bookworm

WORKDIR /user/app

RUN apt-get update

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY app/ .

CMD ["python", "-u",  "main.py"]