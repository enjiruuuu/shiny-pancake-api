from classes.apiConfig import ApiConfig
from classes.dynamodb import DynamodbAPI
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

class ItinerariesApi:
    def __init__(self) -> None:
        self.tableName = "itineraries"

        dynamodbInstance = DynamodbAPI()
        self.table = dynamodbInstance.dynamodb.Table(self.tableName)

        self.apiConfigInstance = ApiConfig()
    
    def addItinerary(self, item):
        if 'tripUuid' in item:
            queryResponse = self.table.put_item(
                Item = item
            )

            if queryResponse: 
                return {
                    "httpStatusCode": self.apiConfigInstance.statusCodes['success'],
                    "message": self.apiConfigInstance.responses['itineraries']['addedSuccess']
                }
            
            return {
                    "httpStatusCode": self.apiConfigInstance.statusCodes['serverError'],
                    "message": self.apiConfigInstance.responses['generic']['serverError']
            }
        
        return {
                "httpStatusCode": self.apiConfigInstance.statusCodes['serverError'],
                "message": self.apiConfigInstance.responses['generic']['missingKey']
        }

    def getItinerary(self, tripUuid: str):
        try:
            queryResponse = self.table.query(
                KeyConditionExpression=Key('tripUuid').eq(tripUuid)
            )
        except ClientError as e:
            return {
                "httpStatusCode": self.apiConfigInstance.statusCodes['serverError'],
                "message": e.response['Error']['message']
            }
        else:
            return {
                "httpStatusCode": self.apiConfigInstance.statusCodes['success'],
                "data": queryResponse['Items']
            }