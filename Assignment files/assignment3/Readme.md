# Assignment 3

In this assignment, two containers on two instances access their databases named 'test' to function with the users and rides APIs. 


## Pre-build

We use mysql server.

On each container:

sudo docker exec -it sudo service mysql start
sudo docker exec -it /bin/bash


mysql -u root
create database test
use test
{ Create tables as per specifications in user.sql and rides.sql }
create user 'aarya'@'localhost' identified by 'aarya123'
grant all privileges on *.* to 'aarya'@'localhost'
flush privileges
quit

## Build

sudo docker-compose up (on each instance)
