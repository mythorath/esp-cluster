#!/usr/bin/env python3
"""
DuinoCoin ESP32 Cluster Monitor
Monitors all 9 ESP32 miners and displays aggregate statistics

Each ESP32 runs a web server on port 80 that provides JSON statistics.
This script polls all miners and displays combined stats.
"""

import json
import time
import requests
from datetime import datetime
from typing import List, Dict, Optional
import argparse


class MinerStats:
    """Statistics for a single miner"""
    def __init__(self, rig_id: str, ip: str):
        self.rig_id = rig_id
        self.ip = ip
        self.hashrate = 0
        self.shares_accepted = 0
        self.shares_rejected = 0
        self.uptime = 0
        self.difficulty = 0
        self.online = False
        self.last_update = None

    def update(self, data: Dict):
        """Update stats from API response"""
        try:
            self.hashrate = float(data.get('hashrate', 0))
            self.shares_accepted = int(data.get('accepted', 0))
            self.shares_rejected = int(data.get('rejected', 0))
            self.uptime = int(data.get('uptime', 0))
            self.difficulty = int(data.get('difficulty', 0))
            self.online = True
            self.last_update = datetime.now()
        except (ValueError, KeyError) as e:
            print(f"Error parsing data for {self.rig_id}: {e}")
            self.online = False

    def __str__(self):
        status = "🟢 ONLINE" if self.online else "🔴 OFFLINE"
        return (f"{self.rig_id:15} | {status} | "
                f"{self.hashrate:6.1f} kH/s | "
                f"Shares: {self.shares_accepted:5} | "
                f"Uptime: {self.uptime//3600:3}h")


class ClusterMonitor:
    """Monitors all ESP32 miners in the cluster"""

    def __init__(self, config_file: str = "../config/miner_configs.json"):
        self.miners: List[MinerStats] = []
        self.config = self.load_config(config_file)
        self.initialize_miners()

    def load_config(self, config_file: str) -> Dict:
        """Load miner configuration"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Config file not found: {config_file}")
            return {"miners": []}

    def initialize_miners(self):
        """Initialize miner objects from config"""
        # In real deployment, you'd have IP addresses
        # For now, we'll use placeholders
        for miner in self.config.get('miners', []):
            rig_id = miner['rig_identifier']
            # IP should be discovered or configured
            ip = miner.get('ip', f"192.168.1.{100 + miner['id']}")
            self.miners.append(MinerStats(rig_id, ip))

    def poll_miner(self, miner: MinerStats) -> bool:
        """Poll a single miner for statistics"""
        try:
            # Try to get stats from ESP32's web server
            # The actual endpoint depends on the ESP32 firmware
            url = f"http://{miner.ip}/api/stats"
            response = requests.get(url, timeout=3)

            if response.status_code == 200:
                data = response.json()
                miner.update(data)
                return True
            else:
                miner.online = False
                return False

        except requests.exceptions.RequestException:
            miner.online = False
            return False

    def poll_all_miners(self):
        """Poll all miners for current statistics"""
        for miner in self.miners:
            self.poll_miner(miner)

    def get_cluster_stats(self) -> Dict:
        """Calculate aggregate cluster statistics"""
        online_count = sum(1 for m in self.miners if m.online)
        total_hashrate = sum(m.hashrate for m in self.miners if m.online)
        total_shares = sum(m.shares_accepted for m in self.miners if m.online)
        total_rejected = sum(m.shares_rejected for m in self.miners if m.online)

        return {
            'total_miners': len(self.miners),
            'online_miners': online_count,
            'offline_miners': len(self.miners) - online_count,
            'total_hashrate': total_hashrate,
            'total_shares_accepted': total_shares,
            'total_shares_rejected': total_rejected,
            'avg_hashrate': total_hashrate / online_count if online_count > 0 else 0,
            'acceptance_rate': (total_shares / (total_shares + total_rejected) * 100
                              if (total_shares + total_rejected) > 0 else 0)
        }

    def display_stats(self):
        """Display formatted statistics"""
        cluster_stats = self.get_cluster_stats()

        # Clear screen (works on Linux/Mac)
        print("\033[2J\033[H")

        # Header
        print("=" * 80)
        print(f"{'DuinoCoin ESP32 Cluster Monitor':^80}")
        print(f"{'Updated: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'):^80}")
        print("=" * 80)

        # Cluster summary
        print("\n📊 CLUSTER SUMMARY")
        print("-" * 80)
        print(f"Miners Online:       {cluster_stats['online_miners']}/{cluster_stats['total_miners']}")
        print(f"Total Hashrate:      {cluster_stats['total_hashrate']:.1f} kH/s "
              f"({cluster_stats['total_hashrate']/1000:.3f} MH/s)")
        print(f"Average Hashrate:    {cluster_stats['avg_hashrate']:.1f} kH/s per miner")
        print(f"Accepted Shares:     {cluster_stats['total_shares_accepted']}")
        print(f"Rejected Shares:     {cluster_stats['total_shares_rejected']}")
        print(f"Acceptance Rate:     {cluster_stats['acceptance_rate']:.2f}%")

        # Estimated earnings (rough estimate)
        daily_duco = cluster_stats['online_miners'] * 10  # ~10 DUCO per ESP32/day
        print(f"Est. Daily Earnings: ~{daily_duco} DUCO")
        print(f"Est. Monthly:        ~{daily_duco * 30} DUCO")

        # Individual miners
        print("\n⛏️  INDIVIDUAL MINERS")
        print("-" * 80)
        print(f"{'Miner ID':15} | {'Status':8} | {'Hashrate':12} | {'Shares':13} | {'Uptime':11}")
        print("-" * 80)

        for miner in self.miners:
            print(miner)

        # Power consumption
        power_per_miner = 1.5  # Watts
        total_power = cluster_stats['online_miners'] * power_per_miner
        print("\n⚡ POWER CONSUMPTION")
        print("-" * 80)
        print(f"Per Miner:     ~{power_per_miner} W")
        print(f"Total Cluster: ~{total_power:.1f} W")
        print(f"Daily Usage:   ~{total_power * 24 / 1000:.2f} kWh")
        print(f"Monthly Usage: ~{total_power * 24 * 30 / 1000:.2f} kWh")

        print("\n" + "=" * 80)
        print("Press Ctrl+C to exit")

    def run(self, interval: int = 10):
        """Run monitoring loop"""
        print("Starting DuinoCoin Cluster Monitor...")
        print(f"Monitoring {len(self.miners)} miners")
        print(f"Update interval: {interval} seconds")
        print()

        try:
            while True:
                self.poll_all_miners()
                self.display_stats()
                time.sleep(interval)

        except KeyboardInterrupt:
            print("\n\nMonitoring stopped by user")


class SimpleMinerDiscovery:
    """Simple miner discovery using IP scanning"""

    @staticmethod
    def scan_subnet(subnet: str = "192.168.1", port: int = 80) -> List[str]:
        """
        Scan subnet for ESP32 miners
        Returns list of IP addresses that respond
        """
        print(f"Scanning {subnet}.0/24 for miners...")
        found_miners = []

        # This is a simple implementation
        # In production, you'd use proper network scanning
        for i in range(100, 120):  # Scan .100 to .120
            ip = f"{subnet}.{i}"
            try:
                response = requests.get(f"http://{ip}/api/stats",
                                       timeout=1)
                if response.status_code == 200:
                    print(f"Found miner at {ip}")
                    found_miners.append(ip)
            except requests.exceptions.RequestException:
                pass

        return found_miners


def main():
    parser = argparse.ArgumentParser(
        description='Monitor DuinoCoin ESP32 cluster'
    )
    parser.add_argument(
        '--config',
        default='../config/miner_configs.json',
        help='Path to miner config file'
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=10,
        help='Update interval in seconds'
    )
    parser.add_argument(
        '--discover',
        action='store_true',
        help='Scan network for miners'
    )

    args = parser.parse_args()

    if args.discover:
        print("Discovering miners on network...")
        discovery = SimpleMinerDiscovery()
        miners = discovery.scan_subnet()
        print(f"\nFound {len(miners)} miners:")
        for ip in miners:
            print(f"  - {ip}")
        return

    monitor = ClusterMonitor(args.config)
    monitor.run(args.interval)


if __name__ == '__main__':
    main()
