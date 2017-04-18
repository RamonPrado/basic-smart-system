import requests #Para hacer HTTP requests y leer responses
import json
url = 'http://130.206.112.29:5050/iot/devices/'

headers = {'Fiware-Service': 'icai10949',
           'Fiware-ServicePath':'/environment',
           'Content-Type': 'application/json'}
payload = {"devices": [
        {
            #Device_id
            "device_id": "Dev1094905",
            #Entity_name
            "entity_name": "Persiana01",
            "entity_type": "Device",
            "commands": [
                  { "object_id": "pe", "name": "turnPersiana", "type": "integer" }
            ],
            "transport": "MQTT"
        },
        {
            #Device_id
            "device_id": "Dev1094906",
            #Entity_name
            "entity_name": "Frio01",
            "entity_type": "Device",
            "commands": [
                  { "object_id": "fr", "name": "turnFrio", "type": "integer" }
            ],
            "transport": "MQTT"
        },
        {
            #Device_id
            "device_id": "Dev1094907",
            #Entity_name
            "entity_name": "Calor01",
            "entity_type": "Device",
            "commands": [
                  { "object_id": "ca", "name": "turnCalor", "type": "integer" }
            ],
            "transport": "MQTT"
        }
]}

r = requests.post(url, headers=headers, data=json.dumps(payload))
print(r)