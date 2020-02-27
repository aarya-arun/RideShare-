import flask
from flask import Flask, render_template, request, redirect, jsonify
from flask_mysqldb import MySQL
app = Flask(__name__)
#from flask_api import status
import datetime


app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] =  'indu'
app.config['MYSQL_PASSWORD'] = 'indu123'
app.config['MYSQL_DB'] = 'test'

mysql = MySQL(app)

app.config["DEBUG"] = True



rideidstart=10000
p=0
argg="LOL"
argnum=0


# ADD A NEW USER, API=1
@app.route('/api/v1/users', methods=['PUT', 'POST'])
def api_addnewuser():
    if flask.request.method == 'POST':
        return "Method not allowed!",405
    
    if(len(request.json.get('password'))!=40):
        return "Bad password! Please enter a new one.",400

    for letter in request.json.get('password'):
        if(letter not in {'a','b','c','d','e','f','A','B','C','D','E','F','0','1','2','3','4','5','6','7','8','9'}):
            return "Bad password! Please enter a new one.",400
    
    
    global p
    p=1
    return redirect(flask.url_for('readfromdb'), code=307)




# DELETE A USER, API=2
@app.route('/api/v1/users/<usn>', methods=['DELETE', 'POST'])
def api_deluser(usn):
    if flask.request.method == 'POST':
        return "Method not allowed!",405
    global p
    p=2
    global argg
    argg=usn
    print(type(argg))
    return redirect(flask.url_for('readfromdb'), code=307)


# LIST ALL USERS, API=10
@app.route('/api/v1/users', methods=['GET'])
def api_listall():
    
    global p
    p=10
    return redirect(flask.url_for('readfromdb'), code=307)


#WRITE TO A DB, API=8

@app.route('/api/v1/db/write', methods=['POST', 'PUT', 'DELETE', 'GET'])
def writetodb():
    results=[]
    global p
    if p==1:
        username = request.json.get('username')
        password = request.json.get('password')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()
        cur.close()
        results=[]
        return jsonify(results), 201
        
    if p==2:
        cur = mysql.connection.cursor()
        j=argg
        cur.execute("DELETE FROM users WHERE username='"+j+"'" )
        mysql.connection.commit()
        cur.close()
        return jsonify(results), 200
  





@app.route('/api/v1/db/read', methods=['POST', 'PUT', 'DELETE', 'GET'])
def readfromdb():
    result=[]
    if p==1:
        cur = mysql.connection.cursor()
        cur.execute("SELECT *  FROM users where username='"+request.json.get('username')+"'")
        row = cur.fetchone()
        if(row!=None):
            return "This user already exists!",400
        
        else:
            return redirect(flask.url_for('writetodb'), code=307)

    if p==2:
        cur = mysql.connection.cursor()
        j=argg
        cur.execute("SELECT *  FROM users where username='"+j+"'")
        row = cur.fetchone()
        if(row==None):
            return "This user doesn't exit. Can't delete.",400
        
        else:
            return redirect(flask.url_for('writetodb'), code=307)
    
    if p==10:
        cur=mysql.connection.cursor()
        cur.execute("SELECT username FROM users")
        res=[]
        if(cur==None):return 204
        for row1 in cur:
            res.append(row1[0])

        return jsonify(res),200

    

            
app.run(host='0.0.0.0', port=80)