#!/usr/bin/env python

import flask
from flask import Flask, render_template, request, redirect, jsonify
from flask_mysqldb import MySQL
import requests
app = Flask(__name__)
#from flask_api import status
import datetime
import pika
import time
import sys
import sqlite3


import random

import logging

from kazoo.client import KazooClient
from kazoo.client import KazooState

from kazoo.protocol.states import EventType
from kazoo.exceptions import NodeExistsError



logging.basicConfig()


app.config["DEBUG"] = True


zk = KazooClient(hosts='zookeeper:2181')
zk.start()
zk.ensure_path("/consumer")

slaveint=random.randint(0,20000)
path1='/consumer/slave_'+str(slaveint)


if zk.exists(path=path1):
    pass
else:
    zk.create(path=path1, value=b'LOTR',ephemeral=True)




connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rmq'))
channel = connection.channel()

channel.queue_declare(queue='readQ', durable=True)
channel.queue_declare(queue='responseQ', durable=True)
channel.exchange_declare(exchange='logs', exchange_type='fanout')
print(' [*] Waiting for messages.')


def callback(ch, method, properties, body):
    with app.app_context():
        conn = sqlite3.connect('./pythondatabase.db')
        c = conn.cursor()
        c.execute(body.decode('ASCII'))
        print('Hello from slave')
        ron=c.fetchall()
        conn.commit()
    ch.basic_publish(exchange='', routing_key=properties.reply_to, properties=pika.BasicProperties(correlation_id = properties.correlation_id), body=str(ron))
    ch.basic_ack(delivery_tag=method.delivery_tag)
    




channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='readQ', on_message_callback=callback)


channel.start_consuming()

app.run(host='0.0.0.0', port=8090)