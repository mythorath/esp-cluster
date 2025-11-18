# DuinoCoin Mining Quick Start

Get your 9x ESP32 DuinoCoin mining cluster running in under 2 hours!

## What You'll Get

- **Hashrate:** 1.53-1.62 MH/s (9x ESP32 @ 170-180 kH/s each)
- **Power:** ~13.5W total
- **Earnings:** ~90 DUCO/day
- **Each ESP32:** Built-in web dashboard for monitoring

## Prerequisites

- 9x ESP32 Development Boards (ELEGOO ESP-32 DevKit v1)
- 1x KickPi K2B or any Linux PC (for monitoring)
- USB cables
- 2.4GHz WiFi network
- DuinoCoin account

## Quick Setup (5 Steps)

### Step 1: Create DuinoCoin Account (5 minutes)

1. Go to: https://wallet.duinocoin.com
2. Click "Register"
3. Save your username (you'll need it for mining)
4. Optional: Generate a miner key for security

### Step 2: Install Arduino IDE (10 minutes)

**On Linux (K2B or PC):**
```bash
cd /home/user/esp-cluster/duinocoin/scripts
./setup_duinocoin.sh
```

**Or manually:**
1. Download: https://www.arduino.cc/en/software
2. Install Arduino IDE
3. Add ESP32 board support:
   - File → Preferences
   - Additional Board Manager URLs:
     ```
     https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
     ```
   - Tools → Board → Boards Manager → Search "esp32" → Install

### Step 3: Configure Miners (15 minutes)

**Option A: Auto-generate (Recommended)**

1. Edit `duinocoin/config/miner_configs.json`:
   ```json
   {
     "duinocoin_username": "YourUsername",
     "wifi": {
       "ssid": "YourWiFiName",
       "password": "YourWiFiPassword"
     }
   }
   ```

2. Generate configs:
   ```bash
   cd duinocoin/scripts
   python3 flash_helper.py
   ```

   This creates 9 Settings.h files in `generated_configs/`

**Option B: Manual**

Copy `duinocoin/config/settings_template.h` and edit for each miner:
```cpp
#define DUCO_USER "YourUsername"
#define RIG_IDENTIFIER "ESP32-Alpha"  // Unique per miner!
#define SSID "YourWiFi"
#define PASSWORD "YourPassword"
```

### Step 4: Flash ESP32s (60 minutes)

**For each of the 9 ESP32s:**

1. **Copy Settings.h**
   - If auto-generated: Copy `generated_configs/Settings_ESP32-Alpha.h` → `duino-coin/ESP_Code/Settings.h`
   - If manual: Use your edited Settings.h

2. **Open in Arduino IDE**
   - File → Open → `duino-coin/ESP_Code/ESP_Code.ino`

3. **Configure Board**
   - Tools → Board → "ESP32 Dev Module"
   - Tools → CPU Frequency → "240MHz (WiFi/BT)"
   - Tools → Flash Frequency → "80MHz"
   - Tools → Upload Speed → "921600"

4. **Select Port**
   - Tools → Port → `/dev/ttyUSB0` (or your ESP32's port)

5. **Upload**
   - Click Upload button (→)
   - Wait for "Done uploading"

6. **Verify Mining**
   - Open Serial Monitor (115200 baud)
   - Should see:
     ```
     Connected to WiFi
     Connected to pool
     Share accepted!
     ```

7. **Repeat for next ESP32**
   - Disconnect this one
   - Connect next one
   - Use next Settings file (ESP32-Beta, Gamma, etc.)

### Step 5: Monitor Your Cluster (5 minutes)

**Option A: Web Dashboard (Recommended)**

```bash
cd duinocoin/monitor
python3 web_dashboard.py
```

Access at: `http://YOUR_K2B_IP:5000`

**Option B: Terminal Monitor**

```bash
cd duinocoin/monitor
python3 cluster_monitor.py
```

**Option C: Individual Miners**

Each ESP32 has its own web interface:
- Find ESP32 IP in Serial Monitor or router
- Open browser: `http://ESP32_IP_ADDRESS`

## Expected Results

After flashing all 9 ESP32s, you should see:

```
DuinoCoin ESP32 Cluster Monitor
================================

📊 CLUSTER SUMMARY
Miners Online:       9/9
Total Hashrate:      1570.5 kH/s (1.571 MH/s)
Average Hashrate:    174.5 kH/s per miner
Accepted Shares:     1234
Rejected Shares:     5
Acceptance Rate:     99.60%
Est. Daily Earnings: ~90 DUCO
Est. Monthly:        ~2700 DUCO

⛏️  INDIVIDUAL MINERS
ESP32-Alpha    | 🟢 ONLINE | 175.2 kH/s | Shares:  142 | Uptime:  3h
ESP32-Beta     | 🟢 ONLINE | 173.8 kH/s | Shares:  138 | Uptime:  3h
ESP32-Gamma    | 🟢 ONLINE | 176.1 kH/s | Shares:  145 | Uptime:  3h
...
```

## Troubleshooting

### ESP32 Won't Connect to WiFi

1. **Check WiFi band:** ESP32 only supports 2.4GHz, NOT 5GHz
2. **Check credentials:** SSID and password must be exact
3. **Signal strength:** Move closer to router
4. **Serial monitor:** Check for error messages

### Low Hashrate

**Expected:** 170-180 kH/s per ESP32

**If lower:**
- Check CPU frequency is set to 240MHz
- Ensure stable power supply (use 2A USB adapters)
- Check temperature (ESP32 might throttle if hot)
- Update to latest ESP_Code from GitHub

### Shares Not Accepted

1. **Username wrong:** Must match wallet exactly
2. **Pool connection:** Check internet connectivity
3. **Difficulty:** Should auto-adjust, give it time
4. **Miner key:** If set, must match wallet settings

### Miner Keeps Resetting

1. **Power supply:** Use quality 2A USB adapter
2. **USB cable:** Try different cable
3. **Watchdog timer:** Increase `WDT_TIMEOUT` in Settings.h
4. **WiFi stability:** Check signal strength

### Can't Find ESP32 IP Address

**Method 1: Serial Monitor**
- Open Serial Monitor in Arduino IDE
- Should print IP on connection

**Method 2: Router Admin**
- Log into router admin panel
- Look for devices with hostname like "ESP32-Alpha"

**Method 3: mDNS**
- Access via: `http://ESP32-Alpha.local`
- (Works on Linux/Mac, requires Bonjour on Windows)

## Performance Tips

### 1. Optimize Power Supply
- Use quality 2A USB adapters (not 500mA)
- Avoid long/thin USB cables
- Consider powered USB hub for all 9 miners

### 2. Improve Cooling
- Ensure good airflow around ESP32s
- Consider small heatsinks on ESP32 chips
- Don't stack ESP32s without spacing

### 3. Network Optimization
- Strong WiFi signal = better uptime = more shares
- Use WiFi extender if needed
- 2.4GHz band, channel 1, 6, or 11 recommended

### 4. Monitor Regularly
- Check web dashboard daily
- Look for offline miners
- Monitor acceptance rate (should be >95%)

## Earnings Calculator

**Current Rates (approximate):**
- ESP32 hashrate: 170 kH/s
- Daily per ESP32: ~10 DUCO
- DUCO price: ~$0.001-0.002 USD

**Your 9-Node Cluster:**
- Total hashrate: ~1.53 MH/s
- Daily: ~90 DUCO (~$0.09-0.18 USD)
- Monthly: ~2,700 DUCO (~$2.70-5.40 USD)
- Power cost: ~10 kWh/month @ 13.5W
- @ $0.12/kWh = ~$1.20/month

**Profitability:** Educational/fun, not profitable
**But:** Low power, eco-friendly, supports decentralization!

## Advanced: OTA Updates

Once miners are deployed, you can update them Over-The-Air:

1. In Arduino IDE: Sketch → Export Compiled Binary
2. Locate `.bin` file
3. Upload via web interface: `http://ESP32_IP/update`
4. Or use `espota.py` tool

This means you don't need to physically access ESP32s to update!

## What's Next?

### Optimization
- Fine-tune difficulty settings
- Experiment with dual-core mining ratios
- Add temperature monitoring
- Implement auto-restart on errors

### Monitoring
- Set up alerts for offline miners
- Log historical hashrate data
- Create grafana dashboard
- Mobile app for monitoring

### Expansion
- Add more ESP32s (easily scalable!)
- Try ESP32-S2 or ESP32-C3 variants
- Add Arduino boards (lower hashrate but supported)
- Experiment with pool mining strategies

## Useful Links

- **DuinoCoin Official:** https://duinocoin.com
- **Wallet:** https://wallet.duinocoin.com
- **GitHub:** https://github.com/duino-coin/duino-coin
- **Exchange:** https://exchange.duinocoin.com
- **Discord:** https://discord.gg/k48Ht5y
- **Reddit:** r/Duinocoin
- **Stats:** https://server.duinocoin.com

## Support & Community

- **Discord:** Join for support and tips
- **GitHub Issues:** Report bugs/problems
- **Reddit:** Share your setup and results
- **Wiki:** https://github.com/duino-coin/duino-coin/wiki

## FAQ

**Q: Is this profitable?**
A: Not really. It's for fun, learning, and supporting the network.

**Q: Can I use ESP8266?**
A: Yes! But slower (~30-50 kH/s). Use the ESP8266 miner code instead.

**Q: Will this damage my ESP32?**
A: No, but they get warm. Good airflow recommended.

**Q: Can I mine while running other code?**
A: Technically yes, but mining uses both cores intensively.

**Q: How does difficulty work?**
A: Auto-adjusts. ESP32s get ESP32 difficulty, not AVR or PC difficulty.

**Q: Can I solo mine or need a pool?**
A: DuinoCoin automatically connects to optimal pool.

**Q: What if DUCO price goes up?**
A: More valuable! But difficulty may increase too.

**Q: Can I sell DUCO?**
A: Yes, on exchanges like exchange.duinocoin.com

---

Happy Mining! ⛏️💎

Your 9x ESP32 cluster is now part of the DuinoCoin network!
