import json

json_path = join(dirname(__file__), 'tojson.json')

jsonFile = open(json_path)
jsonData = json.load(jsonFile)
jsonFile.close()