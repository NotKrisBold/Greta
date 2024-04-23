import json
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
            key = item["display"]["tab"]
            alias = item["alias"]

            # Append the alias to the table[key]
            if key not in table:
                table[key] = {}

            table[key][alias] = {"options": [], "unit": item.get("unitOfMeasure"), "current value": item.get("value")}

            options = item.get("options")
            if options is not None:
                for option in options:
                    table[key][alias]["options"].append(option.get("label"))
                    if option.get("value") == item.get("value"):
                        table[key][alias]["current value"] = option.get("label")

        self.value = table
        return table

    def print_table(self):
        if self.value is not None:
            filename = "productCustomization.txt"
            with open(filename, 'w') as file:
                for tab, parameters in self.value.items():
                    file.write(f"Tab: {tab}\n")
                    for alias, details in parameters.items():
                        file.write(f"\tParameter: {alias}\n")
                        file.write(f"\t\tUnit: {details['unit']}\n")
                        file.write(f"\t\tCurrent Value: {details['current value']}\n")
                        if len(details["options"]) > 0:
                            file.write(f"\t\tOptions: {', '.join(details['options'])}\n")
                        file.write("\n")


