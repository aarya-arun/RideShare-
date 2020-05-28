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





app.config["DEBUG"] = True





connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rmq'))
channel = connection.channel()

channel.queue_declare(queue='writeQ', durable=True)
channel.queue_declare(queue='responseQ', durable=True)
channel.exchange_declare(exchange='logs', exchange_type='fanout')
print(' [*] Waiting for messages.')


def callback(ch, method, properties, body):
    with app.app_context():
        conn = sqlite3.connect('./pythondatabase.db')
        c = conn.cursor()
        c.execute(body.decode('ASCII'))
        print('Hello from master')
        ron=c.fetchall()
        print(ron)
        conn.commit()

    ch.basic_ack(delivery_tag=method.delivery_tag)
    
    




channel.basic_consume(queue='writeQ', on_message_callback=callback)
channel.basic_qos(prefetch_count=1)
try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
connection.close()



channel.start_consuming()

app.run(host='0.0.0.0', port=8070)