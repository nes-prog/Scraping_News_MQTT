import paho.mqtt.client as mqtt
import time
import ast
import pymongo

#create database
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["database_news"]
#create collection 
mycol = mydb["News"]

def on_connect(rc):
    ""
    if rc == 0:
         print("Connected to broker")
         global Connected                
         Connected = True               
    else:
         print("Connection failed")


def on_message(client, userdata, message):
    # inject data into mongo db 
    x = mycol.insert_one(ast.literal_eval(message.payload.decode("utf-8")))
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)


Connected = False
broker_address="localhost"
port = 1883                   
 
print("creating first reciever instance")
client = mqtt.Client("python_test")
client.on_message=on_message          #attach function to callback
client.on_connect=on_connect
print("connecting to broker")
client.connect(broker_address, port)  #connect to broker
client.loop_start()                   #start the loop
 
while Connected != True:              #Wait for connection
    time.sleep(0.1)

print("Subscribing to topic","test-/messagenews")
client.subscribe("test-/messagenews")

try:
    while True: 
        time.sleep(1)
except KeyboardInterrupt:
    print("exiting")
    client.disconnect()
    client.loop_stop()
