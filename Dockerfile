FROM python:3.10

RUN apt-get update 
RUN apt-get install gdb -y


WORKDIR /attack
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY src src
COPY attack .

ENTRYPOINT ["/attack/entrypoint.sh"]
