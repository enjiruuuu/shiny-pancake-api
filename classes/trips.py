import uuid
from classes.apiConfig import ApiConfig
from classes.dynamodb import DynamodbAPI
from flask import request
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

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
    
    def deleteUserTrip(self, tripUuid: str, ownerUuid: str):
        try:
            queryResponse = self.table.delete_item(Key={'ownerUuid': ownerUuid, 'tripUuid': tripUuid})
        except ClientError as e:
            return {
                "httpStatusCode": self.apiConfigInstance.statusCodes['serverError'],
                "message": e.response['Error']['message']
            }
        else:
            return {
                "httpStatusCode": self.apiConfigInstance.statusCodes['success'],
                "data": queryResponse
            }
    
    def addUserTrip(self, item):
        if 'ownerUuid' in item:
            randomUuid = uuid.uuid4()
            item['tripUuid'] = str(randomUuid) #generate uuid and add it to the json payload

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