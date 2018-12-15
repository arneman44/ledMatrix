import paho.mqtt.client as mqtt #import the client1
from switch import switchmessage



def on_message(client, userdata, msg):
    topic = msg.topic
    message = str(msg.payload.decode("utf-8"))
    switchmessage(message,topic)
    print(message)

def on_log(client, userdata, level, buf):
    print("log: ",buf)

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected")
    else:
        print("error connecting ",rc)

def MQTT_start():
    print('192.168.1.225')
    broker_address='192.168.1.225'
    client = mqtt.Client("MATRIX") #create new instance
    client.on_message=on_message #attach function to callback
    client.on_log=on_log
    client.on_connect=on_connect
    print("connecting to broker")
    client.connect(broker_address) #connect to broker
    client.loop_start() #start the loop
    client.subscribe('LEDMATRIX/#')
    client.subscribe('tekst')