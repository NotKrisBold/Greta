import requests
import pandas as pd

class Customizer:
    def __init__(self, bearer_token):
        self.value = None
        self.bearer_token = bearer_token
        self.df = None

    def calculate_scenario(self, scenario_id):
        url = 'http://localhost:30226/api/v1/customized-process/' + scenario_id
        headers = {
            'Authorization': f'Bearer {self.bearer_token}',
            'Content-Type': 'application/json; charset=utf-8'
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return None

    def generate_table(self, scenario_id):
        data = self.calculate_scenario(scenario_id)

        if data is None:
            return None
        data = data["customization"]["parameters"]

        table = {}

        for item in data:
            alias = item["alias"]
            table[alias] = {"options": [], "unit": item.get("unitOfMeasure"), "current value": item.get("value")}

            options = item.get("options")
            if options is not None:
                for option in options:
                    table[alias]["options"].append(option.get("label"))
                    if option.get("value") == item.get("value"):
                        table[alias]["current value"] = option.get("label")

        df = pd.DataFrame(table)
        df = df.transpose()
        self.value = df
        return df

    def print_table(self):
        filename = "productCustomization.txt"
        if self.value is not None:
            with open(filename, 'w') as file:
                file.write(self.value.to_string())