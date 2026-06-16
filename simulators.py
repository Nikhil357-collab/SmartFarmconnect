import random
import json
import time
import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
TOPIC = "smartfarm/node1"

client = mqtt.Client()

client.connect(BROKER,1883,60)

print("Publishing Smart Farm Data...")

while True:

    soil = random.randint(1000,3500)

    temp = round(random.uniform(22,38),1)

    hum = round(random.uniform(40,90),1)

    light = random.randint(200,1000)

    pump = "ON" if soil < 1800 else "OFF"

    payload = {
        "soil":soil,
        "temperature":temp,
        "humidity":hum,
        "light":light,
        "pump":pump
    }

    client.publish(TOPIC,json.dumps(payload))

    print(payload)
    
    time.sleep(5)