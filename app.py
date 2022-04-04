import json
from flask import Flask
from classes.users import UsersApi 

# setup
app = Flask(__name__)
with open('api-config.json', 'r') as f:
    config = json.load(f)

responses = config['responses']
statusCodes = responses['statusCodes']

# login
@app.route('/login', methods=["GET"])
def login():
    checkLogin = UsersApi().login()
    
    if checkLogin:
        return {
            "HTTPStatusCode": statusCodes['success'],
            "Message": responses['login']['success']
        }

    return {
        "HTTPStatusCode": statusCodes['notFound'],
        "Message": responses['login']['invalid']
    }