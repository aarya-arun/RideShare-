
import flask
from flask import Flask, render_template, request, redirect, jsonify
from flask_mysqldb import MySQL
import requests
app = Flask(__name__)
import datetime
import pika
import sys

global corr_id
global response

app.config["DEBUG"] = True

import uuid

connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='rmq'))
channel = connection.channel()

channel.queue_declare(queue='readQ', durable=True)
channel.queue_declare(queue='writeQ', durable=True)
channel.queue_declare(queue='responseQ', durable=True)


def on_response(ch, method, props, body):
    global corr_id
    print(type(body))
    return body
    if corr_id == props.correlation_id:
        return body




#channel.basic_consume(queue = 'responseQ', on_message_callback=on_response, auto_ack= True)





@app.route('/ping', methods=['GET'])
def pingpong():
    return 'pong!'

@app.route('/api/v1/db/read', methods=['POST'])
def readfromdb():
    print("Why this kolaveri di")
    return "CC sucks and I hate MT"
    #message= request.json
    #global response
    #response = None
    #global corr_id
    #corr_id = str(uuid.uuid4())
    #channel.basic_publish(
    #exchange='',
    #routing_key='readQ',
    #body=message['message'],
    #properties=pika.BasicProperties(
    #delivery_mode=2,
    #reply_to='responseQ',
    #            correlation_id=corr_id  # make message persistent
    #    ))
    #print("CC sucks")
    #channel.basic_consume(queue = 'responseQ', on_message_callback=on_response, auto_ack= True)
    #while response is None:
    #    connection.process_data_events()
    #print (response.decode('ASCII'))
    #return response.decode('ASCII')

    




@app.route('/api/v1/db/write', methods=['POST'])
def writetodb():
    message= request.json.get('message')
    global response
    response = None
    global corr_id
    corr_id = str(uuid.uuid4())
    channel.basic_publish(
        exchange='',
        routing_key='writeQ',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,
            reply_to='responseQ',
                correlation_id=corr_id  # make message persistent
        ))
    print(message)
    channel.basic_consume(queue = 'responseQ', on_message_callback=on_response, auto_ack= True)
    while response is None:
        connection.process_data_events()
    print(response)
    return response



app.run(host='0.0.0.0', port=80)