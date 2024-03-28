FROM ubuntu:latest
# Debian or Alpine don't seem to work with pymc

WORKDIR /usr/src/app

ARG FLASK_RUN_PORT=4000

ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=$FLASK_RUN_PORT

COPY requirements.txt requirements.txt
COPY ./app ./app

# Install g++, python and pip
RUN apt-get update && \
    apt-get install -y g++ python3 python3-pip

# Install the specified packages
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

CMD ["flask", "run"]
