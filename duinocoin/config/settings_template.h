/*
   DuinoCoin ESP32 Miner Configuration Template

   This is a template for Settings.h used by the ESP_Code.ino miner.
   Copy this file and customize for each of your 9 ESP32 miners.

   Repository: https://github.com/duino-coin/duino-coin
   Official Setup: https://duinocoin.com/getting-started.html
*/

#ifndef SETTINGS_H
#define SETTINGS_H

// ============================================
// DUINOCOIN ACCOUNT SETTINGS
// ============================================

// Your DuinoCoin username (REQUIRED)
// Create account at: https://wallet.duinocoin.com
#define DUCO_USER "YOUR_USERNAME_HERE"

// Unique identifier for THIS miner (REQUIRED)
// Each ESP32 should have a different name!
// Examples: ESP32-Alpha, ESP32-Beta, ESP32-Gamma, etc.
#define RIG_IDENTIFIER "ESP32-XX"

// Miner key for security (OPTIONAL)
// Generate in wallet settings: https://wallet.duinocoin.com
// Leave as "None" if not using
#define MINER_KEY "None"

// ============================================
// WIFI CONFIGURATION
// ============================================

// Your WiFi credentials
// NOTE: ESP32 only supports 2.4GHz WiFi, not 5GHz!
#define SSID "YOUR_WIFI_SSID"
#define PASSWORD "YOUR_WIFI_PASSWORD"

// ============================================
// PERFORMANCE SETTINGS
// ============================================

// Enable LED blinking when share is found
// Set to false to save a tiny bit of power
#define BLINK_SHARE_FOUND true

// Watchdog timer timeout in seconds
// Increase if miner keeps resetting
#define WDT_TIMEOUT 60

// Serial baud rate for debugging
#define SERIAL_BAUD 115200

// ============================================
// ADVANCED SETTINGS (Usually don't need to change)
// ============================================

// Which CPU core to run mining on (0 or 1)
// The code uses both cores via FreeRTOS
#define CORE_AFFINITY 0

// Enable OTA (Over-The-Air) updates
// Allows firmware updates via WiFi
#define ENABLE_OTA true

// Hostname for mDNS (local network name)
// Will be accessible at: http://HOSTNAME.local
#define HOSTNAME RIG_IDENTIFIER

// Web server port for statistics dashboard
#define WEB_SERVER_PORT 80

// ============================================
// OPTIONAL: TEMPERATURE MONITORING
// ============================================

// Enable if you have DS18B20 temperature sensor connected
#define USE_DS18B20 false
#define DS18B20_PIN 4

// Enable if you have DHT sensor connected
#define USE_DHT false
#define DHT_PIN 5
#define DHT_TYPE DHT22

// ============================================
// POOL SETTINGS (Automatic - Don't change)
// ============================================

// DuinoCoin uses automatic pool selection
// The miner will connect to: https://server.duinocoin.com/getPool
// and receive the best pool for your location
// No manual configuration needed!

#endif // SETTINGS_H

/*
   QUICK SETUP CHECKLIST:

   1. ✓ Replace YOUR_USERNAME_HERE with your DuinoCoin username
   2. ✓ Set unique RIG_IDENTIFIER for this ESP32 (e.g., ESP32-01)
   3. ✓ Enter your WiFi SSID and PASSWORD
   4. ✓ Optional: Add MINER_KEY for security
   5. ✓ Save and upload to ESP32

   EXPECTED PERFORMANCE:
   - Hashrate: 170-180 kH/s (dual-core ESP32)
   - Power: ~1.5W
   - Daily earnings: ~10 DUCO

   WEB DASHBOARD:
   - Access at: http://ESP32_IP_ADDRESS
   - Shows: Hashrate, shares, uptime, difficulty
*/
