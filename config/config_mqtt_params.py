# MQTT Configuration for ESP32 Cluster
# This file configures how ESP32 nodes connect to the MQTT broker

# MQTT Broker Configuration
# TODO: Replace with your KickPi K2B's IP address
BROKER_HOST = '192.168.1.100'  # Change to your K2B's IP address

# Cluster Group Name
GROUP_NAME = 'esp32_cluster'

# MQTT Authentication (optional)
# If you set up authentication on Mosquitto, configure here
USERNAME = None  # or 'your_mqtt_username'
PASSWORD = None  # or 'your_mqtt_password'

# Example with authentication:
# USERNAME = 'esp32'
# PASSWORD = 'cluster123'
