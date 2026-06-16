import json
import requests
import paho.mqtt.client as mqtt
import os
from dotenv import load_dotenv

load_dotenv()

WRITE_API_KEY = os.getenv("WRITE_API_KEY")

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "smartfarm/node1"

def on_connect(client, userdata, flags, rc):

    print("Connected with code:", rc)

    client.subscribe(TOPIC)

    print("Subscribed to:", TOPIC)

def on_message(client, userdata, msg):

    print("\nMessage Received")

    print(msg.payload.decode())

    try:

        data = json.loads(msg.payload.decode())

        payload = {
            "api_key": WRITE_API_KEY,
            "field1": data["soil"],
            "field2": data["temperature"],
            "field3": data["humidity"],
            "field4": data["light"],
            "field5": 1 if data["pump"] == "ON" else 0
        }

        r = requests.post(
            "https://api.thingspeak.com/update",
            data=payload
        )

        print("ThingSpeak Response:", r.text)

    except Exception as e:

        print("ERROR:", e)

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

print("Connecting MQTT...")

client.connect(BROKER, PORT, 60)

client.loop_forever()