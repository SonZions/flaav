# syntax=docker/dockerfile:1

FROM ubuntu

WORKDIR /app

COPY requirements.txt .

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y python3-pip \
                                         g++ \
                                         gcc \
                                         libxml2-dev \
                                         libxslt-dev \
                                         python3-dev \
                                         libffi-dev \
                                         make \
               && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install -r requirements.txt 

COPY CalDav-Urlaub.py .

CMD ["python3", "CalDav-Urlaub.py"]
 
