# ESP32 Cluster - DuinoCoin Mining & Distributed Computing

Mine **DuinoCoin** or run distributed computations on a 9-node ESP32 cluster!

![Cluster Status](https://img.shields.io/badge/Status-Active-green)
![Nodes](https://img.shields.io/badge/Nodes-9x_ESP32-blue)
![Hashrate](https://img.shields.io/badge/Hashrate-1.5_MH/s-orange)
![Power](https://img.shields.io/badge/Power-13.5W-yellow)

## What Is This?

This is a **9-node ESP32 cluster** optimized for:
- **🪙 DuinoCoin Mining** (Primary use - ~90 DUCO/day)
- **💻 Distributed Computing** (Alternative - parallel processing)

Built from:
- **9x ESP32 DevKit v1** boards (dual-core @ 240MHz each)
- **1x KickPi K2B** (coordinator running Linux)
- **WiFi networking** (MQTT for distributed computing, direct pool connection for mining)

## Two Modes of Operation

### Mode 1: DuinoCoin Mining ⛏️ (Recommended)

**What is DuinoCoin?** A cryptocurrency designed specifically for low-power devices like ESP32s!

**Your Cluster Stats:**
- **Hashrate:** 1.53-1.62 MH/s (170-180 kH/s per ESP32)
- **Daily Earnings:** ~90 DUCO
- **Power Usage:** ~13.5W total
- **Setup Time:** ~2 hours

→ **See [duinocoin/QUICKSTART_DUINOCOIN.md](duinocoin/QUICKSTART_DUINOCOIN.md) to start mining!**

### Mode 2: Distributed Computing 💻

Use the **Broccoli framework** for parallel processing tasks:
- Monte Carlo simulations
- MapReduce operations
- Prime searching
- Parallel algorithms

→ **See [QUICKSTART.md](QUICKSTART.md) for distributed computing setup**

**Note:** ESP32s cannot run Linux - they're microcontrollers running MicroPython/Arduino code. The K2B runs Linux and coordinates the cluster.

## Architecture

```
┌──────────────────────────────────────────────┐
│         KickPi K2B (Master Node)             │
│  • MQTT Broker (Mosquitto)                   │
│  • Python Client (Task Dispatcher)           │
│  • Result Aggregator                         │
└────────────────┬─────────────────────────────┘
                 │
            WiFi Network
         (MQTT Protocol Port 1883)
                 │
    ┌────────────┼───────────┬─────────┐
    │            │           │         │
┌───▼───┐   ┌───▼───┐   ┌───▼───┐   ...
│ESP32-1│   │ESP32-2│   │ESP32-9│
│Worker │   │Worker │   │Worker │
└───────┘   └───────┘   └───────┘

Each ESP32: Dual-core @ 240MHz, 520KB RAM
Total: 18 cores, ~4.6MB RAM, ~1800 MIPS
```

## Features

### Celery Canvas-Like Operations

- **Groups** - Parallel execution across workers
- **Chains** - Sequential pipelines (a → b → c)
- **Chords** - MapReduce patterns (parallel map + reduce)
- **Map/Starmap** - Apply functions to lists
- **Chunks** - Batch processing of large datasets

### Capabilities

- **Distributed Computing** - Spread work across 9 nodes
- **Dynamic Code Deployment** - Upload new tasks wirelessly
- **Symmetric Architecture** - Every ESP32 is identical
- **Auto-Discovery** - Nodes auto-connect to cluster
- **Fault Tolerance** - Tasks retry on failure

## Quick Start

### Option A: DuinoCoin Mining (Recommended) ⛏️

```bash
# 1. Create account at https://wallet.duinocoin.com

# 2. Run setup
cd duinocoin/scripts
./setup_duinocoin.sh

# 3. Configure
nano ../config/miner_configs.json  # Add your username & WiFi

# 4. Generate configs
python3 flash_helper.py

# 5. Flash ESP32s with Arduino IDE
# (See duinocoin/QUICKSTART_DUINOCOIN.md)

# 6. Monitor
python3 ../monitor/web_dashboard.py  # Access at http://K2B_IP:5000
```

**→ Full guide:** [duinocoin/QUICKSTART_DUINOCOIN.md](duinocoin/QUICKSTART_DUINOCOIN.md)

### Option B: Distributed Computing 💻

```bash
# 1. Configure WiFi and MQTT
nano config/config_wifi_params.py
nano config/config_mqtt_params.py

# 2. Setup K2B as master
cd deployment
./setup_k2b_master.sh

# 3. Flash MicroPython to ESP32s
./flash_esp32_nodes.sh

# 4. Deploy Broccoli code
./deploy_broccoli.sh

# 5. Test cluster
cd ../examples
python3 test_cluster.py
```

**→ Full guide:** [QUICKSTART.md](QUICKSTART.md)

## Example: Monte Carlo Pi Estimation

```python
from canvas import group
import cluster_tasks as tasks

# Distribute 90,000 iterations across 9 nodes
gp = group([
    tasks.monte_carlo_pi.s(10000)
    for _ in range(9)
])

results = gp.get()
pi_estimate = sum(results) / len(results)
print(f"Pi ≈ {pi_estimate}")
# Pi ≈ 3.14159 (computed across 9 ESP32s in parallel!)
```

## Example: Distributed Prime Counting

```python
from canvas import group
import cluster_tasks as tasks

# Count primes from 1 to 100,000 across cluster
chunk_size = 100000 // 9
gp = group([
    tasks.count_primes_in_range.s(i*chunk_size + 1, (i+1)*chunk_size)
    for i in range(9)
])

total_primes = sum(gp.get())
print(f"Found {total_primes} primes")
```

## Example: MapReduce Word Count

```python
from canvas import chord
import cluster_tasks as tasks

documents = ["doc1 text...", "doc2 text...", ...]

# Map: count words in each document (parallel)
map_group = group([tasks.word_count.s(doc) for doc in documents])

# Reduce: merge all counts (single node)
result = chord(map_group)(tasks.merge_word_counts.s())
word_counts = result.get()
```

## What Can You Do?

### DuinoCoin Mining ⛏️
- **Mine DUCO cryptocurrency** (~90 DUCO/day with 9 ESP32s)
- **Low power consumption** (~13.5W total)
- **Eco-friendly** compared to traditional crypto mining
- **Educational** - Learn about cryptocurrency and mining
- **Actually earns tokens** - Not just theoretical

### Distributed Computing 💻
- **Monte Carlo Simulations** (embarrassingly parallel)
- **Parameter Sweeps** (try many combinations)
- **Distributed Sensors** (IoT data aggregation)
- **Prime Searching** (distributed number theory)
- **Password Cracking** (educational/authorized only!)
- **Genetic Algorithms** (parallel evolution)
- **MapReduce Operations** (word count, data analysis)

### Not Ideal For:
- Single-threaded CPU-intensive tasks
- Large memory operations (520KB per node)
- Traditional cryptocurrency mining (Bitcoin/Ethereum)
- Real-time control (network latency)

## Performance

**Single ESP32:**
- Dual-core Xtensa LX6 @ 240MHz
- 520KB SRAM
- ~100-200 MIPS

**9-Node Cluster:**
- 18 cores total
- ~4.6MB combined RAM
- ~900-1800 MIPS aggregate
- Speedup depends on problem parallelizability

**Comparison:**
- More cores than a Raspberry Pi 4
- Lower per-node performance
- Better for distributed, not centralized workloads

## Project Structure

```
esp-cluster/
├── README.md              # This file
│
├── duinocoin/             # 🪙 DuinoCoin Mining (Primary Use)
│   ├── README.md                  # DuinoCoin overview
│   ├── QUICKSTART_DUINOCOIN.md    # Quick start guide
│   ├── DUINOCOIN_SETUP.md         # Detailed setup guide
│   ├── config/                    # Mining configuration
│   │   ├── miner_configs.json    # Cluster configuration
│   │   └── settings_template.h   # ESP32 Settings.h template
│   ├── scripts/                   # Setup & deployment
│   │   ├── setup_duinocoin.sh    # Install Arduino IDE, etc.
│   │   └── flash_helper.py       # Auto-generate configs
│   └── monitor/                   # Monitoring tools
│       ├── cluster_monitor.py    # Terminal monitor
│       └── web_dashboard.py      # Web dashboard
│
├── QUICKSTART.md          # Distributed computing quick start
├── SETUP_GUIDE.md         # Distributed computing detailed guide
│
├── config/                # Distributed computing config
│   ├── config_wifi_params.py      # WiFi credentials
│   └── config_mqtt_params.py      # MQTT broker settings
│
├── deployment/            # Distributed computing deployment
│   ├── setup_k2b_master.sh        # Setup K2B master node
│   ├── flash_esp32_nodes.sh       # Flash MicroPython
│   ├── deploy_broccoli.sh         # Deploy cluster code
│   └── node_config.py             # Node definitions
│
├── codes/broccoli/        # Broccoli framework (original)
│   ├── client/            # Client code for master
│   ├── node/              # Node/worker code
│   ├── micropython/       # ESP32 MicroPython code
│   └── config/            # Framework configuration
│
└── examples/              # Distributed computing examples
    ├── README.md          # Examples documentation
    ├── cluster_tasks.py   # Task definitions
    └── test_cluster.py    # Comprehensive test suite
```

## Documentation

### DuinoCoin Mining (Recommended)
- **[duinocoin/QUICKSTART_DUINOCOIN.md](duinocoin/QUICKSTART_DUINOCOIN.md)** - Start mining in ~2 hours
- **[duinocoin/DUINOCOIN_SETUP.md](duinocoin/DUINOCOIN_SETUP.md)** - Complete mining setup guide
- **[duinocoin/README.md](duinocoin/README.md)** - DuinoCoin overview

### Distributed Computing
- **[QUICKSTART.md](QUICKSTART.md)** - Distributed computing quick start
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Architecture and detailed setup
- **[examples/README.md](examples/README.md)** - Task examples and patterns

## Hardware Requirements

### ESP32 Nodes (9x)
- **Board:** ELEGOO ESP-32 Development Board
- **Chip:** ESP32-WROOM-32
- **USB:** USB-C with CP2102 chip
- **Specs:** Dual-core @ 240MHz, 520KB SRAM, WiFi + Bluetooth

### Master Node (1x)
- **Board:** KickPi K2B (or any Linux SBC)
- **OS:** Linux (Ubuntu/Debian recommended)
- **Network:** WiFi or Ethernet
- **Purpose:** MQTT broker + task dispatcher

### Optional
- **ESP8266:** Can be added as additional worker (limited capability)
- **USB Hub:** For simultaneous ESP32 connections
- **Power Supply:** 9x USB power sources (2A each recommended)

## Credits

This project builds on the excellent **Broccoli** framework:
- **Original Author:** Wei Lin
- **GitHub:** [Wei1234c/Broccoli](https://github.com/Wei1234c/Broccoli)
- **Created:** 2018-04-06

Broccoli provides the distributed task queue system that makes this cluster possible!

## Related Projects

- [Celery](http://www.celeryproject.org/) - Distributed task queue (inspiration)
- [Celery On Docker Swarm](https://github.com/Wei1234c/CeleryOnDockerSwarm)
- [IoT as Brain](https://github.com/Wei1234c/IOTasBrain)
- [Elastic Network of Things with MQTT and MicroPython](https://github.com/Wei1234c/Elastic_Network_of_Things_with_MQTT_and_MicroPython)

## License

See [LICENSE](LICENSE) file for details.

The Broccoli framework code in `codes/broccoli/` retains its original license.

## Contributing

Feel free to:
- Add new example tasks
- Improve deployment scripts
- Optimize performance
- Add support for more ESP32 variants
- Create documentation and tutorials

## Troubleshooting

### ESP32 won't connect to WiFi
- Check SSID/password in `config/config_wifi_params.py`
- Ensure WiFi is 2.4GHz (ESP32 doesn't support 5GHz)
- Connect via serial to see debug output

### Cluster not responding
- Verify MQTT broker: `sudo systemctl status mosquitto`
- Check connectivity: `mosquitto_sub -h localhost -t "cluster/#"`
- Verify ESP32s can reach K2B IP

### Slow performance
- Normal! WiFi latency is inherent
- Best for CPU-bound, embarrassingly parallel problems
- Reduce network overhead by batching operations

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for more troubleshooting.

## Fun Facts

- **Total computing power:** ~1800 MIPS (theoretical)
- **Cost per node:** ~$7 USD (vs $35+ for Raspberry Pi)
- **Power consumption:** ~1.5W per ESP32 node
- **Boot time:** ~3 seconds per node
- **WiFi range:** Can span entire building
- **Scalability:** Add more nodes by flashing and powering on

## Why Build This?

Because it's **stupid but fun**!

This project demonstrates:
- Distributed systems concepts
- Message-passing architectures
- Parallel computing patterns
- IoT at scale
- That you don't need expensive hardware to learn cluster computing

Plus, you get to say "I have a 9-node distributed computing cluster" at parties. 🎉

## Next Steps

1. **Get Started:** Follow [QUICKSTART.md](QUICKSTART.md)
2. **Learn Patterns:** Read [examples/README.md](examples/README.md)
3. **Build Something:** Create your own distributed algorithm
4. **Scale Up:** Add more ESP32 nodes!
5. **Share:** Show off your cluster to the world

Happy clustering! 🚀

---

**Note:** This is an educational/experimental project. For production distributed computing, consider mature solutions like Dask, Ray, or Apache Spark.
