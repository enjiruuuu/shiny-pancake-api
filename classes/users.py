import uuid, hashlib, json
from flask import request
from datetime import datetime
from classes.dynamodb import DynamodbAPI
from classes.apiConfig import ApiConfig
from boto3.dynamodb.conditions import Key

class UsersApi:
    def __init__(self) -> None:
        self.tableName = "users"

        dynamodbInstance = DynamodbAPI()
        self.table = dynamodbInstance.dynamodb.Table(self.tableName)

        self.apiConfigInstance = ApiConfig()
    
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

    def login(self) -> json:
        input_json = request.get_json()
        queryEmail = input_json['email']
        queryPassword = input_json['password'] 

        checkUserExists = self.__get(queryEmail)

        if len(checkUserExists['Items']) > 0:
            queryResponse = checkUserExists['Items'][0]
            dbPassword = queryResponse['password']
            checkPassword = self.__checkPassword(queryPassword, dbPassword)
            if checkPassword: 
                return {
                    "HTTPStatusCode": self.apiConfigInstance.statusCodes['success'],
                    "Message": self.apiConfigInstance.responses['login']['success'],
                    "data": {
                        "activated": queryResponse['activated'],
                        "name": queryResponse['name'],
                        "uuid": queryResponse['uuid'],
                    }
                }
        
        return {
            "HTTPStatusCode": self.apiConfigInstance.statusCodes['notFound'],
            "Message": self.apiConfigInstance.responses['login']['invalid']
        }