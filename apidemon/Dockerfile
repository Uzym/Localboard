FROM python:3.10.6
WORKDIR /app
COPY requirements.txt requirements.txt
RUN apt-get install --reinstall libpq-dev
RUN pip3 install -U pip
RUN pip3 install -U -r requirements.txt --use-pep517
COPY . /app
EXPOSE 8000
