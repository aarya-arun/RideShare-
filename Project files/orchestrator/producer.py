
import flask
from flask import Flask, render_template, request, redirect, jsonify
from flask_mysqldb import MySQL
import requests
app = Flask(__name__)
import datetime
import pika
import sys
import random

import logging
import threading

import docker
import math
from multiprocessing import Process

from kazoo.client import KazooClient
from kazoo.client import KazooState

from kazoo.protocol.states import EventType
from kazoo.exceptions import NodeExistsError

logging.basicConfig()

app.config["DEBUG"] = True

import uuid

argnum = 0
   


zk = KazooClient(hosts='zookeeper:2181')
zk.start()
zk.ensure_path("/consumer")

slaveint=random.randint(0,20000)
path1='/consumer/slave_'+str(slaveint)

#########################

def watch_children(event):
    client.containers.run("ubuntu_slave","python slave.py",links={"rmq":"rmq","zoo":"zoo","master":"master"},volumes_from=['master'],network='ubuntu_default',detach=True)
    


#########################

connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='rmq', heartbeat = 275))
channel = connection.channel()

corr_id = str(uuid.uuid4())

peso=channel.queue_declare(queue='', exclusive=True)

callback_queue = peso.method.queue
response = None

channel.queue_declare(queue='readQ',durable=True) 
channel.queue_declare(queue='writeQ',durable=True) 

def on_response(ch, method, props, body):
    global response
    if corr_id == props.correlation_id:
        response = body
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue=callback_queue, on_message_callback=on_response)
channel.exchange_declare(exchange='logs', exchange_type='fanout')

###########################################################################

client = docker.from_env()
check = 0   

def zoo_main_func(): 

    #Autoscaling requirements 
    global argnum
    req_ratio = argnum/20
    if req_ratio==0:
        slaves_req=1
    else:
        slaves_req = math.ceil(req_ratio)
    num_of_slaves=0
    num_of_masters=0
    
    

    for container in client.containers.list():
        if(container.attrs['Config']['Image']=='ubuntu_slave'):
            num_of_slaves+=1
        if(container.attrs['Config']['Image']=='ubuntu_master'):
            num_of_masters+=1
    

    #Implementing autoscaling whrn master is up
    if(num_of_masters==1):
        if(num_of_slaves < slaves_req):
            diff = slaves_req - num_of_slaves
            for i in range(diff):
                client.containers.run("ubuntu_slave","python3 consumer.py",links={"rmq":"rmq"},volumes_from=['master'],network='ubuntu_default',detach=True)
        else:
            diff = num_of_slaves - slaves_req
            slaves_list=[]
            for container in client.containers.list():
                if(container.attrs['Config']['Image']=='ubuntu_slave'):
                    slaves_list.append(container.id)
            for i in range(diff):
                container=client.containers.get(slaves_list[i])
                container.stop(timeout=1)
                container.remove(v=True)

    #argnum = 0
    threading.Timer(120, zoo_main_func).start()
   
    
    

       


#########################################################################


@app.route('/ping', methods=['GET'])
def pingpong():
    return 'pong!'

@app.route('/testamundo', methods=['GET'])
def alexthelion():
    global argnum
    p = argnum
    l = []
    l.append(p)
    return jsonify(l)


@app.route('/api/v1/db/read', methods=['POST'])
def readfromdb():
    global argnum
    argnum = argnum + 1
    zoo_main_func()
    voldemort = request.get_json()
    message= voldemort['message']
    channel.basic_publish( exchange='', routing_key='readQ', properties=pika.BasicProperties(reply_to=callback_queue, correlation_id=corr_id,),body=message) 
    while True:
        dua = ''
        global response
        if response is None:
            connection.process_data_events()
            continue
        else:
            lipa = response.decode("UTF-8")
            dua = lipa
            break
    response = None
    return str(lipa)



@app.route('/api/v1/db/write', methods=['POST'])
def writetodb():
    voldemort = request.get_json()
    message= voldemort['message']
    channel.basic_publish(exchange='', routing_key='writeQ', body=message)
    return 'lol'



@app.route('/api/v1/worker/list',methods=['GET'])
def worker_listing():
    client1 = docker.APIClient()
    sirius = client1.inspect_container('ubuntu_rmq_1')
    list_of_containers = []
    for container in client.containers.list():
        if(container.attrs['Config']['Image']=='ubuntu_slave'):
            list_of_containers.append(container.id)
    pid_list = []
    for i in list_of_containers:
        sirius = client1.inspect_container(i)
        regulus = sirius['State']['Pid']
        pid_list.append(int(regulus))
    pid_list.sort()
    return jsonify(pid_list)



@app.route('/api/v1/crash/slave',methods=['POST'])
def crash_slave():
    client1 = docker.APIClient()
    sirius = client1.inspect_container('ubuntu_rmq_1')
    list_of_containers = []  
    pid_list=[]
    for container in client.containers.list():
        if(container.attrs['Config']['Image']=='ubuntu_slave'):
            list_of_containers.append(container.id)
    max_pid=0
    max_container_id=0

    for i in list_of_containers:
        sirius = client1.inspect_container(i)
        regulus = sirius['State']['Pid']
        if(int(regulus)>max_pid):
            max_pid=int(regulus)
            max_container_id=i
    #print(client.containers.list())
    #return str(client.containers.list()[max_container_id])
    #container = client.containers.list()[max_container_id]
    container=client.containers.get(max_container_id)
    container.stop(timeout=1)
    container.remove(v=True)
    
    children = zk.get_children("/consumer/", watch=watch_children)
    pid_list.append(max_pid)
    return jsonify(pid_list)
    
    
    
    
    #global response
    #response = None
    #global corr_id
    #corr_id = str(uuid.uuid4())
    #channel.basic_publish(
    #    exchange='',
    #    routing_key='writeQ',
    #    body=message,
    #    properties=pika.BasicProperties(
    #        delivery_mode=2,
    #        reply_to='responseQ',
    #            correlation_id=corr_id  # make message persistent
    #    ))
    #print(message)
    #channel.basic_consume(queue = 'responseQ', on_message_callback=on_response, auto_ack= True)
    #while response is None:
    #    connection.process_data_events()
    #print(response)
    #return response



app.run(host='0.0.0.0', port=80)
