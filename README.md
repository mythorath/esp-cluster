# ESP32 Flexible Compute Cluster

A **9-node ESP32 distributed computing cluster** that can run parallel algorithms, mine DuinoCoin, or both!

![Cluster Status](https://img.shields.io/badge/Status-Active-green)
![Nodes](https://img.shields.io/badge/Nodes-9x_ESP32-blue)
![Platform](https://img.shields.io/badge/Platform-MicroPython-blue)
![Framework](https://img.shields.io/badge/Framework-Broccoli-purple)

## What Is This?

This is a **flexible distributed computing cluster** built from 9x ESP32 microcontrollers. It's a general-purpose compute platform that can:

- **💻 Run Distributed Computations** (Primary use - parallel algorithms, MapReduce, simulations)
- **⛏️ Mine DuinoCoin** (Optional - when you want crypto mining)
- **🔄 Switch Between Tasks** (Dynamically change workloads)
- **📡 Deploy Code Wirelessly** (Update tasks without re-flashing)

**Think of it as:** A mini cloud computing platform you control, not dedicated mining hardware!

Built from:
- **9x ESP32 DevKit v1** boards (dual-core @ 240MHz each)
- **1x KickPi K2B** (coordinator running Linux)
- **Broccoli framework** (distributed task queue system)
- **MicroPython** (flexible programming platform)

## Cluster Capabilities

### Primary: Distributed Computing 💻

A **flexible compute platform** using the Broccoli framework:
- **Monte Carlo simulations** - Parallel random sampling
- **MapReduce operations** - Process large datasets
- **Prime searching** - Distributed number crunching
- **Parallel algorithms** - Any embarrassingly parallel problem
- **Custom tasks** - Deploy your own Python code wirelessly

→ **See [QUICKSTART.md](QUICKSTART.md) for setup**
→ **See [CLUSTER_USAGE.md](CLUSTER_USAGE.md) for usage guide**

### Optional: DuinoCoin Mining ⛏️

The cluster **CAN mine DuinoCoin** as one of many possible tasks:

**Flexible Cluster (MicroPython):**
- **Hashrate:** ~450-630 kH/s total (~50-70 kH/s per ESP32)
- **Daily Earnings:** ~30-50 DUCO
- **Advantage:** Switch between mining and computing anytime
- **Trade-off:** Lower hashrate than dedicated miners

**Dedicated Miners (Arduino C++):**
- **Hashrate:** 1.53-1.62 MH/s total (170-180 kH/s per ESP32)
- **Daily Earnings:** ~90 DUCO
- **Advantage:** Maximum performance
- **Trade-off:** Can ONLY mine, no flexibility

→ **Flexible mining:** See [CLUSTER_USAGE.md](CLUSTER_USAGE.md)
→ **Dedicated mining:** See [duinocoin/QUICKSTART_DUINOCOIN.md](duinocoin/QUICKSTART_DUINOCOIN.md)

**Choose based on your goal:** Flexibility or maximum mining performance.

## Architecture

```
┌──────────────────────────────────────────────┐
│         KickPi K2B (Coordinator)             │
│  • MQTT Broker (Mosquitto)                   │
│  • Task Dispatcher                           │
│  • Workload Manager                          │
└────────────────┬─────────────────────────────┘
                 │
            WiFi Network
         (MQTT Protocol Port 1883)
                 │
    ┌────────────┼───────────┬─────────┐
    │            │           │         │
┌───▼───┐   ┌───▼───┐   ┌───▼───┐   ...
│ESP32-1│   │ESP32-2│   │ESP32-9│
│ Task  │   │ Task  │   │ Task  │
│Worker │   │Worker │   │Worker │
└───────┘   └───────┘   └───────┘

Each ESP32: Dual-core @ 240MHz, 520KB RAM
Total: 18 cores, ~4.6MB RAM, ~1800 MIPS

Runs MicroPython + Broccoli framework
Can execute ANY task you deploy!
```

## Features

### Celery Canvas-Like Operations

- **Groups** - Parallel execution across workers
- **Chains** - Sequential pipelines (a → b → c)
- **Chords** - MapReduce patterns (parallel map + reduce)
- **Map/Starmap** - Apply functions to lists
- **Chunks** - Batch processing of large datasets

### Cluster Management

- **Dynamic Code Deployment** - Upload new tasks wirelessly
- **Symmetric Architecture** - Every ESP32 is identical
- **Auto-Discovery** - Nodes auto-connect to cluster
- **Fault Tolerance** - Tasks retry on failure
- **Task Switching** - Change workloads without re-flashing
- **Mixed Workloads** - Run different tasks on different nodes

## Quick Start

### Setup: Build the Compute Cluster 💻

```bash
# 1. Configure WiFi and MQTT
nano config/config_wifi_params.py
nano config/config_mqtt_params.py

# 2. Setup K2B as coordinator
cd deployment
./setup_k2b_master.sh

# 3. Flash MicroPython to all 9 ESP32s
./flash_esp32_nodes.sh

# 4. Deploy Broccoli cluster framework
./deploy_broccoli.sh

# 5. Test cluster with distributed computing
cd ../examples
python3 test_cluster.py
```

**→ Full guide:** [QUICKSTART.md](QUICKSTART.md)

### Usage: Run Tasks on Your Cluster

**Distributed Computing:**
```bash
cd examples
python3 test_cluster.py  # Run test suite
```

**DuinoCoin Mining (as a task):**
```bash
cd examples
python3 cluster_coordinator.py \
    --mode mine \
    --username YOUR_DUCO_USERNAME \
    --duration 60
```

**Mixed Workload:**
```python
from cluster_coordinator import ClusterCoordinator

coord = ClusterCoordinator("your_username")
coord.start_cluster()

# Deploy both computing and mining tasks
coord.deploy_tasks(['cluster_tasks.py', 'duinocoin_task.py'])

# Mine for 30 minutes
coord.mine_duinocoin(duration_minutes=30)

# Run computation
coord.run_computation('monte_carlo_pi', iterations=100000)
```

**→ Full usage guide:** [CLUSTER_USAGE.md](CLUSTER_USAGE.md)

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

## Example: DuinoCoin Mining

```bash
# Mine for 1 hour
python3 cluster_coordinator.py --mode mine --username myusername --duration 60

# Mine specific number of shares
python3 cluster_coordinator.py --mode mine --username myusername --shares 100
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

### Distributed Computing (Primary Use) 💻
- **Monte Carlo Simulations** - Run millions of iterations in parallel
- **MapReduce Operations** - Process large datasets across nodes
- **Prime Searching** - Distributed number crunching
- **Parameter Sweeps** - Test many parameter combinations
- **Genetic Algorithms** - Parallel evolution of solutions
- **Distributed Sensors** - IoT data aggregation
- **Password Cracking** - Educational/authorized testing
- **Custom Algorithms** - Deploy your own Python tasks wirelessly

### Optional: DuinoCoin Mining ⛏️
- **Mine as a cluster task** (~30-50 DUCO/day with flexible MicroPython setup)
- **OR use dedicated miners** (~90 DUCO/day with Arduino C++ setup)
- **Switch between mining and computing** on demand
- **Mine when idle** - Use cluster downtime productively
- **Educational** - Learn about cryptocurrency mining
- **Low power** - ~13.5W total

### Flexibility is Key 🔄
- **Switch tasks dynamically** - No re-flashing needed
- **Deploy code wirelessly** - Update tasks over WiFi
- **Mixed workloads** - Some nodes mine, others compute
- **Scheduler support** - Mine at night, compute during day
- **Resource allocation** - Assign nodes to different tasks

### Not Ideal For:
- Traditional cryptocurrency mining (Bitcoin/Ethereum)
- Single-threaded CPU-intensive tasks
- Large memory operations (520KB per node)
- Real-time control (network latency)
- Maximum DuinoCoin hashrate (use dedicated miners for that)

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
├── CLUSTER_USAGE.md       # ⭐ How to use your cluster (READ THIS!)
│
├── QUICKSTART.md          # Setup guide (~1 hour)
├── SETUP_GUIDE.md         # Detailed architecture
│
├── config/                # Configuration files
│   ├── config_wifi_params.py      # WiFi credentials
│   └── config_mqtt_params.py      # MQTT broker settings
│
├── deployment/            # Setup and deployment scripts
│   ├── setup_k2b_master.sh        # Setup K2B coordinator
│   ├── flash_esp32_nodes.sh       # Flash MicroPython
│   ├── deploy_broccoli.sh         # Deploy cluster code
│   └── node_config.py             # Node definitions
│
├── examples/              # Task examples and coordinator
│   ├── README.md          # Examples documentation
│   ├── cluster_tasks.py   # Distributed computing tasks
│   ├── test_cluster.py    # Test suite
│   ├── duinocoin_task.py  # ⛏️ DuinoCoin mining as a task
│   └── cluster_coordinator.py  # 🎯 Task coordinator
│
├── codes/broccoli/        # Broccoli framework (original)
│   ├── client/            # Client code for coordinator
│   ├── node/              # Node/worker code
│   ├── micropython/       # ESP32 MicroPython code
│   └── config/            # Framework configuration
│
└── duinocoin/             # 📁 Dedicated mining setup (alternative)
    ├── README.md                  # DuinoCoin overview
    ├── QUICKSTART_DUINOCOIN.md    # Dedicated miners guide
    ├── DUINOCOIN_SETUP.md         # Complete mining setup
    ├── config/                    # Mining configuration
    ├── scripts/                   # Setup & deployment
    └── monitor/                   # Monitoring tools
```

## Documentation

### Getting Started
- **[QUICKSTART.md](QUICKSTART.md)** - Set up your cluster (~1 hour)
- **[CLUSTER_USAGE.md](CLUSTER_USAGE.md)** - How to use your cluster ⭐ (READ THIS!)
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Detailed architecture guide

### Using the Cluster
- **[examples/README.md](examples/README.md)** - Distributed computing examples
- **[examples/cluster_coordinator.py](examples/cluster_coordinator.py)** - Task coordinator
- **[examples/duinocoin_task.py](examples/duinocoin_task.py)** - Mining as a task

### Dedicated DuinoCoin Mining (Alternative)
If you want maximum mining performance (not flexibility):
- **[duinocoin/QUICKSTART_DUINOCOIN.md](duinocoin/QUICKSTART_DUINOCOIN.md)** - Dedicated miners setup
- **[duinocoin/DUINOCOIN_SETUP.md](duinocoin/DUINOCOIN_SETUP.md)** - Complete mining guide
- **[duinocoin/README.md](duinocoin/README.md)** - DuinoCoin overview

**Note:** Dedicated mining sacrifices cluster flexibility for ~3x better hashrate.

## Hardware Requirements

### ESP32 Nodes (9x)
- **Board:** ELEGOO ESP-32 Development Board
- **Chip:** ESP32-WROOM-32
- **USB:** USB-C with CP2102 chip
- **Specs:** Dual-core @ 240MHz, 520KB SRAM, WiFi + Bluetooth

### Coordinator Node (1x)
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
- [DuinoCoin](https://duinocoin.com) - Cryptocurrency for microcontrollers

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

### Mining performance lower than expected
- **Normal for MicroPython!** (~50-70 kH/s vs 170-180 kH/s for Arduino C++)
- This is the trade-off for flexibility
- Use dedicated miners if you want maximum hashrate

See [SETUP_GUIDE.md](SETUP_GUIDE.md) and [CLUSTER_USAGE.md](CLUSTER_USAGE.md) for more troubleshooting.

## Fun Facts

- **Total computing power:** ~1800 MIPS (theoretical)
- **Cost per node:** ~$7 USD (vs $35+ for Raspberry Pi)
- **Power consumption:** ~1.5W per ESP32 node
- **Boot time:** ~3 seconds per node
- **WiFi range:** Can span entire building
- **Scalability:** Add more nodes by flashing and powering on
- **Flexibility:** Switch from mining to computing in seconds!

## Why Build This?

Because it's a **flexible compute platform** that teaches you:
- Distributed systems concepts
- Message-passing architectures
- Parallel computing patterns
- IoT at scale
- Task scheduling and coordination
- Cryptocurrency mining (optionally!)
- That you don't need expensive hardware to learn cluster computing

Plus, you get to say "I have a 9-node distributed computing cluster that can also mine crypto" at parties. 🎉

## Next Steps

1. **Get Started:** Follow [QUICKSTART.md](QUICKSTART.md)
2. **Learn Usage:** Read [CLUSTER_USAGE.md](CLUSTER_USAGE.md)
3. **Run Examples:** Try [examples/test_cluster.py](examples/test_cluster.py)
4. **Try Mining:** Use [examples/cluster_coordinator.py](examples/cluster_coordinator.py)
5. **Build Something:** Create your own distributed algorithm
6. **Scale Up:** Add more ESP32 nodes!

Happy clustering! 🚀

---

**Note:** This is a flexible educational/experimental compute cluster. For production distributed computing, consider mature solutions like Dask, Ray, or Apache Spark. For dedicated cryptocurrency mining, use specialized hardware or the dedicated Arduino setup in `duinocoin/`.
