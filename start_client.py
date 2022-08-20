import argparse
import time
from threading import Thread

import paho.mqtt.client as mqtt

if __name__ == "__main__":
    time.sleep(1)  # Give the mqtt broker a second to initialize
    parser = argparse.ArgumentParser(description='Process args to setup mqtt client.')
    parser.add_argument('--name', type=str, help='Name of the client.')
    parser.add_argument('--address', type=str, help='The mqtt broker ip address to connect to.')
    parser.add_argument('--port', type=int, help='The mqtt broker port to connect to.')
    parser.add_argument('--delay', type=int, help='The delay in seconds to publish data.', default=1)
    parser.add_argument('--subscribe_topics', type=list, nargs='*', default=[])
    parser.add_argument('--publish_topic', type=str, help='The topic to publish.')
    parser.add_argument('--payload', type=str, help='The payload to publish.')
    args, _ = parser.parse_known_args()


    def on_message(_client, userdata, message):
        message = str(message.payload.decode("utf-8"))
        print(f"{args.name} Received from client at {_client._host}, userdata {userdata}, message: {message}")


    def publisher(_client, delay, publish_topic, payload):
        while True:
            _client.publish(topic=publish_topic, payload=payload)
            print(f"{args.name} Published topic {publish_topic} payload {payload}")
            time.sleep(delay)


    client = mqtt.Client(args.name)
    client.connect(host=args.address, port=args.port)
    client.on_message = on_message
    for topic in args.subscribe_topics:
        topic = "".join(topic)
        print(f"{args.name} subscribed to topic {topic}")
        client.subscribe(topic)
    publisher_thread = Thread(target=publisher, args=(client, args.delay, args.publish_topic, args.payload))
    publisher_thread.start()
    client.loop_forever()
