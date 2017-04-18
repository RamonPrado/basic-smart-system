
# -*- coding: utf-8 -*-
from random import uniform

import paho.mqtt.client as mqtt
import time
# import json


def get_luminosity(hour):
    luminosity=9999 # In case of error
    if hour < 7 or hour > 19:   # Night
        luminosity = 0
    if hour >= 7 and hour <= 14:   # from night to high noon
        luminosity = round((5/7.0)*(1.0 * hour) - 5)
    if hour > 14 and hour <= 20:  # from high noon to night
        luminosity = round((-5/6.0) * hour + 50/3.0)
    return luminosity

def get_presence(hour):
    presence = False
    if hour < 8 or hour > 20:
        presence = True
    if hour>13 and hour < 17:
        presence = True
    return presence

def get_temperature(in_out):
    if in_out:
        temperature = round(uniform(10, 30),1)#Caso Fuera
    else:
        temperature = round(uniform(18, 24),1)#Caso Dentro

    return temperature

def on_connect(client,userdata,flags,rc):
    print("Connected with result code "+str(rc))


def on_publish(client, userdata, mid):
     pass

topicLuminosidad = "/1234/Dev1094901/attrs/l"
topicTempExterior = "/1234/Dev1094902/attrs/te"
topicTempInterior = "/1234/Dev1094903/attrs/ti"
topicPresencia = "/1234/Dev1094904/attrs/p"

in_out = False  # in --> True // out --> False
presence = False   # Está en casa --> True // No está en casa --> False
luminosity = 0  # [0..5] 0 --> Está Oscuro // 5 --> Hace mucho sol

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_publish

#
host = "130.206.112.29"

client.connect(host, port=1883, keepalive=60)
hour = 0

while hour < 25:
    if hour == 24:
        hour = 0

    temperatureOutside = get_temperature(True)   #Temperatura exterior
    temperatureInside = get_temperature(False)   #Temperatura interior

    luminosity = get_luminosity(hour)
    presence = get_presence(hour)
    print('Hora: ', hour, 'Temperatura Interior: ', temperatureInside,'Temperatura Exterior: ', temperatureOutside, 'Presencia: ', presence,'Luminosidad', luminosity)
    #print(str(temperatureInside)+","+str(temperatureOutside)+","+str(presence)+","+str(luminosity))
    time.sleep(1)
    hour += 1
    luminosidad = str(luminosity)
    client.publish(topicLuminosidad, luminosidad)
    presencia = str(presence)
    client.publish(topicPresencia, presencia)
    tempExterior = str(temperatureOutside)
    client.publish(topicTempExterior, tempExterior)
    tempInterior = str(temperatureInside)
    client.publish(topicTempInterior, tempInterior)
    time.sleep(1)


'''
topic="/1234/Dev1094903/attrs/l"
s= ""
while s != "exit":
     s=input("payload > ")
     client.publish(topic, s)
     time.sleep(5)
#     print(get_temperature())
'''