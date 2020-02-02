import flask
from flask import request, jsonify
#from flask_api import status
import datetime


app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Create some test data for our catalog in the form of a list of dictionaries.

rides = [
    {'rideId': 10000,
     'created_by': "indu_r",
     'users': ["indu_r", "aarya_a"],
     'timestamp': "02-02-2020:19:05:66",
     'source': 1,
      'destination': 2}
]



users=[
    {
        'username':"indu_r",
        'password': "bullshit"
    },

    {
        'username': "aarya_a",
        'password': "bullfuck"
    },

    {
        'username': "maneesha_s",
        'password': "juice_kudithiya"
    }
]

rideidstart=10000

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


@app.route('/api/v1/users/all', methods=['GET'])
def api_allusers():
    return jsonify(users)

@app.route('/api/v1/rides/all', methods=['GET'])
def api_allrides():
    return jsonify(rides)



# ADD A NEW USER, API=1
@app.route('/api/v1/users', methods=['PUT'])
def api_addnewuser():



    for user in users:
        if user['username'] == request.json.get('username'):
            return "This user already exists!",400
    
    if(len(request.json.get('password'))!=40):
        return "Bad password! Please enter a new one.",400

    for letter in request.json.get('password'):
        if(letter not in {'a','b','c','d','e','f','A','B','C','D','E','F','0','1','2','3','4','5','6','7','8','9'}):
            return "Bad password! Please enter a new one.",400
   
    newuser={

        'username': request.json.get('username'),
        'password': request.json.get('password')
    }

    results=[]
    users.append(newuser)

    return jsonify(results),201




# DELETE A USER, API=2
@app.route('/api/v1/users/<usn>', methods=['DELETE'])
def api_deluser(usn):

    usn1 = usn
    results = []
    for user in users:
        if user['username'] == usn1:
            users.remove(user)
            return jsonify(results),200

    return "User never existed. Can't delete.",400




# ADD A NEW RIDE, API=3
@app.route('/api/v1/rides', methods=['POST'])
def api_addnewride():
   

    for user in users:
        if user['username'] == request.json.get('created_by'):
            global rideidstart
            rideidstart=rideidstart+1
            newride={

                'created_by': request.json.get('created_by'),
                'timestamp': request.json.get('timestamp'),
                'source': request.json.get('source'),
                'destination': request.json.get('destination'),
                'users': [request.json.get('created_by')],
                'rideId': rideidstart
            }
            results=[]
            rides.append(newride)
            return jsonify(results),200

    return "This user doesn't exist! Join now to create a ride.",400




#RETURN ALL UPCOMING RIDES FOR A SOURCE AND DESTINATION API=4
@app.route('/api/v1/rides', methods=['GET'])
def api_sourceanddest():

    if 'source' not in request.args:
        return "Error! Please provide a source.",400

    if 'destination' not in request.args:
        return "Error! Please provide a destination.",400
    
    source = int(request.args.get('source'))
    destination = int(request.args.get('destination'))
  
    results = []



    for ride in rides:
        if ride['source'] == source and ride['destination'] == destination and ride['timestamp']>datetime.date.today().strftime("%d-%m-%Y:%S-%M-%H"):
            newride={ 

                'rideId': ride['rideId'],
                'username': ride['created_by'],
                'timestamp': ride['timestamp']
            }
            results.append(newride)
    if results==0:
        p=204
    else: 
        p=200
    return jsonify(results),p




# LIST ALL DETAILS OF A GIVEN RIDE API=5
@app.route('/api/v1/rides/<id>', methods=['GET'])
def api_id(id):
    id1 = int(id)

    results = []

    for ride in rides:
        if ride['rideId'] == id1:
            results.append(ride)
            return jsonify(results),200

    return "This ride doesn't exist. Sorry!",204




# JOIN A RIDE, API=6

@app.route('/api/v1/rides/<rideid>', methods=['POST'])
def api_joinride(rideid):

    usn= request.json.get('username')
    id = int(rideid)
    results=[]

    flagu=0
    flagr=0

    for user in users:
        if user['username']== request.json.get('username'):
            flagu=1

    for ride in rides:
        if ride['rideId'] == id:
            flagr=1

    if flagu==0:
        return "This user doesn't exist! Join today to create/join rides.",204
    if flagr==0:
        return "This ride doesn't exist. Sorry!",204

    if flagu==1 and flagr==1:
        for ride in rides:
            if ride['rideId'] ==id:
                if usn in ride['users']:
                    return "This user is already part of the ride."
                else:
                    ride['users'].append(usn)
    
    return jsonify(results),200



# DELETE A RIDE, API=7
@app.route('/api/v1/rides/<rideid>', methods=['DELETE'])
def api_delride(rideid):

    
    results = []
    for ride in rides:
        if ride['rideId'] == int(rideid):
            rides.remove(ride)
            return jsonify(results),200

    return "This ride doesn't exist!"




app.run()