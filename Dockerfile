FROM python:3.10-alpine

WORKDIR /app

COPY . .

COPY .env.docker .env

RUN rm .env.docker

RUN pip install -r requirements.txt

CMD ["python", "-u", "main.py"]