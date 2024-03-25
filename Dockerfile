FROM public.ecr.aws/lambda/provided:al2023

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}
COPY pytensor_caller_config ${LAMBDA_TASK_ROOT}/caller_rc
COPY lambda_function.py ${LAMBDA_TASK_ROOT}


# Update image
RUN dnf install -y g++ python3.11 python3.11-pip python3.11-devel

# Install the specified packages
RUN python3.11 -m pip install -r requirements.txt

# Precompile function code
#COPY pytensor_build_config ${LAMBDA_TASK_ROOT}/build_rc
#ENV PYTENSORRC=build_rc
#COPY precompile.py ${LAMBDA_TASK_ROOT}
#RUN python3.11 precompile.py
## chmod the precompile directory so lambda can access it
## WARNING: WSL will override this chmod if /etc/wsl.conf isn't configured
#RUN chmod -R 755 ${LAMBDA_TASK_ROOT}/pytensor

ENTRYPOINT PYTENSORRC=caller_rc python3.11 -m awslambdaric lambda_function.handler
