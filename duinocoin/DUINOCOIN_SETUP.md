# DuinoCoin Mining Setup for ESP32 Cluster

Optimized configuration for mining DuinoCoin with 9x ESP32 boards + KickPi K2B coordinator.

## Overview

**DuinoCoin** is a cryptocurrency designed specifically for low-power devices like Arduino and ESP32 boards. It's eco-friendly, ASIC-resistant, and rewards lower-powered devices fairly.

### Your Mining Rig Specifications

**Hardware:**
- 9x ELEGOO ESP32 DevKit v1 (ESP32-WROOM-32)
- 1x KickPi K2B (monitoring and coordination)

**Expected Performance:**
- **Per ESP32:** 170-180 kH/s (dual-core)
- **Total Cluster:** ~1.53 - 1.62 MH/s
- **Power Draw:** ~13.5W total (1.5W per ESP32)
- **Daily Earnings:** ~90 DUCO/day (10 DUCO per ESP32)

## Mining Approaches

### Option 1: Arduino IDE (C++) - RECOMMENDED ⭐

**Advantages:**
- Highest hashrate (170-180 kH/s per ESP32)
- Dual-core mining with FreeRTOS
- Most efficient
- Official support
- Built-in web dashboard on each ESP32

**Disadvantages:**
- Requires Arduino IDE for flashing
- C++ code (less flexible than Python)

### Option 2: MicroPython

**Advantages:**
- Can use existing MicroPython setup
- Python code (easier to modify)
- Works with Broccoli framework

**Disadvantages:**
- Much slower hashrate (~50-70 kH/s)
- Uses AVR difficulty instead of ESP32
- Less efficient
- Lower earnings

**Recommendation:** Use Arduino/C++ approach for maximum mining efficiency!

## Architecture

```
┌──────────────────────────────────────────┐
│      KickPi K2B (Coordinator)            │
│  • Mining Monitor Dashboard              │
│  • Statistics Aggregator                 │
│  • Hashrate Tracker                      │
│  • Earnings Calculator                   │
│  • Web Interface (Optional)              │
└────────────────┬─────────────────────────┘
                 │
            WiFi Network
                 │
    ┌────────────┼───────────┬────────┐
    │            │           │        │
┌───▼────┐  ┌───▼────┐  ┌───▼────┐  ...
│ ESP32  │  │ ESP32  │  │ ESP32  │  (9 nodes)
│ Miner  │  │ Miner  │  │ Miner  │
│ 170kH/s│  │ 170kH/s│  │ 170kH/s│
└────────┘  └────────┘  └────────┘

Each ESP32:
• Connects to DuinoCoin pool independently
• Reports to local web dashboard (port 80)
• K2B aggregates stats from all miners
```

## Setup Process

### Prerequisites

1. **DuinoCoin Account**
   - Create account at: https://wallet.duinocoin.com
   - Save your username (needed for mining)

2. **Arduino IDE** (for C++ approach)
   ```bash
   # Install Arduino IDE on K2B or your PC
   wget https://downloads.arduino.cc/arduino-1.8.19-linux64.tar.xz
   tar -xf arduino-1.8.19-linux64.tar.xz
   cd arduino-1.8.19
   sudo ./install.sh
   ```

3. **ESP32 Board Support**
   - In Arduino IDE: File → Preferences
   - Add to "Additional Board Manager URLs":
     ```
     https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
     ```
   - Tools → Board → Boards Manager → Search "esp32" → Install

### Step 1: Download DuinoCoin ESP32 Code

```bash
cd /home/user/esp-cluster/duinocoin

# Clone the official repository
git clone https://github.com/duino-coin/duino-coin.git
cd duino-coin/ESP_Code

# The main files are:
# - ESP_Code.ino (main miner code)
# - Settings.h (configuration)
```

### Step 2: Configure Miners

You'll need to configure each ESP32 with:
- Your DuinoCoin username
- Unique rig identifier (ESP32-01, ESP32-02, etc.)
- WiFi credentials
- Optional: Miner key for extra security

**Configuration files are in:** `duinocoin/config/`

### Step 3: Flash ESP32s

For **maximum hashrate**, use the Arduino IDE approach:

1. Open `ESP_Code.ino` in Arduino IDE
2. Edit `Settings.h` with your credentials
3. Select Board: "ESP32 Dev Module"
4. Set CPU Frequency: 240MHz (maximum)
5. Flash to each ESP32
6. Repeat 9 times with unique RIG_IDENTIFIER for each

### Step 4: Setup K2B Monitoring

The K2B will:
- Monitor all 9 miners
- Aggregate statistics
- Display total hashrate and earnings
- Provide web dashboard

## DuinoCoin Mining Settings

### Key Configuration Parameters

```cpp
// In Settings.h

// REQUIRED
#define DUCO_USER "your_username"           // Your DuinoCoin username
#define RIG_IDENTIFIER "ESP32-01"           // Unique name for this miner
#define MINER_KEY "None"                    // Optional security key

// WiFi
#define SSID "YourWiFiName"
#define PASSWORD "YourWiFiPassword"

// Optional Performance Settings
#define BLINK_SHARE_FOUND true              // LED blinks on share found
#define WDT_TIMEOUT 60                      // Watchdog timer (seconds)
#define CORE_AFFINITY 0                     // Which CPU core to use (0 or 1)
```

### Naming Convention for 9 Miners

```
ESP32-Alpha    (Node 1)
ESP32-Beta     (Node 2)
ESP32-Gamma    (Node 3)
ESP32-Delta    (Node 4)
ESP32-Epsilon  (Node 5)
ESP32-Zeta     (Node 6)
ESP32-Eta      (Node 7)
ESP32-Theta    (Node 8)
ESP32-Iota     (Node 9)
```

## Performance Optimization

### 1. CPU Frequency
Set to **240MHz** in Arduino IDE for maximum hashrate:
- Tools → CPU Frequency → 240MHz

### 2. Dual-Core Mining
The official code uses FreeRTOS to mine on both cores:
- Core 0: Mining task
- Core 1: Network communication + web server

### 3. Power Supply
Ensure stable power:
- Use quality USB cables
- 2A power supply per ESP32 recommended
- Avoid USB hubs without external power

### 4. Cooling
ESP32s can get warm when mining:
- Ensure good airflow
- Consider small heatsinks
- Monitor temperature via built-in sensor

### 5. Network Stability
- Use 2.4GHz WiFi (ESP32 doesn't support 5GHz)
- Place near router or use WiFi extender
- Strong signal = better uptime = more shares

## Monitoring & Statistics

### Individual ESP32 Web Dashboard

Each ESP32 runs a web server on port 80:
- Open browser to: `http://ESP32_IP_ADDRESS`
- Shows: Hashrate, accepted shares, uptime, difficulty

### K2B Aggregated Monitoring

The K2B will poll all 9 miners and display:
- Total combined hashrate
- Individual miner status
- Total accepted shares
- Estimated daily earnings
- Uptime statistics

## Expected Earnings

### Per ESP32
- Hashrate: 170-180 kH/s
- Daily: ~10 DUCO
- Monthly: ~300 DUCO
- Power cost: ~1.08 kWh/month @ 1.5W

### Total Cluster (9x ESP32)
- Hashrate: 1.53-1.62 MH/s
- Daily: ~90 DUCO
- Monthly: ~2,700 DUCO
- Power cost: ~9.7 kWh/month @ 13.5W

**Profitability Note:** DuinoCoin is designed for education and fun, not profit. At current rates (~$0.001-0.002 per DUCO), earnings are minimal but power costs are also very low.

## Troubleshooting

### ESP32 Not Mining

1. **Check WiFi connection:**
   - Open Serial Monitor (115200 baud)
   - Should see "Connected to WiFi"

2. **Check pool connection:**
   - Should see "Connected to pool"
   - If not, check internet connectivity

3. **Check username:**
   - Verify DuinoCoin username is correct
   - Must match your wallet username exactly

### Low Hashrate

1. **CPU Frequency:** Ensure set to 240MHz
2. **Interference:** Check WiFi signal strength
3. **Temperature:** ESP32 might be thermal throttling
4. **Code version:** Use latest ESP_Code.ino from repo

### Miner Keeps Disconnecting

1. **Watchdog timer:** Increase `WDT_TIMEOUT` in Settings.h
2. **Power supply:** Use quality power source
3. **WiFi stability:** Move closer to router
4. **Pool issues:** Check duinocoin.com status

## Security Notes

### Miner Key
- Optional but recommended
- Set in your DuinoCoin wallet settings
- Add to `MINER_KEY` in Settings.h
- Prevents unauthorized miners using your username

### Network Security
- ESP32s only connect to duinocoin.com servers
- No incoming connections needed
- Firewall friendly

## Alternative: MicroPython Mining

If you still want to use MicroPython (not recommended for mining):

```bash
# Download ESPython-DUCO-Miner
git clone https://github.com/fabiopolancoe/ESPython-DUCO-Miner.git

# Edit ESPythonMiner.py with your credentials
# Upload to ESP32 using ampy or Thonny

# Note: Much slower than Arduino approach!
# Expected hashrate: 50-70 kH/s instead of 170-180 kH/s
```

## Next Steps

1. Create DuinoCoin account at wallet.duinocoin.com
2. Configure Settings.h templates for your 9 miners
3. Flash all ESP32s with Arduino IDE
4. Setup K2B monitoring dashboard
5. Start mining!

## Useful Links

- **DuinoCoin Official:** https://duinocoin.com
- **Wallet:** https://wallet.duinocoin.com
- **GitHub:** https://github.com/duino-coin/duino-coin
- **Getting Started:** https://duinocoin.com/getting-started.html
- **Discord:** https://discord.gg/k48Ht5y
- **Exchange:** https://exchange.duinocoin.com

## Mining Pools

DuinoCoin uses automatic pool selection:
- Connects to: `server.duinocoin.com/getPool`
- Receives optimal pool based on location
- Automatic failover if pool goes down

No manual pool configuration needed!

---

Happy Mining! ⛏️💰
