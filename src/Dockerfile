# Debian, Alpine, etc don't seem to work with pymc
FROM ubuntu:latest

WORKDIR /usr/src/app

#ENV FLASK_APP=service.py
#ENV FLASK_RUN_HOST=0.0.0.0
ENV PORT=4000

COPY requirements.txt requirements.txt
#COPY ./src ./src
COPY . .

# Install g++, python and pip
#RUN apk add --update gcc musl-dev linux-headers
#RUN apk add --update build-base python3 py3-pip
RUN apt-get update && \
    apt-get install -y g++ python3 python3-pip

# Install the specified packages
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

# Precompile function code
#COPY pytensor_build_config ${LAMBDA_TASK_ROOT}/build_rc
#ENV PYTENSORRC=build_rc
#COPY precompile.py ${LAMBDA_TASK_ROOT}
#RUN python3.11 precompile.py
## chmod the precompile directory so lambda can access it
## WARNING: WSL will override this chmod if /etc/wsl.conf isn't configured
#RUN chmod -R 755 ${LAMBDA_TASK_ROOT}/pytensor

ENTRYPOINT [ "python3" ]
CMD ["service.py"]
#CMD ["flask", "run"]
