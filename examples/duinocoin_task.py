"""
DuinoCoin Mining Task for Broccoli Cluster
This allows the ESP32 cluster to mine DuinoCoin as a distributed task
alongside other computational tasks.

The cluster can switch between:
- Mining DuinoCoin
- Running distributed computations
- Processing parallel algorithms
- Any other tasks you define
"""

import socket
import hashlib
import time
from micropython import const

# DuinoCoin pool settings
DUINOCOIN_POOL = "server.duinocoin.com"
DUINOCOIN_PORT = 2811  # AVR/ESP8266 difficulty port (MicroPython is slower)

# Mining configuration
USERNAME = "YOUR_USERNAME"  # Set this in deployment
MINING_KEY = "None"  # Optional miner key
INTENSITY = 95  # Mining intensity (1-100)


class DuinoCoinMiner:
    """MicroPython DuinoCoin miner for ESP32 cluster nodes"""

    def __init__(self, username, miner_key="None", node_id="ESP32-Node"):
        self.username = username
        self.miner_key = miner_key
        self.node_id = node_id
        self.socket = None
        self.shares_accepted = 0
        self.shares_rejected = 0

    def connect_to_pool(self):
        """Connect to DuinoCoin mining pool"""
        try:
            self.socket = socket.socket()
            self.socket.connect(socket.getaddrinfo(DUINOCOIN_POOL, DUINOCOIN_PORT)[0][-1])
            # Receive server version
            server_version = self.socket.recv(100).decode().rstrip('\n')
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False

    def request_job(self):
        """Request mining job from pool"""
        try:
            # Send job request
            request = f"JOB,{self.username},{INTENSITY}"
            if self.miner_key != "None":
                request += f",{self.miner_key}"

            self.socket.send(bytes(request + '\n', 'utf8'))

            # Receive job
            job = self.socket.recv(128).decode().rstrip('\n')

            # Parse job: hash,expected_hash,difficulty
            parts = job.split(',')
            if len(parts) >= 3:
                return {
                    'hash': parts[0],
                    'expected_hash': parts[1],
                    'difficulty': int(parts[2])
                }
            return None

        except Exception as e:
            print(f"Job request error: {e}")
            return None

    def mine_share(self, job, max_time=5):
        """
        Mine a share for the given job
        max_time: maximum time to spend mining (seconds)
        """
        start_time = time.time()
        base_hash = job['hash']
        expected_hash = job['expected_hash']
        difficulty = job['difficulty']

        # Try different nonces
        for nonce in range(difficulty * 100):
            # Check timeout
            if time.time() - start_time > max_time:
                return None

            # Calculate hash
            test_hash = hashlib.sha1(
                bytes(base_hash + str(nonce), 'utf8')
            ).hexdigest()

            # Check if we found the solution
            if test_hash == expected_hash:
                return nonce

        return None

    def submit_share(self, nonce, hashrate, miner_software="Broccoli-MicroPython"):
        """Submit found share to pool"""
        try:
            response_msg = f"{nonce},{hashrate},{miner_software},{self.node_id}"
            self.socket.send(bytes(response_msg + '\n', 'utf8'))

            # Receive feedback
            feedback = self.socket.recv(128).decode().rstrip('\n')

            if feedback == "GOOD":
                self.shares_accepted += 1
                return True
            else:
                self.shares_rejected += 1
                return False

        except Exception as e:
            print(f"Submit error: {e}")
            return False

    def disconnect(self):
        """Disconnect from pool"""
        if self.socket:
            try:
                self.socket.close()
            except:
                pass


def mine_duinocoin_shares(username, num_shares=10, node_id="ESP32-Node"):
    """
    Mine specified number of DuinoCoin shares
    This is a task that can be distributed across the cluster

    Args:
        username: DuinoCoin username
        num_shares: Number of shares to attempt
        node_id: Identifier for this node

    Returns:
        dict with mining statistics
    """
    miner = DuinoCoinMiner(username, node_id=node_id)

    if not miner.connect_to_pool():
        return {
            'success': False,
            'error': 'Failed to connect to pool'
        }

    shares_found = 0
    total_time = 0

    try:
        for _ in range(num_shares):
            start_time = time.time()

            # Get job
            job = miner.request_job()
            if not job:
                continue

            # Mine the share
            nonce = miner.mine_share(job, max_time=10)

            elapsed = time.time() - start_time
            total_time += elapsed

            if nonce is not None:
                # Calculate hashrate
                hashrate = job['difficulty'] / elapsed if elapsed > 0 else 0

                # Submit share
                if miner.submit_share(nonce, hashrate):
                    shares_found += 1

        avg_hashrate = (sum([job['difficulty'] for _ in range(shares_found)]) /
                       total_time if total_time > 0 else 0)

        return {
            'success': True,
            'node_id': node_id,
            'shares_attempted': num_shares,
            'shares_accepted': miner.shares_accepted,
            'shares_rejected': miner.shares_rejected,
            'avg_hashrate': avg_hashrate,
            'total_time': total_time
        }

    finally:
        miner.disconnect()


def mine_continuous(username, duration_seconds=300, node_id="ESP32-Node"):
    """
    Mine continuously for specified duration

    Args:
        username: DuinoCoin username
        duration_seconds: How long to mine
        node_id: Node identifier

    Returns:
        Mining statistics
    """
    miner = DuinoCoinMiner(username, node_id=node_id)

    if not miner.connect_to_pool():
        return {
            'success': False,
            'error': 'Failed to connect to pool'
        }

    start_time = time.time()
    end_time = start_time + duration_seconds

    try:
        while time.time() < end_time:
            job = miner.request_job()
            if not job:
                continue

            nonce = miner.mine_share(job, max_time=10)

            if nonce is not None:
                elapsed = time.time() - start_time
                hashrate = job['difficulty'] / elapsed if elapsed > 0 else 0
                miner.submit_share(nonce, hashrate)

        total_time = time.time() - start_time

        return {
            'success': True,
            'node_id': node_id,
            'shares_accepted': miner.shares_accepted,
            'shares_rejected': miner.shares_rejected,
            'mining_time': total_time,
            'avg_hashrate': (miner.shares_accepted / total_time * 100
                           if total_time > 0 else 0)
        }

    finally:
        miner.disconnect()


# Export tasks for Broccoli cluster
__all__ = ['mine_duinocoin_shares', 'mine_continuous']
