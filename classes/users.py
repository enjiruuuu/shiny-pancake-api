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

    def __hashPassword(self, queryPassword):
        return hashlib.sha256(str(queryPassword).encode()).hexdigest()
    
    def __checkPassword(self, queryPassword, dbPassword) -> bool:
        hashed = self.__hashPassword(queryPassword)
        return bool(hashed == dbPassword)

    def __generateUuid(self) -> str: 
        now = datetime.now()
        now = now.strftime("%m/%d/%Y%H:%M:%S")
        generatedUuid = uuid.uuid5(uuid.NAMESPACE_DNS, now)
        print(generatedUuid)
        return generatedUuid

    def login(self) -> json:
        # input_json = request.get_json()
        # queryEmail = input_json['email']
        # queryPassword = input_json['password']

        queryEmail = request.args.get('email') 
        queryPassword = request.args.get('password')

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

    def createUser(self) -> json:
        input_json = request.get_json()
        
        if 'email' in input_json and 'password' in input_json and 'name' in input_json:
            queryEmail = input_json['email']
            queryPassword = input_json['password']
            queryName = input_json['name']

            checkUserExists = self.__get(queryEmail)

            if len(checkUserExists['Items']) == 0:
                generatedUuid = self.__generateUuid()
                hashedPassword = self.__hashPassword(queryPassword)
                if(generatedUuid and hashedPassword):
                    item = {
                        "email": queryEmail,
                        "activated": False,
                        "uuid": str(generatedUuid),
                        "password": str(hashedPassword),
                        "name": queryName
                    }

                    queryResponse = self.table.put_item(
                        Item = item
                    )

                    if queryResponse: 
                        return {
                            "HTTPStatusCode": self.apiConfigInstance.statusCodes['success'],
                            "Message": self.apiConfigInstance.responses['users']['addedSuccess'],
                            "data": {
                                "email": queryEmail,
                                "name": queryName,
                                "uuid": str(generatedUuid)
                            }
                        }
                    
                    return {
                            "HTTPStatusCode": self.apiConfigInstance.statusCodes['serverError'],
                            "Message": self.apiConfigInstance.responses['generic']['serverError']
                        }
            
            return {
                "HTTPStatusCode": self.apiConfigInstance.statusCodes['conflict'],
                "Message": self.apiConfigInstance.responses['users']['addedExists']
            }

        return {
            "HTTPStatusCode": self.apiConfigInstance.statusCodes['serverError'],
            "Message": self.apiConfigInstance.responses['generic']['missingKey']
        }
