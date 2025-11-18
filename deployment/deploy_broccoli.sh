#!/bin/bash
# Deploy Broccoli cluster code to all ESP32 nodes
# This script uploads the necessary Python files to each ESP32

set -e

echo "=========================================="
echo "ESP32 Cluster - Deploy Broccoli Code"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check dependencies
if ! command -v ampy &> /dev/null; then
    echo -e "${RED}Error: ampy not found${NC}"
    echo "Install with: pip3 install adafruit-ampy"
    exit 1
fi

# Check if config files exist
if [ ! -f "../config/config_wifi_params.py" ]; then
    echo -e "${RED}Error: config_wifi_params.py not found${NC}"
    echo "Please create and configure ../config/config_wifi_params.py"
    exit 1
fi

if [ ! -f "../config/config_mqtt_params.py" ]; then
    echo -e "${RED}Error: config_mqtt_params.py not found${NC}"
    echo "Please create and configure ../config/config_mqtt_params.py"
    exit 1
fi

echo -e "${YELLOW}Configuration files found${NC}"
echo ""

# Function to deploy to a single ESP32
deploy_to_esp32() {
    local port=$1
    local node_name=$2

    echo "=========================================="
    echo -e "${GREEN}Deploying to $node_name on $port${NC}"
    echo "=========================================="

    if [ ! -e "$port" ]; then
        echo -e "${RED}Error: Port $port not found${NC}"
        return 1
    fi

    # Set ampy port
    export AMPY_PORT="$port"
    export AMPY_BAUD=115200

    echo "Uploading configuration files..."
    ampy put ../config/config_wifi_params.py /config_wifi_params.py
    ampy put ../config/config_mqtt_params.py /config_mqtt_params.py

    echo "Uploading Broccoli node files..."
    ampy put ../codes/broccoli/micropython/boot.py /boot.py
    ampy put ../codes/broccoli/micropython/main.py /main.py

    if [ -f "../codes/broccoli/micropython/config_hardware.py" ]; then
        ampy put ../codes/broccoli/micropython/config_hardware.py /config_hardware.py
    fi

    # Upload node code (if exists in repository)
    if [ -f "../codes/broccoli/node/cluster_node.py" ]; then
        echo "Uploading cluster node code..."
        ampy put ../codes/broccoli/node/cluster_node.py /cluster_node.py
        ampy put ../codes/broccoli/node/cluster_broker.py /cluster_broker.py
    fi

    # Upload additional node modules (we'll need to check what exists)
    if [ -f "../codes/broccoli/node/node.py" ]; then
        ampy put ../codes/broccoli/node/node.py /node.py
    fi

    echo "Listing files on ESP32..."
    ampy ls

    echo ""
    echo -e "${GREEN}✓ $node_name deployment complete${NC}"
    echo ""
    sleep 1
}

# Interactive deployment
echo -e "${YELLOW}Deploy Broccoli to ESP32 Nodes${NC}"
echo ""
echo "This script will deploy the cluster code to your ESP32 boards."
echo "Connect each ESP32 one at a time and press Enter."
echo ""

NODE_NUM=1
while true; do
    echo -e "${YELLOW}Ready to deploy to ESP32 Node #$NODE_NUM${NC}"
    echo "Connect ESP32 and press Enter (or 'q' to quit): "
    read -r response

    if [[ "$response" == "q" ]] || [[ "$response" == "Q" ]]; then
        break
    fi

    # Find the first available port
    for port in /dev/ttyUSB* /dev/ttyACM*; do
        if [ -e "$port" ]; then
            deploy_to_esp32 "$port" "ESP32-Node-$NODE_NUM"
            NODE_NUM=$((NODE_NUM + 1))
            break
        fi
    done

    echo ""
    echo "Disconnect this ESP32 and connect the next one"
    echo ""
done

echo ""
echo "=========================================="
echo -e "${GREEN}✓ Deployment Complete!${NC}"
echo "=========================================="
echo ""
echo "Total nodes deployed: $((NODE_NUM - 1))"
echo ""
echo "Next steps:"
echo "1. Power on all ESP32 nodes"
echo "2. They will auto-connect to WiFi and MQTT broker"
echo "3. Run the Python client to test the cluster"
echo ""
