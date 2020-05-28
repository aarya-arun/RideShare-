FROM ubuntu:latest

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && apt-get -y upgrade && apt-get install -y wget sudo gnupg gnupg2 gnupg1 net-tools
RUN sudo apt-get install python3.7
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
#RUN pip install pika
RUN pip install ipython
RUN pip3 install kazoo
RUN pip3 install pika --upgrade
RUN pip3 install docker
RUN pip3 install schedule
RUN sudo apt-get install python3-pika



RUN mkdir /code
#COPY ./requirements.txt /code/requirements.txt
#RUN pip3 install -r /code/requirements.txt
COPY . /code
WORKDIR /code
