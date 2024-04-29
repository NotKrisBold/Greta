import requests
import pandas as pd


class ProductName:
    def __init__(self, bearer_token):
        self.value = None
        self.bearer_token = bearer_token

    def fetch(self, scenario_id):
        url = 'http://localhost:30226/api/v1/scenario/' + str(scenario_id)
        headers = {
            'Authorization': f'Bearer {self.bearer_token}',
            'Content-Type': 'application/json; charset=utf-8'
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_name(self, scenario_id):
        data = self.fetch(scenario_id)
        self.value = data["name"]
        return self.value
