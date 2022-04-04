import hashlib
from flask import request
from classes.dynamodb import DynamodbAPI
from boto3.dynamodb.conditions import Key

class UsersApi:
    def __init__(self) -> None:
        self.url = "users"
        self.tableName = "users"

        dynamodbInstance = DynamodbAPI()
        self.table = dynamodbInstance.dynamodb.Table('users')
    
    def __get(self, email):
        response = self.table.query(
            KeyConditionExpression=Key('email').eq(email)
        )
        return response
    
    def __checkPassword(self, queryPassword, dbPassword) -> bool:
        hashed = hashlib.sha256(str(queryPassword).encode()).hexdigest()
        return bool(hashed == dbPassword)

    def login(self) -> bool:
        input_json = request.get_json()
        queryEmail = input_json['email']
        queryPassword = input_json['password']

        checkUserExists = self.__get(queryEmail)

        if len(checkUserExists['Items']) > 0:
            dbPassword = checkUserExists['Items'][0]['password']
            checkPassword = self.__checkPassword(queryPassword, dbPassword)
            if checkPassword: 
                return True
        
        return False