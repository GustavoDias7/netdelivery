FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y locales \
    && sed -i 's/# pt_BR.UTF-8 UTF-8/pt_BR.UTF-8 UTF-8/' /etc/locale.gen \
    && locale-gen

RUN apt-get install -y nodejs npm
RUN npm install -g yarn

ENV LANG=pt_BR.UTF-8
ENV LC_ALL=pt_BR.UTF-8

COPY requirements.txt .
COPY package.json .

RUN pip install -r requirements.txt
RUN yarn install

COPY . .
