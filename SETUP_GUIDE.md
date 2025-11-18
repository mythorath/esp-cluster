# ESP32 Cluster Setup Guide
## Your Hardware Configuration

**Available Hardware:**
- 9x ELEGOO ESP32 Development Boards (ESP-32 DevKit v1 WROOM, USB-C, CP2102)
- 1x ESP8266 module
- 1x KickPi K2B (Linux SBC)

## Architecture Overview

You already have the **Broccoli** framework - a distributed task queue system for ESP32 clusters that mimics Celery Canvas! This is exactly what you need for creating a "Beowulf-like" cluster.

### Important Reality Check

**ESP32s CANNOT run Linux** - they are microcontrollers with:
- Xtensa LX6 dual-core @ 240MHz
- 520KB SRAM
- They run FreeRTOS (via MicroPython or Arduino)

**However**, you CAN create a powerful distributed computing cluster where:
- The **KickPi K2B** acts as the **master node** (running Linux)
- The **9x ESP32s** act as **worker nodes** (distributed compute)
- They communicate via **MQTT over WiFi**
- You can dispatch parallel tasks like a Beowulf cluster!

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    KickPi K2B (Master)                       │
│  - MQTT Broker (Mosquitto)                                  │
│  - Python Client (Task Dispatcher)                          │
│  - Result Collector                                         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ WiFi Network
                     │ (MQTT Protocol)
                     │
    ┌────────────────┼────────────────┐
    │                │                │
┌───▼────┐      ┌───▼────┐      ┌───▼────┐
│ ESP32  │      │ ESP32  │ ...  │ ESP32  │  (9 nodes)
│ Node 1 │      │ Node 2 │      │ Node 9 │
│        │      │        │      │        │
│Worker+ │      │Worker+ │      │Worker+ │
│Broker  │      │Broker  │      │Broker  │
└────────┘      └────────┘      └────────┘
```

### Each ESP32 Node is:
- **Broker** + **Task Queue** + **Worker** (symmetric architecture)
- Can receive and execute tasks
- Can communicate with other nodes
- Runs MicroPython

### What You Can Do (Celery Canvas-like operations):

1. **Chains** - Sequential operations: `((4+4) * 8) * 10 = 640`
2. **Groups** - Parallel operations: Distribute tasks across 9 ESP32s
3. **Chords** - Parallel then reduce: MapReduce pattern
4. **Map/Starmap** - Apply function to list elements
5. **Chunks** - Split large datasets across workers

## Setup Steps

### Step 1: Set Up KickPi K2B (Master Node)

1. **Install MQTT Broker (Mosquitto)**
   ```bash
   sudo apt update
   sudo apt install mosquitto mosquitto-clients -y
   sudo systemctl enable mosquitto
   sudo systemctl start mosquitto
   ```

2. **Verify MQTT is running**
   ```bash
   mosquitto -v
   netstat -tuln | grep 1883
   ```

3. **Install Python dependencies**
   ```bash
   sudo apt install python3-pip -y
   pip3 install paho-mqtt
   ```

### Step 2: Flash MicroPython to ESP32s

1. **Install esptool**
   ```bash
   pip3 install esptool
   ```

2. **Download MicroPython firmware**
   ```bash
   wget https://micropython.org/resources/firmware/ESP32_GENERIC-20231005-v1.21.0.bin
   ```

3. **Flash each ESP32** (repeat for all 9 boards)
   ```bash
   # Erase flash
   esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash

   # Flash MicroPython
   esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 ESP32_GENERIC-20231005-v1.21.0.bin
   ```

### Step 3: Configure WiFi Settings

Create a configuration file for your WiFi network that will be deployed to all ESP32s.

### Step 4: Deploy Broccoli Code to ESP32s

Use `ampy` (Adafruit MicroPython tool) to upload the Broccoli worker code to each ESP32.

### Step 5: Start the Cluster!

1. Power on all ESP32s (they auto-connect to WiFi and MQTT broker)
2. Run the Python client on K2B to dispatch tasks
3. Watch them process in parallel!

## Use Cases

### Perfect For:
- **Parallel numerical computations** (Monte Carlo simulations)
- **Distributed sensor processing** (IoT data aggregation)
- **MapReduce operations** (word counting, data analysis)
- **Embarrassingly parallel problems** (parameter sweeps, rendering)
- **Distributed hash cracking** (educational/authorized only)
- **Genetic algorithms** (parallel evolution)

### Not Ideal For:
- CPU-intensive single-threaded tasks (use K2B's CPU instead)
- Large memory operations (520KB SRAM per ESP32)
- Tasks requiring OS-level features (no Linux on ESP32)

## Performance Expectations

**Single ESP32:**
- Dual-core @ 240MHz
- ~520KB usable RAM
- ~100-200 MIPS

**9x ESP32 Cluster:**
- 18 cores total
- ~4.6MB combined RAM
- ~900-1800 MIPS (theoretical aggregate)

**Comparison:**
- Raspberry Pi 4: 4-core @ 1.5GHz, 1-8GB RAM
- Your cluster: More cores, distributed, lower per-node performance

## Next Steps

Ready to proceed? I'll create:
1. Configuration files for your network
2. Deployment scripts for all 9 ESP32s
3. Example tasks to demonstrate cluster computing
4. Automated setup scripts

What would you like to tackle first?
