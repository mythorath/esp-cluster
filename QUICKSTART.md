# ESP32 Cluster - Quick Start Guide

Get your 9-node ESP32 cluster up and running in under an hour!

## Prerequisites

- 9x ESP32 Development Boards (ELEGOO ESP-32 DevKit v1)
- 1x KickPi K2B (or any Linux machine)
- WiFi network
- USB cables to connect ESP32s
- Micro-USB hub (optional, for simultaneous connections)

## 5-Minute Setup Overview

1. **Configure WiFi and MQTT** (2 minutes)
2. **Setup K2B Master Node** (10 minutes)
3. **Flash ESP32s with MicroPython** (20 minutes)
4. **Deploy Cluster Code** (15 minutes)
5. **Run Demo** (5 minutes)

## Step-by-Step Instructions

### Step 1: Configure Your Network Settings

Edit the configuration files with your WiFi and network details:

```bash
cd /home/user/esp-cluster

# Edit WiFi settings
nano config/config_wifi_params.py
```

Replace with your WiFi credentials:
```python
SSID = 'YourWiFiNetworkName'
PASSWORD = 'YourWiFiPassword'
```

### Step 2: Setup K2B as Master Node

Run the automated setup script on your KickPi K2B:

```bash
cd deployment
./setup_k2b_master.sh
```

This script will:
- Install MQTT broker (Mosquitto)
- Install Python dependencies
- Configure the cluster master node
- Display your K2B's IP address

**Important:** Note the K2B's IP address displayed at the end!

Now update the MQTT configuration:

```bash
nano ../config/config_mqtt_params.py
```

Set the BROKER_HOST to your K2B's IP:
```python
BROKER_HOST = '192.168.1.XXX'  # Your K2B's IP
```

### Step 3: Flash MicroPython to ESP32s

Connect each ESP32 one at a time and run:

```bash
./flash_esp32_nodes.sh
```

This will:
- Download MicroPython firmware (if needed)
- Erase each ESP32's flash
- Flash MicroPython firmware

**Note:** You'll connect each ESP32, press Enter to flash it, then disconnect and connect the next one.

### Step 4: Deploy Broccoli Cluster Code

Now deploy the cluster software to each ESP32:

```bash
./deploy_broccoli.sh
```

This uploads:
- WiFi configuration
- MQTT configuration
- Broccoli worker code
- Cluster node software

### Step 5: Power On and Test!

1. **Power on all 9 ESP32s**
   - They'll auto-connect to WiFi
   - Then connect to the MQTT broker on K2B
   - LED should blink when connected

2. **Run the test suite:**

```bash
cd ../examples
python3 test_cluster.py
```

You should see:
- Cluster initialization
- Multiple test scenarios running
- Results from distributed computations

## What You Can Do Now

### Example 1: Calculate Pi with Monte Carlo

```python
from canvas import group
import cluster_tasks as tasks

# Run 10,000 iterations on each of 9 nodes = 90,000 total
gp = group([
    tasks.monte_carlo_pi.s(10000)
    for _ in range(9)
])

results = gp.get()
pi_estimate = sum(results) / len(results)
print(f"Pi estimate: {pi_estimate}")
```

### Example 2: Parallel Prime Counting

```python
from canvas import group
import cluster_tasks as tasks

# Count primes from 1 to 100,000 across 9 nodes
chunk_size = 100000 // 9

gp = group([
    tasks.count_primes_in_range.s(i*chunk_size + 1, (i+1)*chunk_size)
    for i in range(9)
])

results = gp.get()
total_primes = sum(results)
print(f"Total primes: {total_primes}")
```

### Example 3: Distributed Word Count (MapReduce)

```python
from canvas import chord
import cluster_tasks as tasks

text_chunks = ["text chunk 1", "text chunk 2", ...]  # Your data

# Map phase: count words in each chunk
map_group = group([tasks.word_count.s(text) for text in text_chunks])

# Reduce phase: merge all counts
async_result = chord(map_group)(tasks.merge_word_counts.s())
word_counts = async_result.get()
```

## Supported Patterns

The cluster supports Celery Canvas-like patterns:

| Pattern | Description | Use Case |
|---------|-------------|----------|
| **group** | Parallel execution | Run same task with different inputs |
| **chain** | Sequential pipeline | (a + b) → (× c) → (× d) |
| **chord** | Map-Reduce | Parallel map, then reduce to single result |
| **map** | Apply to each | Process list items in parallel |
| **starmap** | Apply with unpacking | Like map but unpacks arguments |
| **chunks** | Batch processing | Split large dataset across workers |

## Troubleshooting

### ESP32 Won't Connect to WiFi

1. Check SSID and password in `config_wifi_params.py`
2. Ensure WiFi is 2.4GHz (ESP32 doesn't support 5GHz)
3. Connect to ESP32 serial console to see debug messages:
   ```bash
   screen /dev/ttyUSB0 115200
   ```

### Cluster Not Responding

1. Check MQTT broker is running on K2B:
   ```bash
   sudo systemctl status mosquitto
   ```

2. Test MQTT connectivity:
   ```bash
   mosquitto_sub -h localhost -t "cluster/#" -v
   ```

3. Verify ESP32s can reach K2B:
   ```bash
   # From K2B, check MQTT logs
   tail -f /var/log/mosquitto/mosquitto.log
   ```

### Slow Performance

- ESP32s are connected via WiFi - latency is expected
- Best for embarrassingly parallel problems
- Reduce network overhead by batching operations

## Performance Tips

1. **Use group() for parallel tasks** - Maximize throughput
2. **Minimize data transfer** - Send computation, not data
3. **Batch operations** - Use chunks() for large datasets
4. **Keep tasks CPU-bound** - Avoid I/O intensive operations

## Next Steps

- Read the full [SETUP_GUIDE.md](SETUP_GUIDE.md)
- Explore example tasks in `examples/cluster_tasks.py`
- Create your own distributed algorithms
- Monitor cluster with MQTT tools

## Cool Project Ideas

1. **Distributed Password Cracker** (educational/authorized only)
2. **Parallel Ray Tracer** (render 3D scenes)
3. **Genetic Algorithm Optimizer** (evolve solutions)
4. **IoT Sensor Network** (process distributed sensor data)
5. **Distributed Hash Table** (P2P data structure)
6. **Mandelbrot Set Renderer** (parallel fractal generation)
7. **Prime Factorization** (distributed number theory)

Have fun with your ESP32 cluster! 🚀
