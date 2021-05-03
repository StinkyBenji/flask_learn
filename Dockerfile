FROM python:3.9-slim-buster
RUN apt-get update && apt-get -y dist-upgrade
RUN apt-get -y install gcc python3-dev
RUN apt install -y netcat

RUN pip3 install --upgrade pip

WORKDIR /io-trace

COPY . /io-trace

RUN pip3 --no-cache-dir install -r requirements.txt

EXPOSE 5000
