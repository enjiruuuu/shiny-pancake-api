import hashlib
import uuid
from flask import request
from datetime import datetime
from classes.dynamodb import DynamodbAPI
from boto3.dynamodb.conditions import Key

class UsersApi:
    def __init__(self) -> None:
        self.tableName = "users"

        dynamodbInstance = DynamodbAPI()
        self.table = dynamodbInstance.dynamodb.Table(self.tableName)
    
    def __get(self, email):
        response = self.table.query(
            KeyConditionExpression=Key('email').eq(email)
        )
        return response
    
    def __checkPassword(self, queryPassword, dbPassword) -> bool:
        hashed = hashlib.sha256(str(queryPassword).encode()).hexdigest()
        return bool(hashed == dbPassword)

    def __generateUuid(self) -> str: 
        now = datetime.now()
        now = now.strftime("%m/%d/%Y%H:%M:%S")
        generatedUuid = uuid.uuid5(uuid.NAMESPACE_DNS, now)
        print(generatedUuid)
        return generatedUuid

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