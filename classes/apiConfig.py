import json

class ApiConfig:
    def __init__(self) -> None:
        with open('api-config.json', 'r') as f:
            self.config = json.load(f)
            self.responses = self.config['responses']
            self.statusCodes = self.responses['statusCodes']
            self.trips = self.responses['trips']