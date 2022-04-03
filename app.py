from flask import Flask, request, jsonify
from classes.users import UsersApi 

# setup
app = Flask(__name__)


# users
@app.route('/users', methods=["GET"])
def getUsers():
    input_json = request.get_json(force=True) 
    queryEmail = input_json['email']

    usersApi = UsersApi()
    response = usersApi.get(queryEmail)

    return jsonify(response)