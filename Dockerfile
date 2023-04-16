FROM python:3.10.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8080

ENTRYPOINT ["sh","start.sh" ]