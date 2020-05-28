import flask
from flask import Flask, render_template, request, redirect, jsonify
from flask_mysqldb import MySQL
import requests
app = Flask(__name__)
import datetime


app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] =  'aarya'
app.config['MYSQL_PASSWORD'] = 'aarya123'
app.config['MYSQL_DB'] = 'test'

mysql = MySQL(app)

app.config["DEBUG"] = True


rideidstart = "9999"


p=0
argg="LOL"
argnum = 0
reqnum = 0

@app.route('/ping', methods=['GET'])
def pingpang():
	return 'pong!'


# ADD A NEW RIDE, API=3
@app.route('/api/v1/rides', methods=['POST'])
def api_addnewride():  
    #write api
    global reqnum
    reqnum = reqnum + 1
    acromantula=requests.get('http://LBW-171399600.us-east-1.elb.amazonaws.com/api/v1/users')
    aragog=acromantula.json()
        #return jsonify(aragog)
    flag=0
    for name in aragog:
        if name == request.json.get('created_by'):
            flag = 1
    if flag == 0:
        return "User doesn't exist. Join now to create a ride!",400

    

    created_by= request.json.get('created_by')
    timestamp=request.json.get('timestamp')
    source=request.json.get('source')
    destination=request.json.get('destination')
    global rideidstart
    
    p = int(rideidstart) + 1
    japan = str(p) 
        
    results={

            "message": "INSERT INTO rides(created_by, timestamp1, source1, destination1, rideid) VALUES ('"+created_by+"','"+timestamp+"','"+source+"','"+destination+"',"+japan+")"
        }

        
    harry_potter = requests.post('http://50.19.83.179/api/v1/db/read',json = results)
    
     

    results={

            "message": "INSERT INTO ride_users(rideid,userz) VALUES ("+japan+",'"+created_by+"')"
        }

         
    harry_potter = requests.post('http://50.19.83.179/api/v1/db/read',json = results)

    rideidstart = int(rideidstart) + 1
    rideidstart = str(rideidstart)

    
    results={}
    return jsonify(results), 201
    
  

















#RETURN ALL UPCOMING RIDES FOR A SOURCE AND DESTINATION API=4   DONEDONEDONE################_----------
@app.route('/api/v1/rides', methods=['GET'])
def api_sourceanddest():
    global reqnum
    reqnum = reqnum + 1
    
    if 'source' not in request.args:
        return "Error! Please provide a source.",400

    if 'destination' not in request.args:
        return "Error! Please provide a destination.",400

    global p
    p=4
    global a
    a=request.args.get('source')
    global b
    b=request.args.get('destination')
    results={

        "message": "SELECT *  FROM rides where source1='"+a+"' and destination1 = '"+b+"'"
    }

        
    vernon_dursley = requests.post('http://50.19.83.179/api/v1/db/read',json = results)
    petunia = vernon_dursley.text

    if petunia == "[]":
        return "This ride doesn't exist", 204
    
    

    petunia = petunia.strip("[")
    petunia = petunia.strip("]")

    petunia = petunia.split(", (")

    dudley = []

    for name in petunia:
        name = name.strip()
        name = name.strip("(")
        name = name.strip(")")
        name = name.split(",")
        paramaribo =[]
        for item in name:
            paramaribo.append(item)
        
        dudley.append(paramaribo)



    


    res =[]

    for rideone in dudley:


        calzone1 = rideone[4].strip()
        calzone2 = rideone[0].strip()
        calzone3 = rideone[1].strip()

        calzone1 = calzone1.strip("'")
        calzone2 = calzone2.strip("'")
        calzone3 = calzone3.strip("'")

        resp= {
            "rideId": calzone1,
            "username": calzone2,
            "timestamp": calzone3,
           }
        res.append(resp)
        
    return jsonify(res),200

   
   




































 #LIST ALL DETAILS OF A GIVEN RIDE API=5  DONEDONEDONEDE###########################
@app.route('/api/v1/rides/<id>', methods=['GET'])
def api_id(id):
    global reqnum
    reqnum = reqnum + 1

    if flask.request.method == 'POST':
        return "Method not allowed!", 405 
    
    
    global argnum
    argnum=id
    
    j=argnum

    results={

        "message": "SELECT *  FROM rides where rideid='"+j+"'"
    }

        
    vernon_dursley = requests.post('http://50.19.83.179/api/v1/db/read',json = results)
    petunia = vernon_dursley.text

    if petunia == "[]":
        return "This ride doesn't exist", 204


    petunia = petunia.strip("[")
    petunia = petunia.strip("]")
    petunia = petunia.strip("(")
    petunia = petunia.strip(")")
    petunia = petunia.split(",")

    dudley = []
    for name in petunia:
        name = name.strip()
        name = name.strip("'")
        name = name.strip(")")
        name = name.strip("'")
        dudley.append(name)

    
    

    results={

        "message":"SELECT userz FROM ride_users where rideid="+j
    }

    
    harry_potter = requests.post('http://50.19.83.179/api/v1/db/read',json = results)
    ginny = harry_potter.text
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
    
    


    

    resp={
            "rideId": dudley[4],
            "created_by": dudley[0],
            "timestamp": dudley[1],
            "source": dudley[2],
            "destination": dudley[3],
            "users": cedric
        }
        
    return jsonify(resp),200

    
     
    #Inc


















#JOIN A RIDE, API=6

@app.route('/api/v1/rides/<rideid>', methods=['POST'])
def api_joinride(rideid):
    global reqnum
    reqnum = reqnum + 1

    global p
    p=6
    global argnum
    argnum=rideid
    
    j=argnum

    results={

        "message": "SELECT *  FROM rides where rideid='"+j+"'"
    }

        
    vernon_dursley = requests.post('http://50.19.83.179/api/v1/db/read',json = results)
    petunia = vernon_dursley.text

    if petunia == "[]":
        return "This ride doesn't exist", 204




    petunia = petunia.strip("[")
    petunia = petunia.strip("]")
    petunia = petunia.strip("(")
    petunia = petunia.strip(")")
    petunia = petunia.split(",")

    dudley = []
    for name in petunia:
        name = name.strip()
        name = name.strip("'")
        name = name.strip(")")
        name = name.strip("'")
        dudley.append(name)

    


    acromantula=requests.get('http://LBW-171399600.us-east-1.elb.amazonaws.com/api/v1/users')
    aragog=acromantula.json()
    #return jsonify(aragog)
    flag=0
    for name in aragog:
        if name == request.json.get('username'):
            flag = 1
    if flag == 0:
        return "User doesn't exist. Join now to create a ride!",400

    results={

        "message":"SELECT userz FROM ride_users where rideid="+j
    }

    
    harry_potter = requests.post('http://50.19.83.179/api/v1/db/read',json = results)
    ginny = harry_potter.text
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

    for name in cedric:
     if request.json.get('username') == name:
        return "This user is already in the ride.",400

    
    j=argnum
    results={
            "message": "INSERT INTO ride_users(rideid,userz) VALUES ('"+j+"','"+request.json.get('username')+"')"
        }
     
    harry_potter = requests.post('http://50.19.83.179/api/v1/db/write',json = results)
    
        
    results={}
    return jsonify(results), 200

   
   #INCOMPLETO







# DELETE A RIDE, API=7
@app.route('/api/v1/rides/<rideid>', methods=['DELETE'])
def api_delride(rideid):
     
    global reqnum
    reqnum = reqnum + 1
    if flask.request.method == 'POST':
        return "Method not allowed!", 405 
    
    global p
    p=7
    global argg
    argg=rideid
    
    j=argg

    results={

        "message": "SELECT *  FROM rides where rideid='"+j+"'"
    }

        
    vernon_dursley = requests.post('http://50.19.83.179/api/v1/db/read',json = results)
    petunia = vernon_dursley.text

    if petunia == "[]":
        return "This ride doesn't exist", 204
    


    petunia = petunia.strip("[")
    petunia = petunia.strip("]")
    petunia = petunia.strip("(")
    petunia = petunia.strip(")")
    petunia = petunia.split(",")

    dudley = []
    for name in petunia:
        name = name.strip()
        name = name.strip("'")
        dudley.append(name)


 
 
    results={
            "message": "DELETE FROM rides WHERE rideid='"+j+"'"
        }

    harry_potter = requests.post('http://50.19.83.179/api/v1/db/write',json = results)
    
    
    return jsonify({}), 200




# CLEAR DB, API=11
@app.route('/api/v1/db/clear', methods=['POST'])
def api_cleardb():
    global rideidstart
    rideidstart = "9999"
    global reqnum
    reqnum = reqnum + 1
    global p
    p=11
    j=argg
    results={
            "message":"DELETE FROM rides"
        }
    harry_potter = requests.post('http://50.19.83.179/api/v1/db/write',json = results)

    results={

            "message":"UPDATE rides_id set ridestart=9999"
        }

    harry_potter = requests.post('http://50.19.83.179/api/v1/db/write',json = results)
    results={}
    return jsonify(results), 200

######################

# NUMBER OF REQUESTS, API=12
@app.route('/api/v1/_count', methods=['GET'])
def api_reqno():
    global reqnum
    reqnum = reqnum 
    #cur=mysql.connection.cursor()
    #cur.execute("SELECT value1 from count1 where name1=1")
    # thecount=cur.fetchone()
    resp=[]
    resp.append(reqnum)

    return jsonify(resp),200


# DEL NUMBER OF REQUESTS, API=13
@app.route('/api/v1/_count', methods=['DELETE'])
def api_delreqno():
    global reqnum
    reqnum = 0
   #cur=mysql.connection.cursor()
   #cur.execute("UPDATE count1 set value1=0 WHERE name1=1")
    resp={}

    return jsonify(resp),200














 
        

   
 
 
 
app.run(host='0.0.0.0', port=80)
