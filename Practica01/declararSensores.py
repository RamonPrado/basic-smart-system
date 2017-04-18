import requests #Para hacer HTTP requests y leer responses
import json
url = 'http://130.206.112.29:5050/iot/devices'

headers = {'Fiware-Service': 'icai10949',
           'Fiware-ServicePath':'/environment',
           'Content-Type': 'application/json'}
payload = {"devices": [
        {
            #Device_id
            "device_id": "Dev1094901",
            #Entity_name
            "entity_name": "Luminosidad01",
            "entity_type": "Device",
            "attributes": [
                  { "object_id": "l", "name": "luminosidad", "type": "float" }
            ],
            "transport": "MQTT"
        },
        {
            #Device_id
            "device_id": "Dev1094902",
            #Entity_name
            "entity_name": "TempExterior01",
            "entity_type": "Device",
            "attributes": [
                  { "object_id": "te", "name": "tempExterior", "type": "float" }
            ],
            "transport": "MQTT"
        },
        {
            #Device_id
            "device_id": "Dev1094903",
            #Entity_name
            "entity_name": "TempInterior01",
            "entity_type": "Device",
            "attributes": [
                  { "object_id": "ti", "name": "tempInterior", "type": "float" }
            ],
            "transport": "MQTT"
        },
{
            #Device_id
            "device_id": "Dev1094904",
            #Entity_name
            "entity_name": "Presencia01",
            "entity_type": "Device",
            "attributes": [
                  { "object_id": "p", "name": "presencia", "type": "boolean" }
            ],
            "transport": "MQTT"
        }

]}

r = requests.post(url, headers=headers, data=json.dumps(payload))
print(r)
