#!/bin/bash
# Flash MicroPython to all ESP32 nodes
# This script will erase and flash MicroPython firmware to each ESP32

set -e

echo "=========================================="
echo "ESP32 Cluster - Flash MicroPython"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Firmware settings
FIRMWARE_FILE="ESP32_GENERIC-20231005-v1.21.0.bin"
FIRMWARE_URL="https://micropython.org/resources/firmware/ESP32_GENERIC-20231005-v1.21.0.bin"

# Check if firmware exists
if [ ! -f "$FIRMWARE_FILE" ]; then
    echo -e "${YELLOW}Downloading MicroPython firmware...${NC}"
    wget "$FIRMWARE_URL"
fi

# Check if esptool is installed
if ! command -v esptool.py &> /dev/null; then
    echo -e "${RED}Error: esptool.py not found${NC}"
    echo "Install with: pip3 install esptool"
    exit 1
fi

echo -e "${GREEN}Firmware ready: $FIRMWARE_FILE${NC}"
echo ""

# Function to flash a single ESP32
flash_esp32() {
    local port=$1
    local node_name=$2

    echo "=========================================="
    echo -e "${GREEN}Flashing $node_name on $port${NC}"
    echo "=========================================="

    if [ ! -e "$port" ]; then
        echo -e "${RED}Error: Port $port not found${NC}"
        echo "Please connect the ESP32 and try again"
        return 1
    fi

    echo "Step 1: Erasing flash..."
    esptool.py --chip esp32 --port "$port" erase_flash

    echo ""
    echo "Step 2: Flashing MicroPython..."
    esptool.py --chip esp32 --port "$port" --baud 460800 write_flash -z 0x1000 "$FIRMWARE_FILE"

    echo ""
    echo -e "${GREEN}✓ $node_name flashed successfully${NC}"
    echo ""
    sleep 2
}

# Interactive mode
echo -e "${YELLOW}Flash ESP32 Nodes${NC}"
echo ""
echo "This script will flash MicroPython to your ESP32 boards."
echo "Connect each ESP32 one at a time and press Enter."
echo ""

# Default ports (auto-detect)
ESP32_PORTS=(/dev/ttyUSB* /dev/ttyACM*)

if [ ${#ESP32_PORTS[@]} -eq 0 ]; then
    echo -e "${RED}No USB devices found${NC}"
    echo "Please connect an ESP32 and try again"
    exit 1
fi

echo "Detected USB ports:"
for port in "${ESP32_PORTS[@]}"; do
    if [ -e "$port" ]; then
        echo "  - $port"
    fi
done
echo ""

# Flash each node
NODE_NUM=1
while true; do
    echo -e "${YELLOW}Ready to flash ESP32 Node #$NODE_NUM${NC}"
    echo "Connect ESP32 and press Enter (or 'q' to quit): "
    read -r response

    if [[ "$response" == "q" ]] || [[ "$response" == "Q" ]]; then
        break
    fi

    # Find the first available port
    for port in /dev/ttyUSB* /dev/ttyACM*; do
        if [ -e "$port" ]; then
            flash_esp32 "$port" "ESP32-Node-$NODE_NUM"
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
echo -e "${GREEN}✓ Flashing Complete!${NC}"
echo "=========================================="
echo ""
echo "Total nodes flashed: $((NODE_NUM - 1))"
echo ""
echo "Next step: Run ./deployment/deploy_broccoli.sh to deploy cluster code"
echo ""
