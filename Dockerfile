FROM tensorflow/tensorflow:latest-gpu

WORKDIR /usr/src/app

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

RUN apt-get update && apt-get install -y openjdk-11-jdk
    
COPY requirements.txt .
RUN pip install -r requirements.txt
