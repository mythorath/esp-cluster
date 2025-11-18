#!/usr/bin/env python3
"""
DuinoCoin ESP32 Flash Helper
Generates Settings.h files for each of the 9 miners with unique configurations
"""

import json
import os
from typing import Dict

SETTINGS_TEMPLATE = """/*
   DuinoCoin ESP32 Miner Configuration
   Auto-generated for: {rig_identifier}
   Generated: {timestamp}
*/

#ifndef SETTINGS_H
#define SETTINGS_H

// ============================================
// DUINOCOIN ACCOUNT SETTINGS
// ============================================

#define DUCO_USER "{username}"
#define RIG_IDENTIFIER "{rig_identifier}"
#define MINER_KEY "{miner_key}"

// ============================================
// WIFI CONFIGURATION
// ============================================

#define SSID "{ssid}"
#define PASSWORD "{password}"

// ============================================
// PERFORMANCE SETTINGS
// ============================================

#define BLINK_SHARE_FOUND true
#define WDT_TIMEOUT 60
#define SERIAL_BAUD 115200

// ============================================
// ADVANCED SETTINGS
// ============================================

#define CORE_AFFINITY 0
#define ENABLE_OTA true
#define HOSTNAME "{rig_identifier}"
#define WEB_SERVER_PORT 80

// ============================================
// TEMPERATURE MONITORING (Optional)
// ============================================

#define USE_DS18B20 false
#define DS18B20_PIN 4
#define USE_DHT false
#define DHT_PIN 5
#define DHT_TYPE DHT22

#endif // SETTINGS_H

/*
   Configuration for: {rig_identifier}
   Expected hashrate: 170-180 kH/s
   Expected daily earnings: ~10 DUCO
   Power consumption: ~1.5W

   Web dashboard: http://{rig_identifier}.local or http://ESP32_IP
*/
"""


class ConfigGenerator:
    """Generate Settings.h files for all miners"""

    def __init__(self, config_file: str = "../config/miner_configs.json"):
        self.config = self.load_config(config_file)
        self.output_dir = "../generated_configs"

    def load_config(self, config_file: str) -> Dict:
        """Load miner configuration"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Config file not found: {config_file}")
            print("Please configure duinocoin/config/miner_configs.json first")
            exit(1)

    def generate_settings(self):
        """Generate Settings.h for all miners"""
        os.makedirs(self.output_dir, exist_ok=True)

        username = self.config.get('duinocoin_username', 'YOUR_USERNAME_HERE')
        wifi_ssid = self.config['wifi']['ssid']
        wifi_password = self.config['wifi']['password']
        miner_key = self.config.get('miner_key', 'None')

        if username == 'YOUR_USERNAME_HERE':
            print("ERROR: Please set your DuinoCoin username in miner_configs.json")
            return False

        if wifi_ssid == 'YOUR_WIFI_SSID':
            print("ERROR: Please set your WiFi credentials in miner_configs.json")
            return False

        print("=" * 60)
        print("Generating Settings.h files for ESP32 miners")
        print("=" * 60)
        print()

        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for miner in self.config['miners']:
            rig_id = miner['rig_identifier']

            # Generate settings file content
            settings_content = SETTINGS_TEMPLATE.format(
                rig_identifier=rig_id,
                username=username,
                miner_key=miner_key,
                ssid=wifi_ssid,
                password=wifi_password,
                timestamp=timestamp
            )

            # Write to file
            output_file = os.path.join(
                self.output_dir,
                f"Settings_{rig_id}.h"
            )

            with open(output_file, 'w') as f:
                f.write(settings_content)

            print(f"✓ Generated: {output_file}")

        print()
        print("=" * 60)
        print("✓ All configuration files generated!")
        print("=" * 60)
        print()
        print("Next steps:")
        print()
        print("For each ESP32:")
        print("  1. Open duino-coin/ESP_Code/ESP_Code.ino in Arduino IDE")
        print(f"  2. Copy Settings_{rig_id}.h over the original Settings.h")
        print("  3. Select Board: ESP32 Dev Module")
        print("  4. Select CPU Frequency: 240MHz")
        print("  5. Select Port: /dev/ttyUSBX (your ESP32)")
        print("  6. Click Upload")
        print()
        print("Repeat for all 9 miners with their respective Settings files")
        print()

        return True

    def generate_deployment_script(self):
        """Generate bash script to help with deployment"""
        script_content = """#!/bin/bash
# Auto-generated deployment helper script

echo "DuinoCoin ESP32 Deployment Helper"
echo "=================================="
echo ""
echo "This script will help you flash all 9 ESP32 miners"
echo ""

"""

        for i, miner in enumerate(self.config['miners'], 1):
            rig_id = miner['rig_identifier']
            script_content += f"""
echo "Ready to flash: {rig_id} (Miner {i}/9)"
echo "1. Copy generated_configs/Settings_{rig_id}.h to duino-coin/ESP_Code/Settings.h"
echo "2. Connect {rig_id} to USB"
echo "3. Open Arduino IDE"
echo "4. Select the correct port"
echo "5. Click Upload"
echo ""
read -p "Press Enter when done, or 'q' to quit: " response
if [[ "$response" == "q" ]]; then
    exit 0
fi
"""

        script_content += """
echo ""
echo "✓ All miners configured!"
echo ""
echo "Start monitoring with:"
echo "  python3 duinocoin/monitor/cluster_monitor.py"
echo ""
"""

        script_file = os.path.join(self.output_dir, "deploy_helper.sh")
        with open(script_file, 'w') as f:
            f.write(script_content)

        os.chmod(script_file, 0o755)
        print(f"✓ Generated deployment helper: {script_file}")


def main():
    print()
    print("=" * 60)
    print("DuinoCoin ESP32 Configuration Generator")
    print("=" * 60)
    print()

    generator = ConfigGenerator()

    if generator.generate_settings():
        generator.generate_deployment_script()
        print()
        print("Configuration files are ready!")
        print(f"Location: {generator.output_dir}/")
        print()


if __name__ == '__main__':
    main()
