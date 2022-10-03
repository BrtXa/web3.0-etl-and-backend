# syntax=docker/dockerfile:1

FROM python:3.9.14-slim-buster

WORKDIR /web3.0_and_elt

COPY requirements.txt requirements.txt

RUN apt-get -qq update \
    && apt-get install -y --no-install-recommends \
    wget
RUN apt-get update --fix-missing && \
    apt-get upgrade -y && \
    apt-get install -y zip unzip build-essential libsnappy-dev zlib1g-dev libbz2-dev \
    libgflags-dev liblz4-dev libzstd-dev \
    librocksdb-dev

RUN pip3 install -r requirements.txt

COPY . .

CMD python3 run_api.py