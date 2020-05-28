FROM ubuntu:latest

RUN apt-get update && apt-get -y upgrade && apt-get install -y wget sudo gnupg gnupg2 gnupg1 net-tools
RUN apt-get install -y python3-pip && pip3 install flask
RUN pip3 install -U setuptools
RUN sudo easy_install pip
RUN sudo pip3 install python-language-server
RUN pip install flask-mysql
RUN sudo pip3 install --upgrade pip setuptools wheel
RUN echo Y| sudo apt-get install libmysqlclient-dev
RUN echo Y| sudo apt-get install mysql-server
RUN pip3 install mysql-connector-python
RUN sudo pip3 install flask-mysqldb
RUN pip install mysqlclient
RUN pip install setuptools
RUN echo Y| sudo apt-get install python3
RUN sudo pip install requests
RUN mkdir /data && mkdir /data/db

EXPOSE 5000
