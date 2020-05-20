# Assignment 1

In this assignment, a single python application file accesses a single database named 'test' to function with the users and rides APIs. 


## Pre-build

We use mysql server.

sudo service mysql start


mysql -u root
create database test
use test
{ Create tables as per specifications in user.sql and rides.sql }
create user 'aarya'@'localhost' identified by 'aarya123'
grant all privileges on *.* to 'aarya'@'localhost'
flush privileges
quit

## Build

sudo python CC_0009_0795_run.py


## Testing

Postman is used to query the application
