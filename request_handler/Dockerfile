FROM python:3.10.6
WORKDIR /home
COPY *.txt ./
COPY *.py ./
RUN pip3 install -U -r requirements.txt
ENTRYPOINT [ "python3", "main.py" ]