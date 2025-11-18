# DuinoCoin Mining on ESP32 Cluster

This directory contains everything you need to set up DuinoCoin mining on your 9x ESP32 cluster.

## What is DuinoCoin?

**DuinoCoin (DUCO)** is a cryptocurrency specifically designed for low-power devices like Arduino boards and ESP32 microcontrollers. It's:

- ⚡ **Eco-friendly** - Low power consumption
- 🎯 **ASIC-resistant** - Designed for microcontrollers
- 📚 **Educational** - Great for learning about crypto
- 🌐 **Accessible** - Mine with devices you already have
- 💚 **Fair** - Rewards lower-powered devices appropriately

## Quick Stats for Your 9x ESP32 Cluster

| Metric | Value |
|--------|-------|
| **Total Hashrate** | 1.53-1.62 MH/s |
| **Per ESP32** | 170-180 kH/s |
| **Power Consumption** | ~13.5W total |
| **Daily Earnings** | ~90 DUCO |
| **Monthly Earnings** | ~2,700 DUCO |
| **Setup Time** | ~2 hours |

## Directory Structure

```
duinocoin/
├── README.md                          # This file
├── DUINOCOIN_SETUP.md                # Detailed setup guide
├── QUICKSTART_DUINOCOIN.md           # Quick start guide
│
├── config/                            # Configuration files
│   ├── miner_configs.json            # Cluster configuration
│   └── settings_template.h           # ESP32 Settings.h template
│
├── scripts/                           # Setup and deployment scripts
│   ├── setup_duinocoin.sh           # Initial setup script
│   └── flash_helper.py              # Auto-generate configs
│
├── monitor/                           # Monitoring tools
│   ├── cluster_monitor.py           # Terminal-based monitor
│   └── web_dashboard.py             # Web dashboard (Flask)
│
└── generated_configs/                 # Auto-generated (after running flash_helper.py)
    ├── Settings_ESP32-Alpha.h
    ├── Settings_ESP32-Beta.h
    └── ... (one for each miner)
```

## Quick Start

### 1. Create DuinoCoin Account
→ https://wallet.duinocoin.com

### 2. Run Setup Script
```bash
cd scripts
./setup_duinocoin.sh
```

### 3. Configure Miners
```bash
# Edit with your credentials
nano config/miner_configs.json

# Generate Settings.h files
python3 scripts/flash_helper.py
```

### 4. Flash ESP32s
- Open `duino-coin/ESP_Code/ESP_Code.ino` in Arduino IDE
- For each ESP32:
  - Copy the corresponding Settings.h from `generated_configs/`
  - Set Board to "ESP32 Dev Module"
  - Set CPU Frequency to "240MHz"
  - Upload

### 5. Start Monitoring
```bash
# Web dashboard (recommended)
python3 monitor/web_dashboard.py
# Access at: http://YOUR_K2B_IP:5000

# OR terminal monitor
python3 monitor/cluster_monitor.py
```

## Detailed Guides

- **[QUICKSTART_DUINOCOIN.md](QUICKSTART_DUINOCOIN.md)** - Fast setup in ~2 hours
- **[DUINOCOIN_SETUP.md](DUINOCOIN_SETUP.md)** - Complete setup guide with troubleshooting

## Configuration Example

**miner_configs.json:**
```json
{
  "duinocoin_username": "your_username",
  "wifi": {
    "ssid": "YourWiFi",
    "password": "YourPassword"
  },
  "miners": [
    {
      "id": 1,
      "rig_identifier": "ESP32-Alpha",
      "expected_hashrate": "170-180 kH/s"
    },
    ...
  ]
}
```

## Monitoring Options

### 1. Web Dashboard (Recommended)
Beautiful real-time dashboard with:
- Total cluster hashrate
- Individual miner status
- Share acceptance rates
- Earnings estimates

```bash
python3 monitor/web_dashboard.py
```

### 2. Terminal Monitor
Text-based monitoring:
```bash
python3 monitor/cluster_monitor.py --interval 10
```

### 3. Individual ESP32 Dashboards
Each ESP32 has its own web interface at `http://ESP32_IP`

## Expected Performance

### Per ESP32
- **Hashrate:** 170-180 kH/s (dual-core @ 240MHz)
- **Power:** ~1.5W
- **Daily:** ~10 DUCO
- **Uptime:** 24/7 (with stable WiFi)

### 9-Node Cluster
- **Hashrate:** 1.53-1.62 MH/s total
- **Power:** ~13.5W total
- **Daily:** ~90 DUCO
- **Monthly:** ~2,700 DUCO
- **Cost:** ~10 kWh/month (~$1.20 electricity)

## Why DuinoCoin for ESP32?

### ✅ Perfect Match
- ESP32 is officially supported
- Optimized DUCO-S1 algorithm
- Fair difficulty for ESP32 hardware
- Active community and development

### ✅ Better than Other Mining
- Can't mine Bitcoin/Ethereum on ESP32 (impossible)
- DUCO is specifically designed for microcontrollers
- Actually earns tokens (not just hashing for nothing)
- Low power = eco-friendly

### ✅ Educational Value
- Learn about cryptocurrency
- Understand mining and blockchain
- Distributed systems in practice
- Hardware optimization techniques

## Troubleshooting

### WiFi Issues
- ESP32 only supports 2.4GHz WiFi
- Check signal strength
- Verify SSID/password are correct

### Low Hashrate
- Ensure CPU frequency is 240MHz
- Check power supply (need 2A)
- Monitor temperature (may throttle if hot)

### No Shares Accepted
- Verify username matches wallet
- Check internet connection
- Wait for difficulty adjustment (takes time)

### Miner Offline
- Check Serial Monitor for errors
- Verify WiFi connection
- Restart ESP32
- Check pool status

See **[DUINOCOIN_SETUP.md](DUINOCOIN_SETUP.md)** for detailed troubleshooting.

## Optimization Tips

1. **Power Supply**
   - Use quality 2A USB adapters
   - Avoid long/thin USB cables
   - Consider powered USB hub

2. **Cooling**
   - Ensure good airflow
   - Small heatsinks help
   - Don't stack ESP32s

3. **Network**
   - Strong WiFi signal crucial
   - Use 2.4GHz channel 1, 6, or 11
   - WiFi extender if needed

4. **Monitoring**
   - Check daily for offline miners
   - Monitor acceptance rate (>95% is good)
   - Track earnings in wallet

## Useful Links

- **Official Site:** https://duinocoin.com
- **Wallet:** https://wallet.duinocoin.com
- **GitHub:** https://github.com/duino-coin/duino-coin
- **Discord:** https://discord.gg/k48Ht5y
- **Exchange:** https://exchange.duinocoin.com
- **Getting Started:** https://duinocoin.com/getting-started.html

## Alternative: Distributed Computing

If you're not interested in mining, this cluster can also be used for:
- Distributed computing (Broccoli framework)
- Monte Carlo simulations
- MapReduce operations
- Parallel algorithms

See the main repository README for distributed computing examples.

## Support

- **Questions?** Join the DuinoCoin Discord
- **Issues?** Check troubleshooting guide
- **Improvements?** Contributions welcome!

---

Happy Mining! ⛏️💎

Transform your 9x ESP32s into a distributed mining cluster!
