#!/usr/bin/env python3
"""
ESP32 Cluster Coordinator
Manages the cluster for different types of tasks:
- DuinoCoin mining
- Distributed computing
- Parallel algorithms
- Mixed workloads

This allows you to switch between mining and computing on demand.
"""

import sys
import os
import time
from typing import Dict, List

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from codes.broccoli.client.client import Client


class ClusterCoordinator:
    """Coordinates tasks across the ESP32 cluster"""

    def __init__(self, duinocoin_username=None):
        self.client = None
        self.duinocoin_username = duinocoin_username
        self.cluster_mode = None  # 'idle', 'mining', 'computing', 'mixed'

    def start_cluster(self):
        """Initialize cluster connection"""
        print("Starting cluster coordinator...")
        self.client = Client()
        self.client.start()

        # Wait for cluster to be ready
        timeout = 30
        start = time.time()
        while not self.client.status['Is connected']:
            if time.time() - start > timeout:
                print("ERROR: Cluster connection timeout")
                return False
            time.sleep(1)
            print('.', end='', flush=True)

        print("\n✓ Cluster connected!")
        return True

    def deploy_tasks(self, task_files: List[str]):
        """Deploy task definitions to cluster"""
        print(f"\nDeploying {len(task_files)} task file(s) to cluster...")

        for task_file in task_files:
            print(f"  - {task_file}")
            self.client.sync_file(task_file, load_as_tasks=True)
            time.sleep(2)  # Give nodes time to load

        print("✓ Tasks deployed!")

    def mine_duinocoin(self, duration_minutes=60, shares_per_node=None):
        """
        Set cluster to mine DuinoCoin

        Args:
            duration_minutes: How long to mine (if shares_per_node is None)
            shares_per_node: Number of shares per node (if set, ignores duration)
        """
        if not self.duinocoin_username:
            print("ERROR: No DuinoCoin username configured")
            return

        print("=" * 60)
        print(f"Starting DuinoCoin Mining on Cluster")
        print("=" * 60)
        print(f"Username: {self.duinocoin_username}")

        if shares_per_node:
            print(f"Mode: Mine {shares_per_node} shares per node")
        else:
            print(f"Mode: Mine for {duration_minutes} minutes")

        print()

        from canvas import group
        import duinocoin_task as tasks

        self.cluster_mode = 'mining'

        if shares_per_node:
            # Mine specific number of shares on each node
            print(f"Distributing mining task to 9 nodes...")
            gp = group([
                tasks.mine_duinocoin_shares.s(
                    self.duinocoin_username,
                    shares_per_node,
                    f"ESP32-Node-{i}"
                )
                for i in range(1, 10)
            ])
        else:
            # Mine continuously for duration
            duration_sec = duration_minutes * 60
            print(f"Mining for {duration_minutes} minutes ({duration_sec} seconds)...")
            gp = group([
                tasks.mine_continuous.s(
                    self.duinocoin_username,
                    duration_sec,
                    f"ESP32-Node-{i}"
                )
                for i in range(1, 10)
            ])

        start_time = time.time()
        results = gp.get()
        elapsed = time.time() - start_time

        # Aggregate results
        self._display_mining_results(results, elapsed)

    def run_computation(self, task_name, *args, **kwargs):
        """Run distributed computation task"""
        print("=" * 60)
        print(f"Running Computation: {task_name}")
        print("=" * 60)

        self.cluster_mode = 'computing'

        # Example: This would execute the named task
        # Implementation depends on your specific tasks
        print(f"Task: {task_name}")
        print(f"Args: {args}")
        print(f"Kwargs: {kwargs}")

    def mixed_workload(self, mine_ratio=0.5):
        """
        Run mixed workload: part mining, part computing

        Args:
            mine_ratio: Ratio of nodes to dedicate to mining (0.0-1.0)
        """
        print("=" * 60)
        print("Running Mixed Workload")
        print("=" * 60)

        num_miners = int(9 * mine_ratio)
        num_computers = 9 - num_miners

        print(f"Mining nodes: {num_miners}")
        print(f"Computing nodes: {num_computers}")
        print()

        self.cluster_mode = 'mixed'

        # This would split tasks between nodes
        # Implementation depends on specific use case

    def stop_all_tasks(self):
        """Stop all cluster tasks"""
        print("\nStopping all cluster tasks...")
        self.cluster_mode = 'idle'
        # Implementation would send stop signal to all nodes

    def get_cluster_status(self) -> Dict:
        """Get current cluster status"""
        return {
            'connected': self.client.status['Is connected'] if self.client else False,
            'mode': self.cluster_mode,
            'broker_status': self.client.status if self.client else {}
        }

    def _display_mining_results(self, results, elapsed):
        """Display mining results"""
        print("\n" + "=" * 60)
        print("Mining Results")
        print("=" * 60)

        total_accepted = sum(r.get('shares_accepted', 0) for r in results)
        total_rejected = sum(r.get('shares_rejected', 0) for r in results)
        total_shares = total_accepted + total_rejected
        acceptance_rate = (total_accepted / total_shares * 100) if total_shares > 0 else 0

        print(f"\nCluster Statistics:")
        print(f"  Total Time: {elapsed:.1f} seconds ({elapsed/60:.1f} minutes)")
        print(f"  Shares Accepted: {total_accepted}")
        print(f"  Shares Rejected: {total_rejected}")
        print(f"  Acceptance Rate: {acceptance_rate:.2f}%")

        print(f"\nPer-Node Results:")
        for i, result in enumerate(results, 1):
            if result.get('success'):
                print(f"  Node {i}: {result.get('shares_accepted', 0)} accepted, "
                      f"{result.get('shares_rejected', 0)} rejected")
            else:
                print(f"  Node {i}: ERROR - {result.get('error', 'Unknown')}")

        # Estimate earnings (rough)
        # DuinoCoin pays per accepted share, amount varies by difficulty
        estimated_duco = total_accepted * 0.001  # Very rough estimate
        print(f"\nEstimated Earnings: ~{estimated_duco:.3f} DUCO")
        print("=" * 60)

    def shutdown(self):
        """Shutdown cluster coordinator"""
        print("\nShutting down cluster coordinator...")
        if self.client:
            self.client.stop()
        print("✓ Shutdown complete")


def main():
    """Example usage"""
    import argparse

    parser = argparse.ArgumentParser(description='ESP32 Cluster Coordinator')
    parser.add_argument('--mode', choices=['mine', 'compute', 'mixed'],
                       required=True, help='Cluster mode')
    parser.add_argument('--username', help='DuinoCoin username (for mining)')
    parser.add_argument('--duration', type=int, default=60,
                       help='Mining duration in minutes')
    parser.add_argument('--shares', type=int,
                       help='Number of shares to mine per node')

    args = parser.parse_args()

    coordinator = ClusterCoordinator(duinocoin_username=args.username)

    try:
        # Start cluster
        if not coordinator.start_cluster():
            print("Failed to start cluster")
            return

        # Deploy tasks
        if args.mode == 'mine':
            coordinator.deploy_tasks(['duinocoin_task.py'])
            coordinator.mine_duinocoin(
                duration_minutes=args.duration,
                shares_per_node=args.shares
            )

        elif args.mode == 'compute':
            coordinator.deploy_tasks(['cluster_tasks.py'])
            # Run your computation tasks here
            print("Deploy your computation tasks...")

        elif args.mode == 'mixed':
            coordinator.deploy_tasks(['duinocoin_task.py', 'cluster_tasks.py'])
            coordinator.mixed_workload(mine_ratio=0.5)

    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    finally:
        coordinator.shutdown()


if __name__ == '__main__':
    main()
