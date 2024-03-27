# Debian, Alpine, etc don't seem to work with pymc
FROM ubuntu:latest

WORKDIR /usr/src/app

ENV FLASK_APP=rating_service
ENV FLASK_RUN_HOST=0.0.0.0
ENV PORT=4000

COPY requirements.txt requirements.txt
#COPY ./src ./src
COPY ./rating_service ./rating_service

# Install g++, python and pip
RUN apt-get update && \
    apt-get install -y g++ python3 python3-pip

# Install the specified packages
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

#ENTRYPOINT [ "python3" ]
#CMD ["service.py"]
#CMD ["flask", "--app", "rating_service", "run", "-p", "$PORT"]
CMD ["flask", "run", "-p", "$PORT"]
