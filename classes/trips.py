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
    
    def getSpecificUserTrip(self, ownerUuid: str, tripUuid: str):
        try:
            queryResponse = self.table.get_item(Key={'ownerUuid': ownerUuid, 'tripUuid': tripUuid})
        except ClientError as e:
            return {
                "httpStatusCode": self.apiConfigInstance.statusCodes['serverError'],
                "message": e.response['Error']['message']
            }
        else:
            if 'Item' in queryResponse:
                return {
                    "httpStatusCode": self.apiConfigInstance.statusCodes['success'],
                    "data": queryResponse['Item']
                }
            else:
                return {
                    "httpStatusCode": self.apiConfigInstance.statusCodes['notFound'],
                    "message": self.apiConfigInstance.trips['notFound']
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
    
    def updateUserTrip(self, tripUuid, ownerUuid, item):
        queryResponse = self.table.get_item(
            Key={'ownerUuid': ownerUuid, 'tripUuid': tripUuid},
        )

        if 'Item' in queryResponse:
            try:
                query = self.table.update_item(
                    Key={'ownerUuid': ownerUuid, 'tripUuid': tripUuid},
                    ExpressionAttributeValues={  #only these 3 attributes are editable
                        ":title" : item["title"],
                        ":startDate" : item["startDate"],
                        ":endDate" : item["endDate"],
                    },
                    UpdateExpression="SET title = :title, startDate = :startDate, endDate = :endDate",
                )
            except ClientError as e:
                return {
                    "httpStatusCode": self.apiConfigInstance.statusCodes['serverError'],
                    "message": e.response['Error']['message']
                }
            else:
                return {
                    "httpStatusCode": self.apiConfigInstance.statusCodes['success'],
                    "data": query
                }
        else:
            return {
                "httpStatusCode": self.apiConfigInstance.statusCodes['notFound'],
                "message": self.apiConfigInstance.trips['notFound']
            }
        