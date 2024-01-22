FROM python:3.10

WORKDIR /usr/src/app

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

RUN apt-get update && apt-get install -y openjdk-17-jdk
    
COPY requirements.txt .
RUN pip install -r requirements.txt
