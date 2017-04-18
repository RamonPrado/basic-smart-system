import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, rc):
   print("Connected with result code" + str(rc))
   # Subscribing in on_connect() means that if we lose the connection and
   # reconnect then subscriptions will be renewed.
   client.subscribe("/1234/Dev1094905/#")
   client.subscribe("/1234/Dev1094906/#")
   client.subscribe("/1234/Dev1094907/#")


def on_message(client, userdata, msg):
   print(msg.topic + " " + str(msg.payload))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

host="130.206.112.29"
print("Connecting to "+host)
client.connect(host, 1883, 60)

client.loop_forever()
