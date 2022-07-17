import uuid
from classes.apiConfig import ApiConfig
from classes.dynamodb import DynamodbAPI
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

class ListsApi:
    def __init__(self) -> None:
        self.tableName = "lists"

        dynamodbInstance = DynamodbAPI()
        self.table = dynamodbInstance.dynamodb.Table(self.tableName)

        self.apiConfigInstance = ApiConfig()
    
    def getAllListsByTrips(self, tripUuid: str):
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
    
    def getListByUuid(self, tripUuid: str, listUuid: str):
        try:
            queryResponse = self.table.get_item(Key={'tripUuid': tripUuid, 'listUuid': listUuid})
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
    
    def addUserList(self, item):
        #listuuid shld be generated from BE
        #tripUuid: str, ownerUuid: str, name: str
        if 'ownerUuid' in item:
            randomUuid = uuid.uuid4()
            item['listUuid'] = str(randomUuid) #generate uuid and add it to the json payload

            queryResponse = self.table.put_item(
                Item = item
            )

            if queryResponse: 
                return {
                    "httpStatusCode": self.apiConfigInstance.statusCodes['success'],
                    "message": self.apiConfigInstance.responses['lists']['addedSuccess']
                }
            
            return {
                    "httpStatusCode": self.apiConfigInstance.statusCodes['serverError'],
                    "message": self.apiConfigInstance.responses['generic']['serverError']
            }
        
        return {
                "httpStatusCode": self.apiConfigInstance.statusCodes['serverError'],
                "message": self.apiConfigInstance.responses['generic']['missingKey']
        }