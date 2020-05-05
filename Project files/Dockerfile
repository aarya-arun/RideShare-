FROM ubuntu:latest

RUN apt-get update && apt-get -y upgrade && apt-get install -y wget sudo gnupg gnupg2 gnupg1 net-tools
RUN apt-get install -y python3-pip && pip3 install flask 
RUN pip3 install -U setuptools
RUN sudo pip3 install python-language-server
RUN sudo pip3 install --upgrade pip setuptools wheel
RUN echo Y| sudo apt-get install mysql-server
RUN echo Y| sudo apt-get install libmysqlclient-dev
RUN pip3 install mysql-connector-python
RUN sudo pip3 install flask-mysqldb
RUN pip3 install mysqlclient
RUN echo Y | sudo apt-get install python
RUN pip3 install setuptools
RUN sudo pip3 install requests
RUN pip3 install pika
RUN mkdir /data && mkdir /data/db

