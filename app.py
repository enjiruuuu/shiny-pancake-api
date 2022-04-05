import json
from flask import Flask, request
from classes.users import UsersApi 
from classes.trips import TripsApi
from classes.lists import ListsApi

# setup
app = Flask(__name__)
with open('api-config.json', 'r') as f:
    config = json.load(f)

responses = config['responses']
statusCodes = responses['statusCodes']

usersApiInstance = UsersApi()
tripsApiInstance = TripsApi()
listsApiInstance = ListsApi()

# login / users
@app.route('/login', methods=["GET"])
def login():
    checkLogin = usersApiInstance.login()
    return checkLogin

@app.route('/users/create', methods=["PUT"])
def createUser():
    createUser = usersApiInstance.createUser()
    return createUser

# trips
@app.route('/users/<ownerUuid>/trips', methods=["GET"])
def getUserTrips(ownerUuid):
    trips = tripsApiInstance.getAllUserTrips(ownerUuid)
    return trips

@app.route('/trips/create', methods=["PUT"])
def addUserTrip():
    input_json = request.get_json()
    trips = tripsApiInstance.addUserTrip(input_json) #ownerUuid must be in the json
    return trips

# lists
@app.route('/trips/<tripUuid>/lists', methods=["GET"])
def getListsByTrips(tripUuid):
    lists = listsApiInstance.getAllListsByTrips(tripUuid)
    return lists

@app.route('/trips/<tripUuid>/lists/<listUuid>', methods=["GET"])
def getListByUuid(tripUuid, listUuid):
    list = listsApiInstance.getListByUuid(tripUuid, listUuid)
    return list