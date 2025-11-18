# ESP32 Flexible Compute Cluster Usage Guide

This guide explains how to use your ESP32 cluster as a **general-purpose distributed computing platform** that can run multiple types of workloads, including DuinoCoin mining.

## Cluster Philosophy

Your cluster is a **flexible computing resource**, not dedicated mining hardware. You can:

- **Switch between tasks** on demand
- **Run mining** when you want
- **Run computations** when you want
- **Mix workloads** - some nodes mining, others computing
- **Deploy new tasks** dynamically over WiFi

Think of it like a mini cloud computing platform!

## Architecture Overview

```
┌─────────────────────────────────────────────┐
│         KickPi K2B (Coordinator)            │
│  • Task Dispatcher                          │
│  • Workload Manager                         │
│  • MQTT Broker                              │
└────────────────┬────────────────────────────┘
                 │
            WiFi/MQTT
                 │
    ┌────────────┼───────────┬────────────┐
    │            │           │            │
┌───▼────┐  ┌───▼────┐  ┌───▼────┐   ┌──▼──┐
│ESP32-1 │  │ESP32-2 │  │ESP32-3 │...│ESP32-9│
│        │  │        │  │        │   │        │
│Running │  │Running │  │Running │   │Running │
│Task A  │  │Task A  │  │Task B  │   │Task C  │
└────────┘  └────────┘  └────────┘   └────────┘

Each node can run ANY task you deploy!
```

## Usage Modes

### Mode 1: Pure Computation (Default)

Use the cluster for distributed computing tasks:

```bash
cd examples
python3 cluster_coordinator.py --mode compute
```

Then run any distributed task:
- Monte Carlo simulations
- MapReduce operations
- Prime searching
- Parallel algorithms

See `examples/test_cluster.py` for examples.

### Mode 2: DuinoCoin Mining

Mine DuinoCoin across all 9 nodes:

```bash
python3 cluster_coordinator.py \
    --mode mine \
    --username YOUR_DUINOCOIN_USERNAME \
    --duration 60  # mine for 60 minutes
```

Or mine specific number of shares:

```bash
python3 cluster_coordinator.py \
    --mode mine \
    --username YOUR_DUINOCOIN_USERNAME \
    --shares 100  # 100 shares per node
```

### Mode 3: Mixed Workload

Run mining on some nodes, computing on others:

```bash
python3 cluster_coordinator.py --mode mixed
```

This dedicates:
- 5 nodes to mining
- 4 nodes to computing

You can adjust the ratio in the code.

### Mode 4: On-Demand Task Switching

```python
from cluster_coordinator import ClusterCoordinator

coord = ClusterCoordinator(duinocoin_username="myusername")
coord.start_cluster()

# Mine for 30 minutes
coord.deploy_tasks(['duinocoin_task.py'])
coord.mine_duinocoin(duration_minutes=30)

# Switch to computing
coord.deploy_tasks(['cluster_tasks.py'])
coord.run_computation('monte_carlo_pi', iterations=10000)

# Back to mining
coord.mine_duinocoin(duration_minutes=30)

coord.shutdown()
```

## Setting Up for DuinoCoin Mining

### 1. Create DuinoCoin Account

```bash
# Go to https://wallet.duinocoin.com and register
# Save your username
```

### 2. Configure Username

Edit `examples/duinocoin_task.py`:

```python
USERNAME = "your_duinocoin_username"
```

### 3. Deploy Mining Task to Cluster

The mining code runs as a **MicroPython task** on the Broccoli cluster:

```bash
cd examples
python3 -c "
from cluster_coordinator import ClusterCoordinator
coord = ClusterCoordinator('your_username')
coord.start_cluster()
coord.deploy_tasks(['duinocoin_task.py'])
coord.mine_duinocoin(duration_minutes=60)
"
```

### 4. Monitor Mining

The coordinator shows real-time stats:

```
Mining Results
========================================
Cluster Statistics:
  Total Time: 3600.0 seconds (60.0 minutes)
  Shares Accepted: 145
  Shares Rejected: 3
  Acceptance Rate: 97.97%

Per-Node Results:
  Node 1: 16 accepted, 0 rejected
  Node 2: 15 accepted, 1 rejected
  Node 3: 17 accepted, 0 rejected
  ...

Estimated Earnings: ~0.145 DUCO
```

## Performance Expectations

### DuinoCoin Mining (MicroPython)

**Note:** Using MicroPython is slower than compiled C++!

- **Per ESP32:** ~50-70 kH/s (MicroPython) vs 170-180 kH/s (Arduino C++)
- **Total Cluster:** ~450-630 kH/s vs 1.5 MH/s
- **Daily Earnings:** ~30-50 DUCO vs ~90 DUCO

**Why MicroPython?**
- Flexibility! Same cluster can switch between tasks
- Dynamic deployment of new tasks
- No re-flashing needed
- Unified platform for computing + mining

**If you want maximum mining:**
- Use dedicated Arduino-based miners (see `duinocoin/` folder)
- But you lose cluster flexibility!

### Distributed Computing

Same as before:
- Monte Carlo: Full 9-node parallelization
- MapReduce: Efficient parallel processing
- Prime search: ~10x speedup

## Example Workflows

### Workflow 1: Mine at Night, Compute During Day

```python
import schedule
import time
from cluster_coordinator import ClusterCoordinator

coord = ClusterCoordinator("my_duco_username")
coord.start_cluster()

def start_mining():
    print("Night mode: Starting mining...")
    coord.deploy_tasks(['duinocoin_task.py'])
    coord.mine_duinocoin(duration_minutes=480)  # 8 hours

def start_computing():
    print("Day mode: Ready for computing...")
    coord.deploy_tasks(['cluster_tasks.py'])
    coord.cluster_mode = 'idle'

# Schedule
schedule.every().day.at("22:00").do(start_mining)   # 10 PM
schedule.every().day.at("06:00").do(start_computing) # 6 AM

while True:
    schedule.run_pending()
    time.sleep(60)
```

### Workflow 2: Mine When Idle

```python
coord = ClusterCoordinator("my_username")
coord.start_cluster()

# Default: Ready for computing
coord.deploy_tasks(['cluster_tasks.py', 'duinocoin_task.py'])

# When you're done computing for the day:
print("Switching to mining mode...")
coord.mine_duinocoin(duration_minutes=300)  # 5 hours

# When you need to compute again:
print("Back to computing mode...")
coord.cluster_mode = 'idle'
# Now run your computations
```

### Workflow 3: Priority-Based Task Queue

```python
class SmartCoordinator(ClusterCoordinator):
    def __init__(self, username):
        super().__init__(username)
        self.task_queue = []

    def queue_task(self, task_type, priority, **kwargs):
        self.task_queue.append({
            'type': task_type,
            'priority': priority,
            'kwargs': kwargs
        })

    def process_queue(self):
        # Sort by priority
        self.task_queue.sort(key=lambda x: x['priority'], reverse=True)

        for task in self.task_queue:
            if task['type'] == 'mine':
                self.mine_duinocoin(**task['kwargs'])
            elif task['type'] == 'compute':
                self.run_computation(**task['kwargs'])

        self.task_queue.clear()

# Usage
coord = SmartCoordinator("username")
coord.start_cluster()

coord.queue_task('compute', priority=10, task_name='urgent_calculation')
coord.queue_task('mine', priority=5, duration_minutes=60)
coord.queue_task('compute', priority=8, task_name='analysis')

coord.process_queue()  # Runs: urgent_calculation → analysis → mining
```

## Adding Your Own Tasks

### 1. Create Task File

```python
# my_custom_task.py

def analyze_data(dataset):
    """Your custom analysis task"""
    result = process(dataset)
    return result

def train_model(params):
    """Train a simple ML model"""
    # Your code here
    return model_accuracy
```

### 2. Deploy to Cluster

```python
coord.deploy_tasks(['my_custom_task.py'])
```

### 3. Run Task

```python
from canvas import group
import my_custom_task as tasks

# Run on all nodes
gp = group([
    tasks.analyze_data.s(chunk)
    for chunk in data_chunks
])
results = gp.get()
```

## Monitoring

### Web Dashboard (Recommended)

Start a monitoring dashboard:

```python
# In duinocoin/monitor/web_dashboard.py
# Modify to track current cluster mode

python3 duinocoin/monitor/web_dashboard.py
```

Access at `http://K2B_IP:5000`

Shows:
- Current cluster mode (mining/computing/mixed/idle)
- Active tasks per node
- Performance metrics
- Task history

### Terminal Monitor

```bash
python3 duinocoin/monitor/cluster_monitor.py
```

### Per-Task Monitoring

Each task can report its own status:

```python
def my_task_with_progress(workload):
    total = len(workload)
    for i, item in enumerate(workload):
        result = process(item)

        # Report progress
        if i % 100 == 0:
            progress = (i / total) * 100
            print(f"Progress: {progress:.1f}%")

    return results
```

## Best Practices

### 1. Task Design

**Good:** Independent, parallelizable tasks
```python
# Each node processes different data
group([
    tasks.process_chunk.s(chunk_1),
    tasks.process_chunk.s(chunk_2),
    ...
])
```

**Bad:** Sequential tasks with dependencies
```python
# Don't do this
result1 = tasks.step1.s().apply_async().get()
result2 = tasks.step2.s(result1).apply_async().get()
result3 = tasks.step3.s(result2).apply_async().get()
```

### 2. Mining Strategy

**For learning/fun:**
- Mine with MicroPython (flexible)
- Switch between tasks often

**For maximum earnings:**
- Use dedicated Arduino miners (`duinocoin/` setup)
- Sacrifice flexibility for performance

### 3. Resource Management

```python
# Monitor cluster health
status = coord.get_cluster_status()

if status['connected']:
    # Cluster is ready
    coord.run_my_task()
else:
    # Reconnect or alert
    coord.start_cluster()
```

### 4. Error Handling

```python
try:
    coord.mine_duinocoin(duration_minutes=60)
except Exception as e:
    print(f"Mining failed: {e}")
    # Fall back to computing or retry
    coord.deploy_tasks(['cluster_tasks.py'])
```

## Comparison: Flexible vs Dedicated

### This Setup (Flexible Cluster)

**Pros:**
- ✅ Can mine DuinoCoin
- ✅ Can run distributed computing
- ✅ Switch tasks dynamically
- ✅ Deploy new code wirelessly
- ✅ Unified platform
- ✅ Learning platform

**Cons:**
- ❌ Mining slower (~50-70 kH/s vs 170-180 kH/s per node)
- ❌ Lower earnings (~30-50 DUCO/day vs ~90)

### Dedicated Miners (duinocoin/ folder)

**Pros:**
- ✅ Maximum hashrate (170-180 kH/s per node)
- ✅ Maximum earnings (~90 DUCO/day)
- ✅ Optimized C++ code

**Cons:**
- ❌ Can ONLY mine
- ❌ Must re-flash to change tasks
- ❌ No flexibility
- ❌ Each node independent (not a cluster)

## Use Cases

### Perfect for Flexible Cluster:

1. **Research/Education**
   - Learn distributed computing
   - Experiment with parallel algorithms
   - Test cluster architectures

2. **Development**
   - Prototype distributed applications
   - Test code on real hardware
   - Rapid iteration

3. **Mixed Workloads**
   - Mine when idle
   - Compute when needed
   - Dynamic resource allocation

4. **IoT Platform**
   - Distributed sensor processing
   - Edge computing
   - Data aggregation

### Better with Dedicated Miners:

1. **Maximum Mining Profit**
2. **24/7 Mining Operations**
3. **Set-it-and-forget-it**

## Next Steps

1. **Set up cluster:** Follow `QUICKSTART.md`
2. **Test computing:** Run `examples/test_cluster.py`
3. **Try mining:** Run cluster coordinator with `--mode mine`
4. **Experiment:** Create your own tasks!
5. **Optimize:** Find the best workload balance for your needs

---

**Bottom Line:** This is a **compute cluster with mining capability**, not dedicated miners. Flexibility over maximum performance!
