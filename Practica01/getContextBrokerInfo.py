# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import requests #Para hacer HTTP requests y leer responses
import urllib
import urllib2

# The callback for when the client receives a CONNACK response from the server.

#Clear Stream : http://data.sparkfun.com/input/lz6yR5odw1F4Kyb6J8Gd/clear?private_key=Elp0GwngP5hqMolE0VwW

def on_connect(client, userdata, rc):
    print("Connected with result code" + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/1234/Dev1094901/#")
    client.subscribe("/1234/Dev1094902/#")
    client.subscribe("/1234/Dev1094903/#")
    client.subscribe("/1234/Dev1094904/#")

# The callback for when a PUBLISH message is received from the server.


def on_message(client, userdata, msg):
        global luminosidad
        global received_lum
        global tempExterior
        global received_ex
        global tempInterior
        global received_in
        global presencia
        global received_pre
        if msg.topic == topicLuminosidad:
            luminosidad = float(msg.payload)
            received_lum = True
        if msg.topic == topicTempExterior:
            tempExterior = float(msg.payload)
            received_ex = True
        if msg.topic == topicTempInterior:
            tempInterior = float(msg.payload)
            received_in = True
        if msg.topic == topicPresencia:
            presencia = bool(msg.payload)
            received_pre = True
        if received_ex and received_in and received_lum and received_pre:
            received_ex = False
            received_pre = False
            received_lum = False
            received_in = False
            print(str(tempInterior) + ";" + str(tempExterior) + ";" + str(presencia) + ";" + str(luminosidad))
            '''
            data = {}  # Create empty set, then fill in with our two fields:
            data['tempinside'] = tempInterior
            data['tempoustide'] = tempExterior
            data = urllib.urlencode(data)
            post_request = urllib2.Request(server+"/input/"+publicKey, data, headers)
            post_response = urllib2.urlopen(post_request)
            print post_response.read()
            '''
            #payload = {'tempinside': tempInterior, 'tempoutside': tempExterior}
            #a = requests.post("http://data.sparkfun.com/input/"+publicKey, headers=headers, data=payload,)
            payload = {'private_key': privateKey, 'tempinside': tempInterior, 'tempoustside': tempExterior}
            a = requests.get("http://data.sparkfun.com/input/"+publicKey, params=payload)
            print(a)


topicLuminosidad = "/1234/Dev1094901/attrs/l"
topicTempExterior = "/1234/Dev1094902/attrs/te"
topicTempInterior = "/1234/Dev1094903/attrs/ti"
topicPresencia = "/1234/Dev1094904/attrs/p"

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

server = "http://data.sparkfun.com"
publicKey = "lz6yR5odw1F4Kyb6J8Gd"
privateKey = "Elp0GwngP5hqMolE0VwW"



# Now we need to set up our headers:
headers = {} # start with an empty set
# These are static, should be there every time:
headers["Content-Type"] = "application/x-www-form-urlencoded"
headers["Phant-Private-Key"] = privateKey # private key header


host="130.206.112.29"
print("Connecting to "+host)
client.connect(host, 1883, 60)

# SENSORES:
luminosidad = 9999.9
tempExterior = 9999.9
tempInterior = 9999.9
presencia = None

received_ex = None
received_in = None
received_lum = None
received_pre = None
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()