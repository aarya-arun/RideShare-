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




p=0
argg="LOL"
argnum = 0
reqnum = 0




# ADD A NEW RIDE, API=3
@app.route('/api/v1/rides', methods=['POST'])
def api_addnewride():  
    #write api
    global reqnum
    reqnum = reqnum + 1
    acromantula=requests.get('http://34.203.191.33/api/v1/users')
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
    cur=mysql.connection.cursor()
    cur.execute("SELECT ridestart from rides_id")
    rideidstart=cur.fetchone()
        
    results={

            "message": "INSERT INTO rides(created_by, timestamp1, source1, destination1, rideid) VALUES ('"+created_by+"','"+timestamp+"','"+source+"','"+destination+"','"+str(int(rideidstart[0])+1)+"')"
        }

        
    harry_potter = requests.post('http://34.203.191.33/api/v1/db/write', data = results)
    

    results={

            "message": "INSERT INTO ride_users(rideid,userz) VALUES ("+str(int(rideidstart[0])+1)+",'"+created_by+"')"
        }

         
    harry_potter = requests.post('http://34.203.191.33/api/v1/db/write', data = results)

    results={

            "message": "UPDATE rides_id SET ridestart="+str(int(rideidstart[0])+1)+" WHERE ridestart="+rideidstart[0]


        }

        
    harry_potter = requests.post('http://34.203.191.33/api/v1/db/write', data = results)

    cur.close()
    results={}
    return jsonify(results), 201
    
     #Inc





#RETURN ALL UPCOMING RIDES FOR A SOURCE AND DESTINATION API=4
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
    return redirect(flask.url_for('readfromdb'), code=307)       #------------------------------ ///////////UPCOMING PART ISNOT DONE YET WHAT THE FUCKING HECK. 






 #LIST ALL DETAILS OF A GIVEN RIDE API=5
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

        
    harry_potter = requests.post('http://34.203.191.33/api/v1/db/read', data = results)
    ginny=harry_potter.json()

    
    if(ginny==None):
        return "This ride doesn't exist", 204


    results={

        "message":"SELECT userz FROM ride_users where rideid="+j
    }

    harry_potter = requests.post('http://34.203.191.33/api/v1/db/read', data = results)
    ginny=harry_potter.json()
    
    res=[]
    for row1 in ginny:
        res.append(row1[0])
        #for x in row1:
        #    res.append(x)

    resp={
            "rideId": ginny[4],
            "created_by": ginny[0],
            "timestamp": ginny[1],
            "source": ginny[2],
            "destination": ginny[3],
            "users": res
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
    
   harry_potter = requests.post('http://34.203.191.33/api/v1/db/read', data = results)
   ginny=harry_potter.json()
   
    if(ginny==None):
        return "Ride doesn't exist. Create a new ride now!",400


    acromantula=requests.get('http://34.203.191.33/api/v1/users')
    aragog=acromantula.json()
    #return jsonify(aragog)
    flag=0
    for name in aragog:
        if name == request.json.get('username'):
            flag = 1
    if flag == 0:
        return "User doesn't exist. Join now to create a ride!",400

    results={

        "message":"SELECT *  FROM ride_users where userz='"+request.json.get('username')+"' AND rideid='"+j+"'"
    }
   
    harry_potter = requests.post('http://34.203.191.33/api/v1/db/read', data = results)
    ginny=harry_potter.json()


    if(ginny!=None):
        return "This user is already in the ride.",400


    
    j=argnum
    results={
            "message": "INSERT INTO ride_users(rideid,userz) VALUES ('"+j+"','"+request.json.get('username')+"')"
        }
     
    harry_potter = requests.post('http://34.203.191.33/api/v1/db/write', data = results)
    
        
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

        "message":"SELECT *  FROM rides where rideid='"+j+"'"
    } 
    harry_potter = requests.post('http://34.203.191.33/api/v1/db/read', data = results)
    ginny=harry_potter.json()
        
    if(ginny==None):
        return "This ride doesn't exist. Can't delete.",400
    else:
        j=argg
        results={
            "message": "DELETE FROM rides WHERE rideid='"+j+"'"
        }

        harry_potter = requests.post('http://34.203.191.33/api/v1/db/write', data = results)
    
        results={}
        return jsonify(results), 200




# CLEAR DB, API=11
@app.route('/api/v1/db/clear', methods=['POST'])
def api_cleardb():
    
    global reqnum
    reqnum = reqnum + 1
    global p
    p=11
    j=argg
    results={
            "message":"DELETE FROM rides"
        }
    harry_potter = requests.post('http://34.203.191.33/api/v1/db/write', data = results)

    results={

            "message":"UPDATE rides_id set ridestart=9999"
        }

    harry_potter = requests.post('http://34.203.191.33/api/v1/db/write', data = results)
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








#WRITE TO A DB, API=8

@app.route('/api/v1/db/write', methods=['POST', 'PUT', 'DELETE', 'GET'])
def writetodb():
    results=[]
    global p
    if p==3:
        
        
    
    
        

    if p==7:
        
        

    if p==11:
    
        









@app.route('/api/v1/db/read', methods=['POST', 'PUT', 'DELETE', 'GET'])
def readfromdb():
    #result=[]
    if p==3:
        

        return redirect(flask.url_for('writetodb'), code=307)

	
	
    if p==4:
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT *  FROM rides where source1=%s AND destination1=%s",(int(a),int(b)))
        #datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S') 
        row1 = cur.fetchall()
        if(row1==None):
            return "No such ride exists",204  

        res=[]
        for row in row1:
            #checkdate=datetime.strptime(row[1], "%m/%d/%Y, %H:%M:%S")
            
            resp={
                "rideId":row[4],
                "username": row[0],
                "timestamp": row[1]
            }
            res.append(resp)
        
        return jsonify(res),200


    if p==5:
        
       


    if p==6:
        
        


    if p==7:
        
        

   
 
 
 
app.run(host='0.0.0.0', port=80)
