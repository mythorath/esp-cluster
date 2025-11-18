#!/usr/bin/env python3
"""
ESP32 Cluster Node Configuration
Defines the configuration for each ESP32 node in the cluster
"""

# List of ESP32 nodes in your cluster
# Each node will be assigned a unique ID based on its MAC address
# You can give them friendly names here

CLUSTER_NODES = {
    'node_1': {
        'name': 'ESP32-Alpha',
        'description': 'Primary compute node',
        'port': '/dev/ttyUSB0',  # USB port when connected
    },
    'node_2': {
        'name': 'ESP32-Beta',
        'description': 'Secondary compute node',
        'port': '/dev/ttyUSB1',
    },
    'node_3': {
        'name': 'ESP32-Gamma',
        'description': 'Tertiary compute node',
        'port': '/dev/ttyUSB2',
    },
    'node_4': {
        'name': 'ESP32-Delta',
        'description': 'Node 4',
        'port': '/dev/ttyUSB3',
    },
    'node_5': {
        'name': 'ESP32-Epsilon',
        'description': 'Node 5',
        'port': '/dev/ttyUSB4',
    },
    'node_6': {
        'name': 'ESP32-Zeta',
        'description': 'Node 6',
        'port': '/dev/ttyUSB5',
    },
    'node_7': {
        'name': 'ESP32-Eta',
        'description': 'Node 7',
        'port': '/dev/ttyUSB6',
    },
    'node_8': {
        'name': 'ESP32-Theta',
        'description': 'Node 8',
        'port': '/dev/ttyUSB7',
    },
    'node_9': {
        'name': 'ESP32-Iota',
        'description': 'Node 9',
        'port': '/dev/ttyUSB8',
    },
}

# MicroPython firmware
MICROPYTHON_FIRMWARE = 'ESP32_GENERIC-20231005-v1.21.0.bin'
FIRMWARE_URL = 'https://micropython.org/resources/firmware/ESP32_GENERIC-20231005-v1.21.0.bin'

# Broccoli files to deploy to each ESP32
BROCCOLI_FILES = [
    '../codes/broccoli/micropython/boot.py',
    '../codes/broccoli/micropython/main.py',
    '../codes/broccoli/micropython/config_hardware.py',
    '../codes/broccoli/micropython/webrepl_cfg.py',
    '../config/config_wifi_params.py',
    '../config/config_mqtt_params.py',
]

# Additional dependencies (installed via mpremote/ampy)
DEPENDENCIES = [
    'umqtt.simple',
    'umqtt.robust',
]
