import json
import re


def get_rate_conditions_from_file(path: str) -> list:

    with open(path, 'r') as json_file:
        data = json.load(json_file)

    rates = []

    for event in data:
        duration = data[event]['duration']
        rule = data[event]['rules'][0]
        if rule != 'clear':
            rate = int(re.findall(r'\d+', rule)[0])
            rates.extend([rate] * (duration // 1000))

    return rates
