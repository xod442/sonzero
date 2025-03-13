FROM python:3.12.0b1-buster
ENV http_proxy http://10.202.63.3:8080
ENV https_proxy http://10.202.63.3:8080
ENV no_proxy=localhost,127.0.0.1,10.250.201.0/24,10.250.202.0/24,10.250.203.0/24,10.250.204.0/24,10.250.205.0/24,10.250.206.0/24,10.250.207.0/24,10.250.208.0/24,10.250.209.0/24,,10.250.210.0/24,10.202.63.0/24
RUN apt-get update -y
RUN apt-get install -y nano

COPY requirements.txt /opt/
RUN pip3 install --proxy http://10.202.63.3:8080 -r /opt/requirements.txt

WORKDIR /opt
#COPY . .

ENV FLASK_APP=app
ENV FLASK_DEBUG=1
CMD  ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
