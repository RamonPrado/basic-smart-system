# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import requests
import json

# The callback for when the client receives a CONNACK response from the server.
urlPersiana='http://130.206.112.29:1026/v2/entities/Persiana01/attrs/turnPersiana?type=Device'
urlFrio='http://130.206.112.29:1026/v2/entities/Frio01/attrs/turnFrio?type=Device'
urlCalor='http://130.206.112.29:1026/v2/entities/Calor01/attrs/turnCalor?type=Device'
header={'Fiware-Service':'icai10949',
        'Fiware-ServicePath':'/environment',
        'Content-Type':'application/json'}

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
    global pPersiana
    global pFrio
    global pCalor


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
        update_actuators(luminosidad, tempExterior, tempInterior, presencia)
        payloadPersiana = {
            "value": persiana,
            "type": "int"
        }
        payloadFrio = {
            "value": calor,
            "type": "int"
        }
        payloadCalor = {
            "value": frio,
            "type": "int"
        }
        pPersiana = requests.put(urlPersiana, headers=header, data=json.dumps(payloadPersiana));
        pFrio = requests.put(urlFrio, headers=header, data=json.dumps(payloadFrio));
        pCalor = requests.put(urlCalor, headers=header, data=json.dumps(payloadCalor));
        received_ex = False
        received_pre = False
        received_lum = False
        received_in = False



def update_actuators(luminosidad, tempExterior, tempInterior, presencia):
    global frio
    global calor
    global persiana

    if tempExterior - tempInterior >= -15 and tempExterior - tempInterior <= -10:
        calor = 3
        frio = 0
        #print("Variable calor " + "updated to: " + str(calor))
    if tempExterior - tempInterior >= -10 and tempExterior - tempInterior <= -5:
        calor = 2
        frio = 0
        #print("Variable calor " + "updated to: " + str(calor))
    if tempExterior - tempInterior >= -5 and tempExterior - tempInterior < 0:
        calor = 1
        frio = 0
        #print("Variable calor " + "updated to: " + str(calor))
    if tempExterior - tempInterior <= 15 and tempExterior - tempInterior >= 10:
        frio = 3
        calor = 0
        #print("Variable frio " + "updated to: " + str(frio))
    if tempExterior - tempInterior <= -10 and tempExterior - tempInterior >= -5:
        frio = 2
        calor = 0
        #print("Variable frio " + "updated to: " + str(frio))
    if tempExterior - tempInterior <= -5 and tempExterior - tempInterior > 0:
        frio = 1
        calor = 0
        #print("Variable frio " + "updated to: " + str(frio))
    if tempExterior - tempInterior == 0:
        frio = 0
        calor = 0
        #print("Variable calor " + "updated to: " + str(calor))
        #print("Variable frio " + "updated to: " + str(frio))
    if presencia == True and luminosidad > 3:
        persiana = 0
        #print("Variable persiana " + "updated to: " + str(persiana))
    else:
        persiana = luminosidad
        #print("Variable persiana " + "updated to: " + str(persiana))
    #print("Calor: " + str(calor) + " Frio: " + str(frio) + " Persiana: " + str(persiana))
    print(str(calor) + ","+str(frio) + "," + str(persiana))

topicLuminosidad = "/1234/Dev1094901/attrs/l"
topicTempExterior = "/1234/Dev1094902/attrs/te"
topicTempInterior = "/1234/Dev1094903/attrs/ti"
topicPresencia = "/1234/Dev1094904/attrs/p"

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

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


# ACTUADORES:
persiana = 0   # persiana abierta --> 0 persiana cerrada --> 5
calor = 0   # Calor desactivado --> 0 calor a tope --> 3
frio = 0   # Frio desactivado --> 0 frio a tope --> 3

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()