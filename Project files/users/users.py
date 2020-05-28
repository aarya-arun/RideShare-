
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

@app.route('/ping', methods=['GET'])
def pingpang():
	return 'pong!'

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
    harry_potter = requests.post('http://50.19.83.179/api/v1/db/read',json = results)
    
    ginny = harry_potter.text

    ginny = ginny.strip("[")
    ginny = ginny.strip("]")
    ginny = ginny.split(",")

    seamus =[]

    for name in ginny:
        name = name.strip()
        name = name.strip("(")
        name = name.strip("'")
        seamus.append(name)



    username = request.json.get('username')
    password = request.json.get('password')

    if(seamus[0]==username):
        return "This user already exists!",400


    results={

        "message":"INSERT INTO users(username, password) VALUES ('"+username+"','"+password+"')"


    }
    
    harry_potter = requests.post('http://50.19.83.179/api/v1/db/write',json = results)

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

    results={

        "message":"SELECT *  FROM users where username='"+j+"'"
    }
    harry_potter = requests.post('http://50.19.83.179/api/v1/db/read',json = results)
    
    ginny = harry_potter.text

    ginny = ginny.strip("[")
    ginny = ginny.strip("]")
    ginny = ginny.split(",")

    seamus =[]

    for name in ginny:
        name = name.strip()
        name = name.strip("(")
        name = name.strip("'")
        seamus.append(name)



    username = request.json.get('username')
    password = request.json.get('password')

    if(seamus[0]!=username):
        return "This user doesn't exist!",400
    
    j=argg

    results={

        "message":"DELETE FROM users WHERE username='"+j+"'" 
    }
    harry_potter = requests.post('http://50.19.83.179/api/v1/db/write',json = results)
    
    return jsonify({}), 200
        
    




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
    harry_potter = requests.post('http://50.19.83.179/api/v1/db/read', json = results)
    ginny = harry_potter.text
    if ginny == "[]":
        return jsonify([])
    ginny = ginny.strip("[")
    ginny = ginny.strip("]")
    ginny = ginny.strip()
    cedric = []
    ginny = ginny.split(",")
    #return jsonify(ginny)
    for name in ginny:
        if name == ')':
            continue
        else:
            name = name.strip()
            name = name.strip("(")
            name = name.strip("'")
            name = name.strip(",")
            cedric.append(name)
    
    if len(cedric) == 0:
        return 204
    return jsonify(cedric), 200


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
    harry_potter = requests.post('http://50.19.83.179/api/v1/db/read', json = results)

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
