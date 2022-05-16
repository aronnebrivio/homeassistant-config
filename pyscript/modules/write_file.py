import json
from io import open


def write_json(filename, content):
    with open(filename, 'w') as file:
        json.dump(content, file, indent=4)
