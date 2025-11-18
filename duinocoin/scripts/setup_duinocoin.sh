#!/bin/bash
# Setup script for DuinoCoin mining on ESP32 cluster
# Run this on your KickPi K2B or development machine

set -e

echo "=========================================="
echo "DuinoCoin ESP32 Cluster Setup"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo -e "${RED}Warning: This script is optimized for Linux${NC}"
fi

echo -e "${GREEN}Step 1: Installing Arduino IDE...${NC}"
echo ""

# Check if Arduino IDE is already installed
if command -v arduino &> /dev/null; then
    echo -e "${GREEN}✓ Arduino IDE already installed${NC}"
else
    echo "Downloading Arduino IDE..."
    ARDUINO_VERSION="1.8.19"
    wget -q --show-progress https://downloads.arduino.cc/arduino-${ARDUINO_VERSION}-linux64.tar.xz

    echo "Extracting..."
    tar -xf arduino-${ARDUINO_VERSION}-linux64.tar.xz

    echo "Installing..."
    cd arduino-${ARDUINO_VERSION}
    sudo ./install.sh
    cd ..

    echo "Cleaning up..."
    rm arduino-${ARDUINO_VERSION}-linux64.tar.xz

    echo -e "${GREEN}✓ Arduino IDE installed${NC}"
fi

echo ""
echo -e "${GREEN}Step 2: Cloning DuinoCoin repository...${NC}"

if [ -d "duino-coin" ]; then
    echo "Repository already exists, updating..."
    cd duino-coin
    git pull
    cd ..
else
    git clone https://github.com/duino-coin/duino-coin.git
fi

echo -e "${GREEN}✓ Repository cloned${NC}"

echo ""
echo -e "${GREEN}Step 3: Installing Python dependencies for monitoring...${NC}"

pip3 install flask requests

echo -e "${GREEN}✓ Python dependencies installed${NC}"

echo ""
echo -e "${GREEN}Step 4: Setting up configuration...${NC}"

# Create config directory if it doesn't exist
mkdir -p ../config

echo ""
echo -e "${YELLOW}================================${NC}"
echo -e "${YELLOW}Manual Configuration Required${NC}"
echo -e "${YELLOW}================================${NC}"
echo ""
echo "Please configure the following files:"
echo ""
echo "1. ${GREEN}duino-coin/ESP_Code/Settings.h${NC}"
echo "   - Set your DuinoCoin username"
echo "   - Set WiFi credentials"
echo "   - Configure for each ESP32 with unique RIG_IDENTIFIER"
echo ""
echo "2. ${GREEN}../config/miner_configs.json${NC}"
echo "   - Update with your DuinoCoin username"
echo "   - Update WiFi SSID and password"
echo ""
echo "Template available at: ${GREEN}../config/settings_template.h${NC}"
echo ""

echo -e "${GREEN}Step 5: Installing ESP32 board support for Arduino IDE...${NC}"
echo ""
echo "Open Arduino IDE and:"
echo "1. File → Preferences"
echo "2. Add to 'Additional Board Manager URLs':"
echo "   ${GREEN}https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json${NC}"
echo "3. Tools → Board → Boards Manager"
echo "4. Search 'esp32' and install 'ESP32 by Espressif Systems'"
echo "5. Tools → Board → Select 'ESP32 Dev Module'"
echo "6. Tools → CPU Frequency → Select '240MHz'"
echo ""

echo ""
echo "=========================================="
echo -e "${GREEN}✓ Setup Complete!${NC}"
echo "=========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Create DuinoCoin account:"
echo "   → https://wallet.duinocoin.com"
echo ""
echo "2. Configure ESP32 miners:"
echo "   → Edit duino-coin/ESP_Code/Settings.h"
echo "   → Use template: duinocoin/config/settings_template.h"
echo ""
echo "3. Flash ESP32s:"
echo "   → Open duino-coin/ESP_Code/ESP_Code.ino in Arduino IDE"
echo "   → Configure Settings.h for each miner"
echo "   → Upload to each ESP32 (repeat 9 times)"
echo ""
echo "4. Start monitoring:"
echo "   → python3 duinocoin/monitor/cluster_monitor.py"
echo "   → python3 duinocoin/monitor/web_dashboard.py"
echo ""
echo "Web dashboard will be at: http://YOUR_K2B_IP:5000"
echo ""
