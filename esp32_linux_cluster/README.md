# ESP32 Linux Cluster - Firmware

This directory contains the firmware for each node type in the ESP32 Linux cluster.

## Node Types

### 1. Master Node (`master_node/`)
- **Quantity**: 1x ESP32
- **Role**: Runs RISC-V emulator, coordinates cluster
- **Connections**: I2C master, WiFi/MQTT
- **Functions**:
  - CPU emulation core
  - Distributed memory management
  - Cluster coordination
  - MQTT/Broccoli integration

### 2. Memory Nodes (`memory_node/`)
- **Quantity**: 3x ESP32
- **Role**: Distributed RAM/storage
- **Connections**: I2C slaves (addresses 0x10, 0x11, 0x12)
- **Functions**:
  - Store memory pages
  - Fast SRAM cache
  - SPIFFS-based virtual memory
  - Handle read/write commands

### 3. Worker Nodes (`worker_node/`) [Coming Soon]
- **Quantity**: 4x ESP32
- **Role**: Distributed task execution
- **Connections**: WiFi/MQTT
- **Functions**:
  - Execute syscall offloads
  - MicroPython tasks
  - Network I/O
  - Crypto/compression operations

### 4. Monitor Node (`monitor_node/`) [Coming Soon]
- **Quantity**: 1x ESP32
- **Role**: System monitoring
- **Connections**: WiFi/MQTT
- **Functions**:
  - Cluster health monitoring
  - Performance metrics
  - Serial console interface

## Hardware Setup

### I2C Cluster Wiring

Connect the ESP32s in an I2C bus configuration:

```
Master Node (ESP32 #1):
  GPIO21 (SDA) ----+---- Memory Node 1 GPIO21 (SDA)
                   |
                   +---- Memory Node 2 GPIO21 (SDA)
                   |
                   +---- Memory Node 3 GPIO21 (SDA)

  GPIO22 (SCL) ----+---- Memory Node 1 GPIO22 (SCL)
                   |
                   +---- Memory Node 2 GPIO22 (SCL)
                   |
                   +---- Memory Node 3 GPIO22 (SCL)

  GND ------------ Common Ground (all nodes)
```

**Important Notes**:
- Use pull-up resistors on SDA and SCL lines (4.7kΩ recommended)
- Keep I2C wires as short as possible (< 20cm for best results)
- All ESP32s must share a common ground
- Total bus capacitance should be < 400pF for 400kHz operation

### I2C Address Assignment

Each memory node must have a unique address. Edit `memory_node.ino`:

```cpp
// Memory Node 1:
#define NODE_ADDRESS 0x10

// Memory Node 2:
#define NODE_ADDRESS 0x11

// Memory Node 3:
#define NODE_ADDRESS 0x12
```

### WiFi Configuration

Edit both `master_node.ino` and worker nodes with your WiFi credentials:

```cpp
const char* WIFI_SSID = "your_wifi_name";
const char* WIFI_PASS = "your_wifi_password";
const char* MQTT_BROKER = "192.168.1.100";  // IP of MQTT broker
```

## Installation Steps

### Prerequisites

1. **Arduino IDE** (1.8.19 or newer) OR **PlatformIO**
2. **ESP32 Board Support**:
   - In Arduino IDE: File → Preferences → Additional Board Manager URLs
   - Add: `https://dl.espressif.com/dl/package_esp32_index.json`
   - Tools → Board → Boards Manager → Install "ESP32"
3. **Required Libraries**:
   - Wire (built-in)
   - WiFi (built-in)
   - SPIFFS (built-in)
   - PubSubClient (install from Library Manager)

### Flashing the Firmware

#### Master Node (1x ESP32):

1. Open `master_node/master_node.ino` in Arduino IDE
2. Configure WiFi settings
3. Select board: "ESP32 Dev Module"
4. Select correct COM port
5. Upload

#### Memory Nodes (3x ESP32):

For each of the 3 memory nodes:

1. Open `memory_node/memory_node.ino`
2. **IMPORTANT**: Set unique address:
   - Node 1: `#define NODE_ADDRESS 0x10`
   - Node 2: `#define NODE_ADDRESS 0x11`
   - Node 3: `#define NODE_ADDRESS 0x12`
3. Upload to each ESP32
4. Label each board with its address!

### Testing the Setup

1. **Wire the I2C bus** as shown above
2. **Power on all nodes**
3. **Connect to Master Node** via Serial Monitor (115200 baud)
4. You should see:
   ```
   ╔════════════════════════════════════╗
   ║  ESP32 LINUX CLUSTER - MASTER NODE ║
   ╚════════════════════════════════════╝
   I2C initialized (SDA:21, SCL:22, 400kHz)

   === Discovering Memory Nodes ===
   ✓ Memory Node 0 (0x10) - ONLINE
   ✓ Memory Node 1 (0x11) - ONLINE
   ✓ Memory Node 2 (0x12) - ONLINE

   === Testing Distributed Memory ===
   Writing test data... OK
   Reading test data... OK
   Data: Hello from ESP32 Linux Cluster!
   ✓ Memory test PASSED!
   ```

5. **Check each memory node** serial output to see read/write operations

## Troubleshooting

### Memory nodes not discovered

- Check I2C wiring (SDA, SCL, GND)
- Verify each memory node has unique address
- Add pull-up resistors (4.7kΩ) to SDA and SCL
- Check for loose connections
- Reduce I2C frequency to 100kHz: `#define I2C_FREQ 100000`

### I2C communication errors

- Shorten I2C wire lengths
- Check for ground loops
- Lower I2C frequency
- Verify power supply is stable (use separate 5V supply if needed)

### Memory test fails

- Check memory node serial output for errors
- Verify SPIFFS initialized correctly
- Try reformatting SPIFFS: `SPIFFS.format()`

### WiFi won't connect

- Double-check SSID and password
- Ensure 2.4GHz WiFi (ESP32 doesn't support 5GHz)
- Check if network uses WPA2 (WPA3 may not work)

## Performance Notes

### Expected Performance:

- **I2C Speed**: 400kHz (Fast Mode)
  - ~40 KB/s theoretical throughput
  - ~20-30 KB/s practical with overhead
- **Memory Access**:
  - SRAM cache: ~1-2 µs
  - SPIFFS: ~100-500 µs
- **Distributed Memory**:
  - I2C overhead: ~100-200 µs per operation
  - Total latency: 100 µs - 1 ms depending on cache

### Optimization Tips:

1. **Cache locality**: Access memory sequentially when possible
2. **Batch operations**: Combine multiple small reads/writes
3. **Use Fast Mode Plus**: Increase to 1MHz if your wiring supports it
4. **Optimize SPIFFS**: Use larger block sizes for sequential access

## Next Steps

1. ✅ Basic I2C cluster communication
2. ✅ Distributed memory system
3. ⏳ Port RISC-V emulator (mini-rv32ima)
4. ⏳ Implement memory paging
5. ⏳ Boot Linux kernel
6. ⏳ Add worker nodes for syscall offloading
7. ⏳ Integrate with Broccoli framework

## Architecture Overview

```
                    ┌─────────────────┐
                    │  Master Node    │
                    │  (RISC-V EMU)   │
                    └────────┬────────┘
                             │
        ┌──────I2C───────────┼──────────────┐
        │                    │              │
   ┌────▼────┐          ┌────▼────┐   ┌────▼────┐
   │ Memory  │          │ Memory  │   │ Memory  │
   │ Node 1  │          │ Node 2  │   │ Node 3  │
   │ (0x10)  │          │ (0x11)  │   │ (0x12)  │
   └─────────┘          └─────────┘   └─────────┘

                  ┌───────────────┐
                  │ WiFi/MQTT Bus │
                  └───────┬───────┘
                          │
      ┌──────────┬────────┼────────┬─────────┐
      │          │        │        │         │
  ┌───▼───┐  ┌───▼───┐ ┌─▼──┐  ┌──▼──┐  ┌───▼────┐
  │Worker │  │Worker │ │Work│  │Work │  │Monitor │
  │  #1   │  │  #2   │ │er#3│  │er#4 │  │  Node  │
  └───────┘  └───────┘ └────┘  └─────┘  └────────┘
```

## Resources

- [ESP32 I2C Tutorial](https://randomnerdtutorials.com/esp32-i2c-master-slave-arduino/)
- [mini-rv32ima RISC-V Emulator](https://github.com/cnlohr/mini-rv32ima)
- [Broccoli Framework](https://github.com/Wei1234c/Broccoli)
- [Project Documentation](../ESP32_CLUSTER_LINUX_PROJECT.md)

## License

This project builds upon the Broccoli framework. See [LICENSE](../LICENSE) for details.

---

**Have fun building your Linux cluster on $7 microcontrollers! 🥦🐧**
