# ESP32 Cluster Examples

This directory contains example tasks and test scripts for the ESP32 cluster.

## Files

- **cluster_tasks.py** - Task definitions deployed to ESP32 worker nodes
- **test_cluster.py** - Comprehensive test suite demonstrating cluster capabilities

## Running the Examples

### Basic Test Suite

Run all tests to verify cluster functionality:

```bash
python3 test_cluster.py
```

This will run:
1. Basic arithmetic operations (parallel multiplication)
2. Chained operations (sequential pipeline)
3. Map-Reduce pattern (sum of squares)
4. Monte Carlo Pi estimation (distributed simulation)
5. Prime number counting (distributed search)
6. Word counting (MapReduce on text)
7. Matrix multiplication (distributed linear algebra)

### Custom Tests

Create your own test file:

```python
#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from codes.broccoli.client.client import Client
import time

# Initialize client
client = Client()
client.start()

# Wait for cluster
while not client.status['Is connected']:
    time.sleep(1)

# Deploy tasks
client.sync_file('cluster_tasks.py', load_as_tasks=True)
time.sleep(3)

# Import Canvas operations
from canvas import group, chain, chord
import cluster_tasks as tasks

# Your code here!
gp = group([tasks.add.s(i, i) for i in range(10)])
results = gp.get()
print(results)

client.stop()
```

## Task Categories

### Basic Math
- `add(x, y)` - Addition
- `mul(x, y)` - Multiplication
- `sub(x, y)` - Subtraction
- `power(x, y)` - Exponentiation

### Aggregation
- `xsum(numbers)` - Sum list
- `average(numbers)` - Calculate mean
- `find_min(numbers)` - Find minimum
- `find_max(numbers)` - Find maximum

### Monte Carlo Simulation
- `monte_carlo_pi(iterations)` - Estimate Pi
- `monte_carlo_pi_batch(iterations, samples)` - Multiple estimates

### Data Processing
- `word_count(text)` - Count word frequencies
- `merge_word_counts(dicts)` - Merge word count results

### Numerical
- `factorial(n)` - Calculate factorial
- `fibonacci(n)` - Nth Fibonacci number
- `is_prime(n)` - Check if prime
- `count_primes_in_range(start, end)` - Count primes in range

### Matrix Operations
- `matrix_multiply_row(row, matrix)` - Multiply row by matrix
- `dot_product(vec_a, vec_b)` - Vector dot product

### Hashing
- `simple_hash(text)` - Simple hash function
- `find_hash_collision(prefix, target, start, count)` - Find hash patterns

### Statistics
- `variance(numbers)` - Calculate variance
- `standard_deviation(numbers)` - Calculate std dev

### Sensor Simulation
- `generate_sensor_reading(id, count)` - Simulate IoT sensors
- `process_sensor_batch(readings)` - Aggregate sensor data

## Canvas Patterns

### Group - Parallel Execution

Execute multiple tasks in parallel:

```python
gp = group([tasks.mul.s(i, i+1) for i in range(9)])
results = gp.get()  # [0, 2, 6, 12, 20, 30, 42, 56, 72]
```

### Chain - Sequential Pipeline

Execute tasks in sequence, passing results:

```python
ch = chain(
    tasks.add.s(4, 4),   # 8
    tasks.mul.s(2),      # 16
    tasks.mul.s(3)       # 48
)
result = ch.get()  # 48
```

### Chord - MapReduce

Parallel tasks followed by aggregation:

```python
# Calculate sum of squares
header = [tasks.mul.s(i, i) for i in range(10)]
callback = tasks.xsum.s()
result = chord(header)(callback).get()  # 285
```

### Map

Apply function to each element:

```python
gp = tasks.xsum.map([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])
results = gp.get()  # [6, 15, 24]
```

### Starmap

Like map, but unpacks arguments:

```python
gp = tasks.add.starmap([
    (1, 2),
    (3, 4),
    (5, 6)
])
results = gp.get()  # [3, 7, 11]
```

### Chunks

Split large dataset across workers:

```python
ck = tasks.add.chunks(
    list(zip(range(100), range(100))),
    10  # 10 chunks
)
results = ck.apply_async().get()
```

## Performance Examples

### Example 1: Monte Carlo Pi (Parallel Simulation)

Estimate Pi using 90,000 iterations across 9 nodes:

```python
from canvas import group

iterations_per_node = 10000
gp = group([
    tasks.monte_carlo_pi.s(iterations_per_node)
    for _ in range(9)
])

start = time.time()
results = gp.get()
elapsed = time.time() - start

pi_estimate = sum(results) / len(results)
print(f"Pi ≈ {pi_estimate} (computed in {elapsed:.2f}s)")
```

### Example 2: Distributed Prime Search

Count primes from 1 to 100,000:

```python
from canvas import group

# Split into 9 chunks
chunk_size = 100000 // 9
gp = group([
    tasks.count_primes_in_range.s(
        i * chunk_size + 1,
        (i + 1) * chunk_size
    )
    for i in range(9)
])

results = gp.get()
total = sum(results)
print(f"Found {total} primes")
```

### Example 3: Parallel Matrix Multiplication

Multiply matrices by distributing rows:

```python
from canvas import group

matrix_a = [[1,2,3], [4,5,6], [7,8,9]]
matrix_b = [[9,8,7], [6,5,4], [3,2,1]]

gp = group([
    tasks.matrix_multiply_row.s(row, matrix_b)
    for row in matrix_a
])

result_matrix = gp.get()
```

### Example 4: MapReduce Word Count

Count words across multiple documents:

```python
from canvas import chord

documents = [
    "document 1 text...",
    "document 2 text...",
    # ... more documents
]

# Map: count words in each document
map_group = group([
    tasks.word_count.s(doc)
    for doc in documents
])

# Reduce: merge all counts
result = chord(map_group)(tasks.merge_word_counts.s())
word_counts = result.get()

# Sort by frequency
sorted_words = sorted(
    word_counts.items(),
    key=lambda x: x[1],
    reverse=True
)
```

## Adding Your Own Tasks

Edit `cluster_tasks.py` and add your function:

```python
def my_custom_task(param1, param2):
    """Your task description"""
    # Your computation here
    result = param1 * param2 + 42
    return result
```

Then redeploy to cluster:

```python
client.sync_file('cluster_tasks.py', load_as_tasks=True)
time.sleep(3)  # Wait for deployment

# Use your task
result = tasks.my_custom_task.s(10, 20).apply_async().get()
```

## Benchmarking

To measure speedup, compare cluster vs. single-node:

```python
import time

# Single node (sequential)
start = time.time()
results = [monte_carlo_pi(10000) for _ in range(9)]
sequential_time = time.time() - start

# Cluster (parallel)
start = time.time()
gp = group([tasks.monte_carlo_pi.s(10000) for _ in range(9)])
results = gp.get()
parallel_time = time.time() - start

speedup = sequential_time / parallel_time
print(f"Speedup: {speedup:.2f}x")
```

## Tips for Good Cluster Performance

1. **CPU-bound tasks work best** - Network latency matters
2. **Minimize data transfer** - Send code, not large datasets
3. **Batch operations** - Group related tasks together
4. **Use appropriate chunk sizes** - Balance load across nodes
5. **Avoid stateful operations** - Tasks should be independent

## Common Patterns

### Embarrassingly Parallel
Tasks that don't need to communicate:
- Monte Carlo simulations
- Parameter sweeps
- Independent calculations

### MapReduce
Parallel processing + aggregation:
- Word counting
- Data analysis
- Statistical computations

### Pipeline
Sequential processing stages:
- Data transformation chains
- Multi-step algorithms

### Divide and Conquer
Break problem into sub-problems:
- Sorting algorithms
- Tree traversal
- Search algorithms

Enjoy building with your ESP32 cluster! 🎯
