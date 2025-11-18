#!/bin/bash
# Setup script for KickPi K2B as cluster master node
# This script installs and configures the MQTT broker and Python dependencies

set -e  # Exit on error

echo "=========================================="
echo "ESP32 Cluster - K2B Master Node Setup"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo -e "${RED}Error: This script must run on Linux (KickPi K2B)${NC}"
    exit 1
fi

echo -e "${GREEN}Step 1: Updating system packages...${NC}"
sudo apt update
sudo apt upgrade -y

echo ""
echo -e "${GREEN}Step 2: Installing MQTT Broker (Mosquitto)...${NC}"
sudo apt install -y mosquitto mosquitto-clients

echo ""
echo -e "${GREEN}Step 3: Configuring Mosquitto...${NC}"
# Create mosquitto config
sudo tee /etc/mosquitto/conf.d/esp32_cluster.conf > /dev/null <<EOF
# ESP32 Cluster Configuration
listener 1883
allow_anonymous true
max_connections 50

# Logging
log_dest file /var/log/mosquitto/mosquitto.log
log_type all

# Persistence
persistence true
persistence_location /var/lib/mosquitto/
EOF

echo ""
echo -e "${GREEN}Step 4: Enabling and starting Mosquitto...${NC}"
sudo systemctl enable mosquitto
sudo systemctl restart mosquitto

echo ""
echo -e "${GREEN}Step 5: Verifying Mosquitto is running...${NC}"
if sudo systemctl is-active --quiet mosquitto; then
    echo -e "${GREEN}✓ Mosquitto is running${NC}"
else
    echo -e "${RED}✗ Mosquitto failed to start${NC}"
    sudo systemctl status mosquitto
    exit 1
fi

echo ""
echo -e "${GREEN}Step 6: Checking MQTT port 1883...${NC}"
if netstat -tuln | grep -q ":1883 "; then
    echo -e "${GREEN}✓ MQTT broker listening on port 1883${NC}"
else
    echo -e "${YELLOW}⚠ Warning: Port 1883 not detected${NC}"
fi

echo ""
echo -e "${GREEN}Step 7: Installing Python dependencies...${NC}"
sudo apt install -y python3-pip python3-dev
pip3 install --upgrade pip
pip3 install paho-mqtt

echo ""
echo -e "${GREEN}Step 8: Installing ESP32 flash tools...${NC}"
pip3 install esptool adafruit-ampy mpremote

echo ""
echo -e "${GREEN}Step 9: Getting K2B IP address...${NC}"
K2B_IP=$(hostname -I | awk '{print $1}')
echo -e "${YELLOW}Your K2B IP address: ${GREEN}$K2B_IP${NC}"
echo ""
echo -e "${YELLOW}IMPORTANT: Update config/config_mqtt_params.py with this IP address:${NC}"
echo -e "${GREEN}BROKER_HOST = '$K2B_IP'${NC}"

echo ""
echo -e "${GREEN}Step 10: Testing MQTT broker...${NC}"
echo "Publishing test message..."
mosquitto_pub -h localhost -t "test/cluster" -m "ESP32 Cluster Master Node Ready"
echo ""
echo "Subscribing to test topic (Ctrl+C to stop)..."
timeout 3 mosquitto_sub -h localhost -t "test/cluster" -v || true

echo ""
echo "=========================================="
echo -e "${GREEN}✓ K2B Master Node Setup Complete!${NC}"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Update config/config_mqtt_params.py with BROKER_HOST = '$K2B_IP'"
echo "2. Update config/config_wifi_params.py with your WiFi credentials"
echo "3. Run ./deployment/flash_esp32_nodes.sh to flash your ESP32s"
echo ""
