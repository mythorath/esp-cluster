#!/usr/bin/env python3
"""
ESP32 Cluster Test Suite
Demonstrates various distributed computing patterns using the Broccoli framework
"""

import sys
import os
import time

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from codes.broccoli.client.client import Client
# Note: canvas module should be available after client initialization


def wait_for_cluster(client, timeout=30):
    """Wait for cluster to be ready"""
    print("Waiting for cluster to be ready...")
    start_time = time.time()

    while not client.status['Is connected']:
        if time.time() - start_time > timeout:
            print("Timeout waiting for cluster!")
            return False
        time.sleep(1)
        print('.', end='', flush=True)

    print("\n✓ Cluster ready!")
    return True


def test_basic_operations(client):
    """Test basic arithmetic operations"""
    print("\n" + "="*60)
    print("TEST 1: Basic Arithmetic Operations")
    print("="*60)

    from canvas import group
    import cluster_tasks as tasks

    # Parallel multiplication
    print("\nRunning parallel multiplications: 0*1, 1*2, 2*3, ..., 9*10")
    gp = group([tasks.mul.s(n, n+1) for n in range(10)])
    results = gp.get()
    print(f"Results: {results}")
    print(f"Expected: [0, 2, 6, 12, 20, 30, 42, 56, 72, 90]")


def test_chains(client):
    """Test chained operations"""
    print("\n" + "="*60)
    print("TEST 2: Chained Operations")
    print("="*60)

    from canvas import chain
    import cluster_tasks as tasks

    print("\nCalculating: ((4 + 4) * 8) * 10")
    ch = chain(tasks.add.s(4, 4), tasks.mul.s(8), tasks.mul.s(10))
    result = ch.get()
    print(f"Result: {result}")
    print(f"Expected: 640")


def test_map_reduce(client):
    """Test map-reduce pattern"""
    print("\n" + "="*60)
    print("TEST 3: Map-Reduce Pattern (Sum of Squares)")
    print("="*60)

    from canvas import chord
    import cluster_tasks as tasks

    print("\nCalculating sum of squares: sum((2*i)^2 for i in range(20))")

    # Map: square each number
    # Reduce: sum all results
    header = [tasks.mul.s(i, i) for i in range(2, 40, 2)]  # 2, 4, 6, ..., 38
    callback = tasks.xsum.s()

    async_result = chord(header)(callback)
    result = async_result.get()

    # Expected: sum of 2^2, 4^2, 6^2, ..., 38^2 = 4 + 16 + 36 + ... + 1444
    expected = sum(i*i for i in range(2, 40, 2))

    print(f"Result: {result}")
    print(f"Expected: {expected}")


def test_monte_carlo_pi(client):
    """Test Monte Carlo Pi estimation"""
    print("\n" + "="*60)
    print("TEST 4: Monte Carlo Pi Estimation")
    print("="*60)

    from canvas import group
    import cluster_tasks as tasks

    iterations_per_node = 10000
    num_nodes = 9  # Use all 9 ESP32s

    print(f"\nRunning {iterations_per_node} iterations on {num_nodes} nodes")
    print(f"Total iterations: {iterations_per_node * num_nodes}")

    # Distribute computation across nodes
    gp = group([
        tasks.monte_carlo_pi.s(iterations_per_node)
        for _ in range(num_nodes)
    ])

    start_time = time.time()
    results = gp.get()
    elapsed = time.time() - start_time

    # Calculate average
    pi_estimate = sum(results) / len(results)

    print(f"\nResults from each node: {results}")
    print(f"Average Pi estimate: {pi_estimate}")
    print(f"Actual Pi: 3.14159265359")
    print(f"Error: {abs(pi_estimate - 3.14159265359)}")
    print(f"Time elapsed: {elapsed:.2f} seconds")


def test_prime_counting(client):
    """Test distributed prime counting"""
    print("\n" + "="*60)
    print("TEST 5: Distributed Prime Counting")
    print("="*60)

    from canvas import group
    import cluster_tasks as tasks

    # Count primes from 1 to 10000, distributed across nodes
    range_start = 1
    range_end = 10000
    num_chunks = 9

    chunk_size = (range_end - range_start + 1) // num_chunks

    print(f"\nCounting primes from {range_start} to {range_end}")
    print(f"Distributed across {num_chunks} nodes")

    # Create chunks for each node
    chunks = []
    for i in range(num_chunks):
        start = range_start + i * chunk_size
        end = start + chunk_size - 1 if i < num_chunks - 1 else range_end
        chunks.append((start, end))

    # Distribute work
    gp = group([
        tasks.count_primes_in_range.s(start, end)
        for start, end in chunks
    ])

    start_time = time.time()
    results = gp.get()
    elapsed = time.time() - start_time

    total_primes = sum(results)

    print(f"\nPrimes found in each chunk: {results}")
    print(f"Total primes found: {total_primes}")
    print(f"Time elapsed: {elapsed:.2f} seconds")


def test_word_count(client):
    """Test distributed word counting (MapReduce)"""
    print("\n" + "="*60)
    print("TEST 6: Distributed Word Count (MapReduce)")
    print("="*60)

    from canvas import group, chord
    import cluster_tasks as tasks

    # Sample text chunks
    text_chunks = [
        "the quick brown fox jumps over the lazy dog",
        "the lazy dog sleeps under the warm sun",
        "the quick fox runs through the green forest",
        "brown bears and quick foxes live in the forest",
        "the warm sun shines over the lazy valley",
        "quick runners jump over the high fence",
        "the brown fence surrounds the green valley",
        "lazy cats sleep under the warm blanket",
        "the quick bird flies over the tall tree"
    ]

    print(f"\nCounting words across {len(text_chunks)} text chunks")

    # Map phase: count words in each chunk
    map_group = group([
        tasks.word_count.s(text)
        for text in text_chunks
    ])

    # Reduce phase: merge all counts
    async_result = chord(map_group)(tasks.merge_word_counts.s())

    start_time = time.time()
    word_counts = async_result.get()
    elapsed = time.time() - start_time

    # Sort by frequency
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

    print(f"\nTop 10 words:")
    for word, count in sorted_words[:10]:
        print(f"  {word}: {count}")

    print(f"\nTime elapsed: {elapsed:.2f} seconds")
    print(f"Total unique words: {len(word_counts)}")


def test_matrix_multiplication(client):
    """Test distributed matrix multiplication"""
    print("\n" + "="*60)
    print("TEST 7: Distributed Matrix Multiplication")
    print("="*60)

    from canvas import group
    import cluster_tasks as tasks

    # Small matrices for testing
    matrix_a = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]

    matrix_b = [
        [9, 8, 7],
        [6, 5, 4],
        [3, 2, 1]
    ]

    print("\nMatrix A:")
    for row in matrix_a:
        print(f"  {row}")

    print("\nMatrix B:")
    for row in matrix_b:
        print(f"  {row}")

    # Distribute each row multiplication to a different node
    gp = group([
        tasks.matrix_multiply_row.s(row, matrix_b)
        for row in matrix_a
    ])

    start_time = time.time()
    result_matrix = gp.get()
    elapsed = time.time() - start_time

    print("\nResult (A × B):")
    for row in result_matrix:
        print(f"  {row}")

    print(f"\nTime elapsed: {elapsed:.2f} seconds")


def main():
    """Run all cluster tests"""
    print("="*60)
    print("ESP32 Cluster Test Suite")
    print("="*60)

    # Initialize client
    print("\nInitializing cluster client...")
    client = Client()
    client.start()

    # Wait for cluster to be ready
    if not wait_for_cluster(client):
        print("Failed to connect to cluster!")
        client.stop()
        return

    # Deploy task definitions to cluster
    print("\nDeploying task definitions to cluster nodes...")
    client.sync_file('cluster_tasks.py', load_as_tasks=True)
    time.sleep(3)  # Give nodes time to load tasks

    print("\n✓ Cluster initialized and ready!")

    # Run tests
    try:
        test_basic_operations(client)
        time.sleep(2)

        test_chains(client)
        time.sleep(2)

        test_map_reduce(client)
        time.sleep(2)

        test_monte_carlo_pi(client)
        time.sleep(2)

        test_prime_counting(client)
        time.sleep(2)

        test_word_count(client)
        time.sleep(2)

        test_matrix_multiplication(client)

    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
    except Exception as e:
        print(f"\n\nError during tests: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n\nStopping cluster client...")
        client.stop()

    print("\n" + "="*60)
    print("Tests Complete!")
    print("="*60)


if __name__ == '__main__':
    main()
