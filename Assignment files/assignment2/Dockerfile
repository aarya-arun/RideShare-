FROM ubuntu:latest

RUN apt-get update && apt-get -y upgrade && apt-get install -y wget sudo gnupg gnupg2 gnupg1 net-tools
RUN apt-get install -y python3-pip && pip3 install flask 
RUN apt-get install -y python-pip && pip install flask
RUN pip install -U setuptools
RUN sudo pip3 install python-language-server
RUN sudo pip3 install --upgrade pip setuptools wheel
RUN echo Y| sudo apt-get install mysql-server
RUN echo Y| sudo apt-get install python3.6-dev libmysqlclient-dev
RUN pip install mysql-connector-python
RUN sudo pip2 install flask-mysqldb
RUN pip3 install mysqlclient
RUN sudo apt-get install python
RUN pip install setuptools
RUN sudo pip2 install requests
RUN mkdir /data && mkdir /data/db

EXPOSE 5000
