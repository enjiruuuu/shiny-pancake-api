import json
from classes.dynamodb import DynamodbAPI
from boto3.dynamodb.conditions import Key

class UsersApi:
    def __init__(self) -> None:
        self.url = "users"
        self.tableName = "users"

        dynamodbInstance = DynamodbAPI()
        self.table = dynamodbInstance.dynamodb.Table('users')
    
    def get(self, email):
        response = self.table.query(
            KeyConditionExpression=Key('email').eq(email)
        )
        print(response)