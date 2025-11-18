# Hardware Bill of Materials (BOM)

## What You Already Have ✅

- 9x ESP32 Dev1 (WROOM) - ELEGOO ESP-32 Development Board USB-C
- 1x ESP8266MOD

## What You Need to Buy 🛒

### Essential Components:

| Item | Quantity | Est. Cost | Purpose |
|------|----------|-----------|---------|
| **Pull-up Resistors** (4.7kΩ) | 2-4pcs | $1 | I2C bus stability |
| **Breadboard** (830 points) or larger | 2-3pcs | $10 | Prototyping I2C cluster |
| **Jumper Wires** (M-M) | 30-40pcs | $5 | I2C connections |
| **USB Cables** (USB-C) | 9pcs | $20 | Power + programming |
| **5V Power Supply** (multi-port) | 1pc | $25 | Power all ESP32s simultaneously |

**Total Essential: ~$60**

### Optional but Recommended:

| Item | Quantity | Est. Cost | Purpose |
|------|----------|-----------|---------|
| **Logic Analyzer** (e.g., Saleae clone) | 1pc | $10-60 | Debug I2C communication |
| **OLED Display** (0.96" I2C) | 1-2pcs | $10 | Status display |
| **SD Card Module** (SPI) | 1-3pcs | $5 | Additional storage for Linux filesystem |
| **Level Shifter** (if using 5V devices) | 1pc | $3 | I2C voltage conversion |
| **Enclosure/Case** | 1pc | $15 | Professional mounting |
| **Cooling Fans** (5V) | 2-3pcs | $10 | If running continuously |

**Total with Optional: ~$110**

### Future Expansion:

| Item | Quantity | Est. Cost | Purpose |
|------|----------|-----------|---------|
| **Additional ESP32s** | 10-20pcs | $70-140 | Expand cluster |
| **Raspberry Pi 4** (4GB) | 1pc | $55 | MQTT broker + coordinator |
| **Network Switch** (5-port) | 1pc | $15 | If using Ethernet adapters |

## Power Requirements

### Per ESP32:
- Voltage: 3.3V (via USB 5V regulator)
- Current: 80mA (idle) - 250mA (WiFi active)
- Peak: 500mA (during boot/transmission)

### For 9x ESP32 Cluster:
- **Idle**: ~0.7A @ 5V = 3.5W
- **Active**: ~2.25A @ 5V = 11.25W
- **Peak**: ~4.5A @ 5V = 22.5W

### Recommended Power Supply:
- **Option 1**: USB multi-port charger (60W+, 12A total)
  - Examples: Anker PowerPort 10, RAVPower 60W
  - Cost: $25-40
- **Option 2**: Bench power supply (5V 5A)
  - Good for development/debugging
  - Cost: $30-50
- **Option 3**: Individual USB chargers
  - Use existing phone chargers
  - Cost: $0 (if you have enough)

## I2C Wiring Details

### Pull-up Resistor Placement:

```
                  +3.3V
                    │
                    ├─── 4.7kΩ ────┐
                    │               │
                    └─── 4.7kΩ ──┐ │
                                 │ │
                                 │ │
Master SDA ──────────────────────┘ │
Memory1 SDA ────────────┘           │
Memory2 SDA ──────┘                 │
Memory3 SDA ──┘                     │
                                    │
Master SCL ──────────────────────────┘
Memory1 SCL ────────────┘
Memory2 SCL ──────┘
Memory3 SCL ──┘

Master GND ──────────────────────────
Memory1 GND ────────────┘
Memory2 GND ──────┘
Memory3 GND ──┘
```

**Note**: Only ONE set of pull-up resistors needed for entire I2C bus!

## Breadboard Layout (Suggested)

### Breadboard 1: I2C Cluster (Master + 3 Memory Nodes)

```
Power Rails:
[+] ─── 3.3V (from USB or regulator)
[-] ─── GND

         ESP32 #1 (Master)
         [21] ─── SDA bus
         [22] ─── SCL bus
         [GND]─── GND rail

         ESP32 #2 (Memory 0x10)
         [21] ─── SDA bus
         [22] ─── SCL bus
         [GND]─── GND rail

         ESP32 #3 (Memory 0x11)
         [21] ─── SDA bus
         [22] ─── SCL bus
         [GND]─── GND rail

         ESP32 #4 (Memory 0x12)
         [21] ─── SDA bus
         [22] ─── SCL bus
         [GND]─── GND rail

Pull-up resistors:
SDA ─── 4.7kΩ ─── 3.3V
SCL ─── 4.7kΩ ─── 3.3V
```

### Breadboard 2: Worker Nodes (WiFi/MQTT only)

```
ESP32 #5-8: Just power and ground
No I2C connections needed
Connect via WiFi/MQTT
```

## Shopping Links (US)

### Amazon:
- **ESP32 Development Boards**: Search "ESP32 DevKit C"
- **Resistor Kit**: Search "resistor assortment kit"
- **Breadboard Kit**: Search "solderless breadboard jumper wire"
- **USB Multi-Port Charger**: Search "Anker USB charger 60W"

### AliExpress (Cheaper, longer shipping):
- **ESP32**: ~$3-4 per board
- **Components**: Resistors, breadboards, wires in bulk
- **Total savings**: ~40-50% vs Amazon

### Local Electronics Store:
- Pull-up resistors (RadioShack, Micro Center, Fry's)
- Breadboards and jumper wires
- Same-day availability!

## Assembly Time Estimate

- **Basic setup** (1 master + 3 memory): 30-60 minutes
- **Full cluster** (9 nodes): 2-3 hours
- **Troubleshooting**: 1-2 hours (first time)
- **Total first build**: 3-5 hours

## Safety Notes

⚠️ **Important**:
- ESP32s are 3.3V logic - do NOT connect 5V directly to GPIO pins
- USB power is fine (has voltage regulator)
- Don't exceed 12mA per GPIO pin
- Total current draw from 3.3V pin: max 600mA
- Always connect GND first, disconnect last
- Use anti-static precautions when handling boards

## Maintenance

- **Expected lifespan**: 10,000+ hours of continuous operation
- **Common issues**:
  - Loose breadboard connections (solder for permanent setup)
  - USB cable wear (use strain relief)
  - Flash wear (SPIFFS has limited write cycles, ~10,000-100,000)

## Upgrade Path

### Phase 1: Basic Cluster ($60)
- 1 master + 3 memory nodes via I2C
- WiFi for Broccoli tasks

### Phase 2: Full Cluster ($70)
- Add 4 worker nodes
- Add monitoring node
- Full distributed system

### Phase 3: Enhanced ($150)
- Add SD card modules for more storage
- OLED displays for status
- Custom PCB for permanent mounting
- Cooling system

### Phase 4: Mega Cluster ($300+)
- 20+ ESP32 nodes
- Raspberry Pi coordinator
- Rack-mount enclosure
- Proper power distribution

---

## Quick Shopping Checklist

```
[ ] 4.7kΩ resistors (at least 2)
[ ] Breadboard (2-3 pieces)
[ ] Jumper wires (M-M, 40 pack minimum)
[ ] USB-C cables (9 total)
[ ] Multi-port USB power supply (or 9 individual chargers)
[ ] (Optional) Logic analyzer
[ ] (Optional) OLED displays
[ ] (Optional) SD card modules
```

**You're ready to build when all boxes are checked!** ✅
