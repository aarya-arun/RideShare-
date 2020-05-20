import flask
from flask import Flask, render_template, request, redirect, jsonify
from flask_mysqldb import MySQL
import requests
app = Flask(__name__)
#from flask_api import status
import datetime


app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] =  'aarya'
app.config['MYSQL_PASSWORD'] = 'aarya123'
app.config['MYSQL_DB'] = 'test'

mysql = MySQL(app)

app.config["DEBUG"] = True



rideidstart=10000
p=0
argg="LOL"
argnum=0


# ADD A NEW USER, API=1
@app.route('/api/v1/users', methods=['PUT'])
def api_addnewuser():
    if flask.request.method == 'POST':
        return "Method not allowed!",405
    
    if(len(request.json.get('password'))!=40):
        return "Bad password! Please enter a new one.",400

    for letter in request.json.get('password'):
        if(letter not in {'a','b','c','d','e','f','A','B','C','D','E','F','0','1','2','3','4','5','6','7','8','9'}):
            return "Bad password! Please enter a new one.",400
    
    global argnum
    argnum=argnum+1   
    global p
    p=1
    results={
        "message":"SELECT *  FROM users where username='"+request.json.get('username')+"'"
    }
    harry_potter = requests.post('http://3.94.149.243/api/v1/db/read', data = results, verify=True)
    ginny=harry_potter.json()
   
    if(ginny!=None):
        return "This user already exists!",400


    username = request.json.get('username')
    password = request.json.get('password')

    results={

        "message":"INSERT INTO users(username, password) VALUES ('"+username+"','"+password+"')"


    }
    
    harry_potter = requests.post('http://3.94.149.243/api/v1/db/write', data = results, verify=True)

    results1={}
    

    return jsonify(results1), 201
    







# DELETE A USER, API=2
@app.route('/api/v1/users/<usn>', methods=['DELETE'])
def api_deluser(usn):
    global argnum
    argnum=argnum+1 
    if flask.request.method == 'POST':
        return "Method not allowed!",405
   
    #write api
    global p
    p=2
    global argg
    argg=usn
    
    j=argg

    requests={

        "message":"SELECT *  FROM users where username='"+j+"'"
    }

    harry_potter = requests.post('http://3.94.149.243/api/v1/db/read', data = results)
    ginny=harry_potter.json()
  
    if(ginny==None):
        return "This user doesn't exit. Can't delete.",400


    
    j=argg

    results={

        "message":"DELETE FROM users WHERE username='"+j+"'" 
    }
    harry_potter = requests.post('http://3.94.149.243/api/v1/db/write', data = results)
    
    return jsonify(results), 200
        
    




# LIST ALL USERS, API=10
@app.route('/api/v1/users', methods=['GET'])
def api_listall():
    global argnum
    argnum=argnum+1

    global p
    p=10
    results={

        'message':"SELECT username FROM users"
    }
    
    harry_potter = requests.post('http://3.94.149.243/api/v1/db/read', json = results)
    
    print(harry_potter)

    if(harry_potter==None):return 204
    #for row1 in ginny:
    #    res.append(row1[0])

    return harry_potter,200


# CLEAR DB, API=11
@app.route('/api/v1/db/clear', methods=['POST'])
def api_cleardb():

    global p
    p=11
    global argnum
    argnum = argnum + 1
    results={

        "message":"DELETE FROM users"
    }
    harry_potter = requests.post('http://3.94.149.243/api/v1/db/write', data = results)

    results1={}
    
    return jsonify(results1), 200


# NUMBER OF REQUESTS, API=12
@app.route('/api/v1/_count', methods=['GET'])
def api_reqno():
   global argnum
   argnum=argnum+0
   resp=[]
   resp.append(argnum)

   return jsonify(resp),200


# DEL NUMBER OF REQUESTS, API=13
@app.route('/api/v1/_count', methods=['DELETE'])
def api_delreqno():
   global argnum
   argnum=0
   resp={}

   return jsonify(resp),200


        

    
    

    

            
app.run(host='0.0.0.0', port=80)
