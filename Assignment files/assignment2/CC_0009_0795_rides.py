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




p=0
argg="LOL"
argnum=0




# ADD A NEW RIDE, API=3
@app.route('/api/v1/rides', methods=['POST'])
def api_addnewride():
    global argnum  
    argnum=argnum+1    
    #write api
    global p
    p=3
    return redirect(flask.url_for('readfromdb'), code=307)





#RETURN ALL UPCOMING RIDES FOR A SOURCE AND DESTINATION API=4
@app.route('/api/v1/rides', methods=['GET'])
def api_sourceanddest():
    global argnum
    argnum=argnum+1
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
    return redirect(flask.url_for('readfromdb'), code=307)






 #LIST ALL DETAILS OF A GIVEN RIDE API=5
@app.route('/api/v1/rides/<id>', methods=['GET'])
def api_id(id):
    global argnum
    argnum=argnum+1
    if flask.request.method == 'POST':
        return "Method not allowed!", 405 
    
    global p
    p=5
    global argnum
    argnum=id
    
    return redirect(flask.url_for('readfromdb'), code=307)




#JOIN A RIDE, API=6

@app.route('/api/v1/rides/<rideid>', methods=['POST'])
def api_joinride(rideid):
    global argnum
    argnum=argnum+1
    global p
    p=6
    global argnum
    argnum=rideid
    return redirect(flask.url_for('readfromdb'), code=307)







# DELETE A RIDE, API=7
@app.route('/api/v1/rides/<rideid>', methods=['DELETE'])
def api_delride(rideid):
     
    global argnum
    argnum=argnum+1
    if flask.request.method == 'POST':
        return "Method not allowed!", 405 
    
    global p
    p=7
    global argg
    argg=rideid
    return redirect(flask.url_for('readfromdb'), code=307)




# CLEAR DB, API=11
@app.route('/api/v1/db/clear', methods=['POST'])
def api_cleardb():
    
    global argnum
    argnum=argnum+1
    global p
    p=11
    return redirect(flask.url_for('writetodb'), code=307)


# NUMBER OF REQUESTS, API=12
@app.route('/api/v1/_count', methods=['GET'])
def api_reqno():
   global argnum
   argnum=argnum+0
   #cur=mysql.connection.cursor()
   #cur.execute("SELECT value1 from count1 where name1=1")
  # thecount=cur.fetchone()
   resp=[]
   resp.append(argnum)

   return jsonify(resp),200


# DEL NUMBER OF REQUESTS, API=13
@app.route('/api/v1/_count', methods=['DELETE'])
def api_delreqno():
   global argnum
   argnum=0
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
        created_by= request.json.get('created_by')
        timestamp=request.json.get('timestamp')
        source=request.json.get('source')
        destination=request.json.get('destination')
        cur=mysql.connection.cursor()
        cur.execute("SELECT ridestart from rides_id")
        rideidstart=cur.fetchone()
        #rideidstart=rideids[0][0]
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO rides(created_by, timestamp1, source1, destination1, rideid) VALUES (%s, %s, %s, %s, %s)", (created_by, timestamp, source, destination, str(int(rideidstart[0])+1)))
        cur.execute("INSERT INTO ride_users(rideid,userz) VALUES (%s, %s)", (str(int(rideidstart[0])+1),created_by))
        cur.execute("UPDATE rides_id SET ridestart=(%s) WHERE ridestart=(%s)", (str(int(rideidstart[0])+1), rideidstart[0]))
        mysql.connection.commit()
        cur.close()
        results={}
        return jsonify(results), 201
        
    
    if p==6:
        cur = mysql.connection.cursor()
        j=argnum
        cur.execute("INSERT INTO ride_users(rideid,userz) VALUES (%s, %s)",(j,request.json.get('username')))
        mysql.connection.commit()
        cur.close()
        results={}
        return jsonify(results), 200
        

    if p==7:
        cur = mysql.connection.cursor()
        j=argg
        cur.execute("DELETE FROM rides WHERE rideid='"+j+"'" )
        mysql.connection.commit()
        cur.close()
        results={}
        return jsonify(results), 200

    if p==11:
        cur = mysql.connection.cursor()
        j=argg
        cur.execute("DELETE FROM rides")
        cur.execute("UPDATE rides_id set ridestart=9999")
        mysql.connection.commit()
        cur.close()
        results={}
        return jsonify(results), 200




@app.route('/api/v1/db/read', methods=['POST', 'PUT', 'DELETE', 'GET'])
def readfromdb():
    result=[]
    if p==3:
	acromantula=requests.get('http://52.1.1.34/api/v1/users')
	aragog=acromantula.json()
	flag=0
	for name in aragog:
		if name==request.json.get('created_by'):
			flag=1
	if flag==0:
		return "User doesn't exist. Join now to create a ride!",400

	return redirect(flask.url_for('writetodb'), code=307)
	
	return "Hello!"
    
    if p==4:
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT *  FROM rides where source1=%s AND destination1=%s",(int(a),int(b)))
        #datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S') 
        row1 = cur.fetchall()
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
        
        cur = mysql.connection.cursor()
        j=argnum
        cur.execute("SELECT *  FROM rides where rideid='"+j+"'")
        row = cur.fetchone()
       # return jsonify(row)
        if(row==None):
            return "This ride doesn't exist",204
        cur.execute("SELECT userz FROM ride_users where rideid="+j)
        res=[]
        for row1 in cur:
            res.append(row1[0])
        #for x in row1:
        #    res.append(x)

        resp={
            "rideId": row[4],
            "created_by": row[0],
            "timestamp": row[1],
            "source": row[2],
            "destination": row[3],
            "users": res
        }
        
        return jsonify(resp),200



    if p==6:
        
        cur = mysql.connection.cursor()
        j=argnum
        cur.execute("SELECT *  FROM rides where rideid='"+j+"'")
        row = cur.fetchone()
        if(row==None):
            return "Ride doesn't exist. Create a new ride now!",400

	
	hippogriff=requests.get('http://52.1.1.34/api/v1/users')
	buckbeak=hippogriff.json()
	flag1=0
	for name in buckbeak:
		if name==request.json.get('username'):
			flag1=1

	if flag1==0:
		return "User doesn't exist. Join today!",400


        cur.execute("SELECT *  FROM ride_users where userz='"+request.json.get('username')+"' AND rideid='"+j+"'")
        row2 = cur.fetchone()
        if(row2!=None):
            return "This user is already in the ride.",400

        return redirect(flask.url_for('writetodb'), code=307)




    if p==7:
        
        cur = mysql.connection.cursor()
        j=argg
       
        cur.execute("SELECT *  FROM rides where rideid='"+j+"'")
        row = cur.fetchone()
        
        if(row==None):
            return "This ride doesn't exist. Can't delete.",400
        else:
            return redirect(flask.url_for('writetodb'), code=307)


            
app.run(host='0.0.0.0', port=80)
