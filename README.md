# mqtt_demo

Simple demo to show communication between three clients on three different networks through a mqtt broker.

A mqtt_broker on a docker container is attached to four networks. A management network, network_a, network_b, and network_c.
Three client docker containers client_a, client_b, and client_c connect to the mqtt_broker's ip address on their respective network.
Each client publishes a unique message and receives messages produced by the other two clients.