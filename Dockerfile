FROM python:3.8-slim-buster

WORKDIR /python-docker

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .
# COPY ./crypto ./crypto
# COPY ./tests ./tests


CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]