from jinja2 import Undefined
from classes.apiConfig import ApiConfig
from classes.dynamodb import DynamodbAPI
from flask import request
from boto3.dynamodb.conditions import Key

class TripsApi:
    def __init__(self) -> None:
        self.tableName = "trips"

        dynamodbInstance = DynamodbAPI()
        self.table = dynamodbInstance.dynamodb.Table(self.tableName)

        self.apiConfigInstance = ApiConfig()
    
    def getAllUserTrips(self, ownerUuid: str):
        queryResponse = self.table.query(
            KeyConditionExpression=Key('ownerUuid').eq(ownerUuid)
        )
        return {
            "HTTPStatusCode": self.apiConfigInstance.statusCodes['success'],
            "data": queryResponse['Items']
        }
    
    def addUserTrip(self, item):
        if 'ownerUuid' in item:
            queryResponse = self.table.put_item(
                Item = item
            )

            if queryResponse: 
                return {
                    "HTTPStatusCode": self.apiConfigInstance.statusCodes['success'],
                    "Message": self.apiConfigInstance.responses['trips']['addedSuccess']
                }
            
            return {
                    "HTTPStatusCode": self.apiConfigInstance.statusCodes['serverError'],
                    "Message": self.apiConfigInstance.responses['generic']['serverError']
            }
        
        return {
                "HTTPStatusCode": self.apiConfigInstance.statusCodes['serverError'],
                "Message": self.apiConfigInstance.responses['trips']['addedMissingKey']
        }