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
            "httpStatusCode": self.apiConfigInstance.statusCodes['success'],
            "data": queryResponse['Items']
        }
    
    def addUserTrip(self, item):
        if 'ownerUuid' in item:
            queryResponse = self.table.put_item(
                Item = item
            )

            if queryResponse: 
                return {
                    "httpStatusCode": self.apiConfigInstance.statusCodes['success'],
                    "message": self.apiConfigInstance.responses['trips']['addedSuccess']
                }
            
            return {
                    "httpStatusCode": self.apiConfigInstance.statusCodes['serverError'],
                    "message": self.apiConfigInstance.responses['generic']['serverError']
            }
        
        return {
                "httpStatusCode": self.apiConfigInstance.statusCodes['serverError'],
                "message": self.apiConfigInstance.responses['generic']['missingKey']
        }