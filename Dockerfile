FROM python:3.10-alpine

WORKDIR /app

COPY . .

COPY .env.docker .env

RUN rm .env.docker

RUN pip install -r requirements.txt

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8888"]