#!/usr/bin/env python3
"""
ESP32 Cluster Example Tasks
Demonstrates various distributed computing patterns
"""

# These task definitions will be deployed to ESP32 workers


# ====================
# Basic Math Operations
# ====================

def add(x, y):
    """Add two numbers"""
    return x + y


def mul(x, y):
    """Multiply two numbers"""
    return x * y


def sub(x, y):
    """Subtract two numbers"""
    return x - y


def power(x, y):
    """Raise x to the power of y"""
    return x ** y


# ====================
# Aggregate Operations
# ====================

def xsum(numbers):
    """Sum a list of numbers"""
    return sum(numbers)


def average(numbers):
    """Calculate average of a list"""
    return sum(numbers) / len(numbers) if numbers else 0


def find_min(numbers):
    """Find minimum in a list"""
    return min(numbers) if numbers else None


def find_max(numbers):
    """Find maximum in a list"""
    return max(numbers) if numbers else None


# ====================
# Monte Carlo Simulation
# ====================

def monte_carlo_pi(iterations):
    """
    Estimate Pi using Monte Carlo method
    Perfect for distributed computing!
    """
    import random
    inside_circle = 0

    for _ in range(iterations):
        x = random.random()
        y = random.random()
        if x*x + y*y <= 1.0:
            inside_circle += 1

    return (inside_circle / iterations) * 4


def monte_carlo_pi_batch(iterations_per_node, num_samples):
    """
    Run multiple Monte Carlo simulations
    Returns list of pi estimates
    """
    import random
    results = []

    for _ in range(num_samples):
        inside = 0
        for _ in range(iterations_per_node):
            x = random.random()
            y = random.random()
            if x*x + y*y <= 1.0:
                inside += 1
        results.append((inside / iterations_per_node) * 4)

    return results


# ====================
# Data Processing
# ====================

def word_count(text):
    """
    Count words in text
    MapReduce pattern example
    """
    words = text.lower().split()
    counts = {}
    for word in words:
        # Remove basic punctuation
        word = word.strip('.,!?;:"')
        if word:
            counts[word] = counts.get(word, 0) + 1
    return counts


def merge_word_counts(count_dicts):
    """
    Merge multiple word count dictionaries
    Reduce step for MapReduce
    """
    merged = {}
    for d in count_dicts:
        for word, count in d.items():
            merged[word] = merged.get(word, 0) + count
    return merged


# ====================
# Numerical Computation
# ====================

def factorial(n):
    """Calculate factorial"""
    if n <= 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def fibonacci(n):
    """Calculate nth Fibonacci number"""
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def is_prime(n):
    """Check if number is prime"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    # Check odd divisors up to sqrt(n)
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def count_primes_in_range(start, end):
    """Count prime numbers in a range"""
    count = 0
    for n in range(start, end + 1):
        if is_prime(n):
            count += 1
    return count


# ====================
# Matrix Operations
# ====================

def matrix_multiply_row(row_a, matrix_b):
    """
    Multiply one row of matrix A by entire matrix B
    Returns one row of the result
    """
    result_row = []
    num_cols = len(matrix_b[0])

    for col in range(num_cols):
        total = 0
        for i, val in enumerate(row_a):
            total += val * matrix_b[i][col]
        result_row.append(total)

    return result_row


def dot_product(vec_a, vec_b):
    """Calculate dot product of two vectors"""
    return sum(a * b for a, b in zip(vec_a, vec_b))


# ====================
# Cryptographic/Hash Functions
# ====================

def simple_hash(text):
    """Simple hash function (educational purposes)"""
    hash_val = 0
    for char in text:
        hash_val = (hash_val * 31 + ord(char)) % (2**32)
    return hash_val


def find_hash_collision(prefix, target_start, start_num, count):
    """
    Find numbers whose hash starts with target
    Example of embarrassingly parallel problem
    """
    results = []
    for i in range(start_num, start_num + count):
        text = f"{prefix}{i}"
        hash_val = simple_hash(text)
        if str(hash_val).startswith(str(target_start)):
            results.append((i, hash_val))
    return results


# ====================
# Statistics
# ====================

def variance(numbers):
    """Calculate variance of a list"""
    if not numbers:
        return 0
    mean = sum(numbers) / len(numbers)
    return sum((x - mean) ** 2 for x in numbers) / len(numbers)


def standard_deviation(numbers):
    """Calculate standard deviation"""
    import math
    return math.sqrt(variance(numbers))


# ====================
# Genetic Algorithm Example
# ====================

def evaluate_fitness(genome, target_sum):
    """
    Evaluate fitness of a genome (list of numbers)
    Fitness = how close sum is to target
    """
    return abs(sum(genome) - target_sum)


def mutate_genome(genome, mutation_rate=0.1):
    """Mutate a genome with given probability"""
    import random
    mutated = genome.copy()
    for i in range(len(mutated)):
        if random.random() < mutation_rate:
            mutated[i] = random.randint(0, 100)
    return mutated


# ====================
# Sensor Data Simulation
# ====================

def generate_sensor_reading(sensor_id, num_readings):
    """
    Simulate sensor readings
    Useful for IoT data processing demos
    """
    import random
    import time

    readings = []
    for i in range(num_readings):
        reading = {
            'sensor_id': sensor_id,
            'timestamp': time.time() + i,
            'temperature': 20 + random.uniform(-5, 5),
            'humidity': 50 + random.uniform(-10, 10),
            'pressure': 1013 + random.uniform(-20, 20)
        }
        readings.append(reading)

    return readings


def process_sensor_batch(readings):
    """Process a batch of sensor readings"""
    if not readings:
        return {}

    temps = [r['temperature'] for r in readings]
    humids = [r['humidity'] for r in readings]
    pressures = [r['pressure'] for r in readings]

    return {
        'count': len(readings),
        'avg_temp': sum(temps) / len(temps),
        'avg_humidity': sum(humids) / len(humids),
        'avg_pressure': sum(pressures) / len(pressures),
        'min_temp': min(temps),
        'max_temp': max(temps)
    }
