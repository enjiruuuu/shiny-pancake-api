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
                "HTTPStatusCode": self.apiConfigInstance.statusCodes['serverError'],
                "Message": e.response['Error']['Message']
            }
        else:
            return {
                "HTTPStatusCode": self.apiConfigInstance.statusCodes['success'],
                "data": queryResponse['Items']
            }
    
    def getListByUuid(self, tripUuid: str, listUuid: str):
        try:
            queryResponse = self.table.get_item(Key={'tripUuid': tripUuid, 'listUuid': listUuid})
        except ClientError as e:
            return {
                "HTTPStatusCode": self.apiConfigInstance.statusCodes['serverError'],
                "Message": e.response['Error']['Message']
            }
        else:
            return {
                "HTTPStatusCode": self.apiConfigInstance.statusCodes['success'],
                "data": queryResponse
            }