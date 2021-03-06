import json
from flask import Flask, request
from flask_cors import CORS, cross_origin
from classes.itineraries import ItinerariesApi
from classes.users import UsersApi 
from classes.trips import TripsApi
from classes.lists import ListsApi

# setup
app = Flask(__name__)
CORS(app)
with open('api-config.json', 'r') as f:
    config = json.load(f)

responses = config['responses']
statusCodes = responses['statusCodes']

usersApiInstance = UsersApi()
tripsApiInstance = TripsApi()
listsApiInstance = ListsApi()
itinerariesApiInstance = ItinerariesApi()

# login / users
# TODO: refactor to POST request for security. GET requests are sending password through params and are expected to be cached.
# GET is just temporary solution to move on

@app.route('/login', methods=["GET"])
@cross_origin()
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

@app.route('/users/<ownerUuid>/trips/<tripUuid>', methods=["GET"])
def getSpecificUserTrip(ownerUuid, tripUuid):
    trip = tripsApiInstance.getSpecificUserTrip(ownerUuid, tripUuid)
    return trip

@app.route('/trips/create', methods=["PUT"])
def addUserTrip():
    input_json = request.get_json()
    trips = tripsApiInstance.addUserTrip(input_json) #ownerUuid must be in the json
    return trips

@app.route('/trips/<tripUuid>/user/<ownerUuid>/update', methods=["PATCH"])
def updateUserTrip(tripUuid, ownerUuid):
    input_json = request.get_json()
    trips = tripsApiInstance.updateUserTrip(tripUuid, ownerUuid, input_json) #ownerUuid must be in the json
    return trips

@app.route('/trips/<tripUuid>/user/<ownerUuid>/delete', methods=["DELETE"])
def deleteUserTrip(tripUuid, ownerUuid):
    response = tripsApiInstance.deleteUserTrip(tripUuid, ownerUuid)
    return response

# lists
@app.route('/trips/<tripUuid>/lists', methods=["GET"])
def getListsByTrips(tripUuid):
    lists = listsApiInstance.getAllListsByTrips(tripUuid)
    return lists

@app.route('/trips/<tripUuid>/lists/<listUuid>', methods=["GET"])
def getListByUuid(tripUuid, listUuid):
    list = listsApiInstance.getListByUuid(tripUuid, listUuid)
    return list

@app.route('/lists/create', methods=["PUT"])
def addUserList():
    input_json = request.get_json()
    lists = listsApiInstance.addUserList(input_json) #ownerUuid must be in the json
    return lists

#itineraries
@app.route('/itineraries/create', methods=["PUT"])
def addItinerary():
    input_json = request.get_json()
    itinerary = itinerariesApiInstance.addItinerary(input_json) #ownerUuid must be in the json
    return itinerary

@app.route('/itineraries/<tripUuid>', methods=["GET"])
def getItinerary(tripUuid):
    itinerary = itinerariesApiInstance.getItinerary(tripUuid)
    return itinerary