# ESP32 Distributed Computing Cluster

A "stupid but fun" expandable ESP32 cluster that amasses computing power similar to a Beowulf cluster, using the **Broccoli** distributed task queue framework.

![Cluster Status](https://img.shields.io/badge/Status-Experimental-orange)
![Nodes](https://img.shields.io/badge/Nodes-9x_ESP32-blue)
![Architecture](https://img.shields.io/badge/Architecture-Distributed-green)

## What Is This?

This is a **distributed computing cluster** built from:
- **9x ESP32 DevKit v1 boards** (worker nodes)
- **1x KickPi K2B** (master node running Linux)
- **MQTT over WiFi** (communication backbone)

Think of it as a mini Beowulf cluster, but with microcontrollers instead of PCs!

## Reality Check

**ESP32s CANNOT run Linux** - they're microcontrollers, not microprocessors. However, they CAN:
- Run MicroPython (Python 3 on bare metal)
- Execute distributed computations
- Communicate via MQTT/WiFi
- Process tasks in parallel across 9 nodes (18 cores total!)

This cluster uses the **Broccoli framework** - a distributed task queue system that mimics [Celery Canvas](http://docs.celeryproject.org/en/latest/userguide/canvas.html) functionality.

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

```bash
# 1. Configure WiFi and MQTT broker IP
nano config/config_wifi_params.py
nano config/config_mqtt_params.py

# 2. Setup K2B as master node
cd deployment
./setup_k2b_master.sh

# 3. Flash MicroPython to ESP32s
./flash_esp32_nodes.sh

# 4. Deploy Broccoli cluster code
./deploy_broccoli.sh

# 5. Test the cluster!
cd ../examples
python3 test_cluster.py
```

See [QUICKSTART.md](QUICKSTART.md) for detailed instructions.

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

## What Can You Build?

### Perfect For:
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
- Tasks requiring OS features (no Linux on ESP32)
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
├── QUICKSTART.md          # Fast setup guide
├── SETUP_GUIDE.md         # Detailed architecture and setup
│
├── config/                # Configuration files
│   ├── config_wifi_params.py      # WiFi credentials
│   └── config_mqtt_params.py      # MQTT broker settings
│
├── deployment/            # Setup and deployment scripts
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
└── examples/              # Example tasks and demos
    ├── README.md          # Examples documentation
    ├── cluster_tasks.py   # Task definitions
    └── test_cluster.py    # Comprehensive test suite
```

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get up and running in < 1 hour
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
