import requests
import pandas as pd


class Calculator:
    def __init__(self, bearer_token):
        self.value = None
        self.bearer_token = bearer_token

    def calculate_scenario(self, scenario_id):
        url = 'http://localhost:30226/api/v1/basic/calculate-scenario'
        headers = {
            'Authorization': f'Bearer {self.bearer_token}',
            'Content-Type': 'application/json; charset=utf-8'
        }
        params = {
            'scenarioId': scenario_id
        }
        response = requests.post(url, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_impact_names(self, impact_method_id):
        url = f"http://localhost:30226/api/v1/impact-method/{impact_method_id}"
        headers = {
            "Authorization": f'Bearer {self.bearer_token}',
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return None

    def generate_table(self, scenario_id, impact_method_id):
        data = self.calculate_scenario(scenario_id)
        names = self.get_impact_names(impact_method_id)

        if data is None or names is None:
            return None

        data = data[0]["phaseResults"]
        names = names["impactCategories"]

        table = {}
        for item in names:
            table[item["name"]] = {}
        for i in range(0, len(data)):
            for j in range(0, len(data[i]["nodeImpactResult"]["impactList"])):
                for item in names:
                    if item["refId"] == data[i]["nodeImpactResult"]["impactList"][j]["refId"]:
                        value_unit = (data[i]["nodeImpactResult"]["impactList"][j]["value"],
                                      data[i]["nodeImpactResult"]["impactList"][j]["unit"])
                        table[item["name"]][data[i]["nodeImpactResult"]["name"]] = value_unit

        df = pd.DataFrame(table)
        df = df.transpose()
        self.value = df
        return df

    def print_table(self):
        if self.value is not None:
            filename = "calculatedScenario.txt"
            with open(filename, 'w') as file:
                file.write(self.value.to_string(index=4))
