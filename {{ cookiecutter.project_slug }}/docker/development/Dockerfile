FROM python:3.8-slim

RUN apt update && apt install -y git netcat nodejs npm
RUN npm install npm@latest -g

EXPOSE 8000
WORKDIR /app
