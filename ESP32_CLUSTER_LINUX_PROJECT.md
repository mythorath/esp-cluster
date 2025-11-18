# ESP32 Cluster Linux Project
**Goal**: Build an expandable ESP32 cluster that can run Linux through distributed computing and emulation

## Hardware Inventory
- 9x ESP32 Dev1 (WROOM) - ELEGOO 3PCS ESP-32 Development Board USB-C
  - Dual-core Xtensa LX6 @ 240MHz
  - 520KB SRAM
  - 4MB Flash (typical)
  - WiFi + Bluetooth
  - I2C, SPI, UART support
- 1x ESP8266MOD
  - Single-core @ 80MHz
  - 80KB DRAM
  - Limited use, possibly for monitoring/logging

## Architecture Options

### Option 1: Distributed RISC-V Emulation (RECOMMENDED)
Leverage existing open-source RISC-V emulators that run on ESP32, enhanced with cluster computing:

**Master Node** (1x ESP32):
- Runs mini-rv32ima or TinyEMU RISC-V emulator
- Boots actual Linux kernel (RISC-V RV32IMA)
- Coordinates cluster operations
- Handles CPU emulation core

**Memory Nodes** (3x ESP32):
- Each provides 4MB flash as "RAM extension"
- Fast I2C communication to master
- Acts as distributed memory pages
- Swap/paging system over I2C bus

**Compute Workers** (4x ESP32):
- Handle specific syscalls offloaded from master
- Run MicroPython tasks via Broccoli framework
- Process-specific operations (crypto, compression, etc.)
- Network I/O operations

**Monitor Node** (1x ESP32):
- System monitoring and logging
- Cluster health checks
- Serial console interface

**Logger** (ESP8266):
- Basic logging to external storage
- Watchdog timer

### Option 2: Virtual Distributed Linux OS
Create a "Linux-compatible" environment where syscalls are distributed:

**Components**:
- `/proc`, `/sys` emulation distributed across nodes
- VFS (Virtual File System) spanning cluster storage
- Process scheduler distributed across worker nodes
- Network stack using native ESP32 WiFi
- Custom "init" system coordinating cluster

### Option 3: Hybrid Beowulf-Style Cluster
Traditional cluster approach with MicroPython:

**Features**:
- MPI-like message passing (via MQTT/I2C)
- Distributed task queue (existing Broccoli)
- Shared file system over network
- Python-based "userland" (MicroPython)
- Optional: Single master node running RISC-V Linux for coordination

## Communication Architecture

### Multi-tier Networking:

1. **I2C Bus** (High-speed local cluster):
   - Connect 4-6 ESP32s on same I2C bus
   - Master-slave configuration
   - Used for memory operations, fast IPC
   - Speed: up to 400kHz (Fast Mode) or 1MHz (Fast Mode Plus)
   - See: https://randomnerdtutorials.com/esp32-i2c-master-slave-arduino/

2. **WiFi/MQTT** (Distributed operations):
   - Existing Broccoli framework
   - Task distribution
   - Remote procedure calls
   - File transfer

3. **UART** (Optional peer-to-peer):
   - Direct ESP32-to-ESP32 communication
   - Backup communication channel

### Topology:
```
                    [Master Node - Linux Emulator]
                              |
        +----I2C--------------+---------------I2C----+
        |                     |                      |
   [Memory 1]            [Memory 2]             [Memory 3]

                    [MQTT Broker/Network]
                              |
        +----------+----------+----------+-----------+
        |          |          |          |           |
    [Worker1]  [Worker2]  [Worker3]  [Worker4]  [Monitor]

                         [ESP8266 Logger]
```

## Existing Assets (Broccoli Framework)

Already available in this repo:
- ✅ Distributed task queue system
- ✅ MQTT-based communication
- ✅ Celery-like Canvas operations (chain, group, chord, map, chunks)
- ✅ Dynamic function deployment
- ✅ Symmetrical node architecture
- ✅ MicroPython support

## Implementation Phases

### Phase 1: Foundation (Week 1-2)
- [ ] Set up I2C cluster (4 ESP32s on I2C bus)
- [ ] Test I2C master-slave communication
- [ ] Enhance Broccoli for hybrid I2C+MQTT
- [ ] Create basic memory sharing over I2C

### Phase 2: Linux Emulation Core (Week 3-4)
- [ ] Port mini-rv32ima to master ESP32
- [ ] Implement distributed memory access
- [ ] Create memory paging to I2C slaves
- [ ] Boot minimal Linux kernel

### Phase 3: Cluster Integration (Week 5-6)
- [ ] Offload syscalls to worker nodes
- [ ] Implement distributed file system
- [ ] Network stack integration
- [ ] Process scheduling across cluster

### Phase 4: Optimization (Week 7-8)
- [ ] Performance tuning
- [ ] Memory optimization
- [ ] Task distribution balancing
- [ ] Monitoring and debugging tools

## Technical Challenges & Solutions

### Challenge 1: Limited RAM
**Problem**: ESP32 has only 520KB SRAM, Linux needs more
**Solutions**:
- Use 4MB flash as swap (slower but viable)
- Distribute memory pages across I2C slaves
- Highly compressed initramfs
- Minimal kernel config (< 2MB)

### Challenge 2: Slow Emulation
**Problem**: RISC-V emulation on Xtensa is slow
**Solutions**:
- Offload specific operations to workers
- Optimize hot paths in emulator
- Use dual-core effectively
- Cache frequently used memory pages

### Challenge 3: I2C Bandwidth
**Problem**: I2C may bottleneck memory access
**Solutions**:
- Use Fast Mode Plus (1MHz)
- Implement smart caching
- Predict memory access patterns
- Use SPI for high-bandwidth slaves

## Development Tools & Resources

### Required:
- Arduino IDE or PlatformIO
- ESP32 toolchain
- Python 3.x (for client scripts)
- MQTT broker (Mosquitto)

### Key Libraries:
- Broccoli (existing in repo)
- mini-rv32ima (RISC-V emulator)
- esp32-i2c libraries
- MicroPython firmware

### References:
1. [mini-rv32ima RISC-V emulator](https://github.com/cnlohr/mini-rv32ima)
2. [ESP32 I2C Tutorial](https://randomnerdtutorials.com/esp32-i2c-master-slave-arduino/)
3. [Broccoli Framework](https://github.com/Wei1234c/Broccoli)
4. [ESP32 TinyEMU](https://github.com/drorgl/esp32-tinyemu)
5. [Linux on M5Stack](https://github.com/verylowfreq/linux_on_m5stack)

## Performance Expectations

### Realistic Goals:
- Boot time: 30-60 seconds
- Emulation speed: ~1-5 MIPS (very slow)
- Usable for: Demonstration, education, simple scripts
- Not suitable for: Heavy computation, real-time tasks

### Stretch Goals:
- Distributed compilation (distcc-like)
- Multi-user support (why not?)
- Network services (tiny web server)
- Container support (really pushing it!)

## Why This Is Fun

This project is "stupid but fun" because:
1. **Educational**: Learn about OS internals, emulation, distributed systems
2. **Challenging**: Solve real engineering constraints
3. **Unique**: Few people have built ESP32 Linux clusters
4. **Expandable**: Can grow from 2 to 100+ nodes
5. **Cheap**: Total cost ~$70 for full cluster
6. **Conversation Starter**: "Yeah, I run Linux on $7 microcontrollers"

## Success Criteria

### Minimum Viable Product:
- [ ] Linux kernel boots on master ESP32
- [ ] Can execute basic commands (ls, echo, cat)
- [ ] At least 3 nodes working together
- [ ] Demonstrable distributed memory

### Stretch Goals:
- [ ] Full 9-node cluster operational
- [ ] Python interpreter running
- [ ] Simple web server
- [ ] Distributed task execution from Linux shell
- [ ] Custom init system coordinating all nodes

## Next Steps

1. Set up I2C communication between ESP32s
2. Test Broccoli framework with current hardware
3. Port mini-rv32ima emulator to ESP32
4. Implement distributed memory manager
5. Boot Linux!

---

**Remember**: The journey is more important than the destination. Even if we can't get full Linux running, building the distributed infrastructure and learning about the limitations is incredibly valuable!
