import json
import boto3

class DynamodbAPI: 
    def __init__(self) -> None:
        with open('api-config.json', 'r') as f:
            config = json.load(f)
        
        self.regionName = config['region_name']
        self.dynamodb = boto3.resource('dynamodb', region_name = self.regionName)