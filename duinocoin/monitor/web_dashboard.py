#!/usr/bin/env python3
"""
DuinoCoin ESP32 Cluster Web Dashboard
Simple web interface for monitoring the cluster

Run on K2B to access from any browser on the network
"""

from flask import Flask, render_template_string, jsonify
import json
import requests
from datetime import datetime
from typing import Dict, List

app = Flask(__name__)

# HTML Template with embedded CSS and JavaScript
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>DuinoCoin ESP32 Cluster Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        h1 {
            text-align: center;
            margin-bottom: 10px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .subtitle {
            text-align: center;
            margin-bottom: 30px;
            opacity: 0.9;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: transform 0.3s;
        }
        .stat-card:hover {
            transform: translateY(-5px);
        }
        .stat-label {
            font-size: 0.9em;
            opacity: 0.8;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .stat-value {
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .stat-unit {
            font-size: 0.9em;
            opacity: 0.7;
        }
        .miners-section {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .miners-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        .miner-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .miner-card.online {
            border-left: 4px solid #10b981;
        }
        .miner-card.offline {
            border-left: 4px solid #ef4444;
            opacity: 0.6;
        }
        .miner-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        .miner-name {
            font-size: 1.2em;
            font-weight: bold;
        }
        .status-badge {
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
        }
        .status-online {
            background: #10b981;
        }
        .status-offline {
            background: #ef4444;
        }
        .miner-stats {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            font-size: 0.9em;
        }
        .miner-stat {
            opacity: 0.9;
        }
        .update-time {
            text-align: center;
            margin-top: 20px;
            opacity: 0.7;
            font-size: 0.9em;
        }
        .refresh-btn {
            display: block;
            margin: 20px auto;
            padding: 12px 30px;
            background: rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 25px;
            color: white;
            cursor: pointer;
            font-size: 1em;
            transition: all 0.3s;
        }
        .refresh-btn:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: scale(1.05);
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .loading {
            animation: pulse 2s infinite;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>⛏️ DuinoCoin ESP32 Cluster</h1>
        <div class="subtitle">Real-time Mining Dashboard</div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Total Hashrate</div>
                <div class="stat-value" id="total-hashrate">0.0</div>
                <div class="stat-unit">MH/s</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Miners Online</div>
                <div class="stat-value" id="miners-online">0</div>
                <div class="stat-unit">/ 9 nodes</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Accepted Shares</div>
                <div class="stat-value" id="total-shares">0</div>
                <div class="stat-unit">accepted</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Daily Earnings</div>
                <div class="stat-value" id="daily-earnings">0</div>
                <div class="stat-unit">DUCO</div>
            </div>
        </div>

        <div class="miners-section">
            <h2>🖥️ Individual Miners</h2>
            <div class="miners-grid" id="miners-grid">
                <!-- Miner cards will be inserted here -->
            </div>
        </div>

        <button class="refresh-btn" onclick="loadData()">🔄 Refresh Now</button>
        <div class="update-time">Last updated: <span id="update-time">Never</span></div>
    </div>

    <script>
        function loadData() {
            document.getElementById('miners-grid').classList.add('loading');

            fetch('/api/stats')
                .then(response => response.json())
                .then(data => {
                    updateDashboard(data);
                    document.getElementById('miners-grid').classList.remove('loading');
                })
                .catch(error => {
                    console.error('Error fetching data:', error);
                    document.getElementById('miners-grid').classList.remove('loading');
                });
        }

        function updateDashboard(data) {
            // Update summary stats
            document.getElementById('total-hashrate').textContent =
                (data.cluster.total_hashrate / 1000).toFixed(3);
            document.getElementById('miners-online').textContent =
                data.cluster.online_miners;
            document.getElementById('total-shares').textContent =
                data.cluster.total_shares_accepted.toLocaleString();
            document.getElementById('daily-earnings').textContent =
                Math.round(data.cluster.online_miners * 10);

            // Update miner cards
            const minersGrid = document.getElementById('miners-grid');
            minersGrid.innerHTML = '';

            data.miners.forEach(miner => {
                const card = createMinerCard(miner);
                minersGrid.appendChild(card);
            });

            // Update timestamp
            document.getElementById('update-time').textContent =
                new Date().toLocaleTimeString();
        }

        function createMinerCard(miner) {
            const card = document.createElement('div');
            card.className = `miner-card ${miner.online ? 'online' : 'offline'}`;

            card.innerHTML = `
                <div class="miner-header">
                    <div class="miner-name">${miner.rig_id}</div>
                    <div class="status-badge status-${miner.online ? 'online' : 'offline'}">
                        ${miner.online ? '🟢 ONLINE' : '🔴 OFFLINE'}
                    </div>
                </div>
                <div class="miner-stats">
                    <div class="miner-stat">
                        <strong>Hashrate:</strong><br>
                        ${miner.hashrate.toFixed(1)} kH/s
                    </div>
                    <div class="miner-stat">
                        <strong>Shares:</strong><br>
                        ${miner.shares_accepted.toLocaleString()}
                    </div>
                    <div class="miner-stat">
                        <strong>Uptime:</strong><br>
                        ${Math.floor(miner.uptime / 3600)}h ${Math.floor((miner.uptime % 3600) / 60)}m
                    </div>
                    <div class="miner-stat">
                        <strong>Difficulty:</strong><br>
                        ${miner.difficulty}
                    </div>
                </div>
            `;

            return card;
        }

        // Auto-refresh every 10 seconds
        setInterval(loadData, 10000);

        // Initial load
        loadData();
    </script>
</body>
</html>
"""


class ClusterAPI:
    """API for accessing cluster stats"""

    def __init__(self, config_file: str):
        self.config = self.load_config(config_file)
        self.miners = []
        self.initialize_miners()

    def load_config(self, config_file: str) -> Dict:
        """Load configuration"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"miners": []}

    def initialize_miners(self):
        """Initialize miner list from config"""
        for miner in self.config.get('miners', []):
            self.miners.append({
                'rig_id': miner['rig_identifier'],
                'ip': miner.get('ip', f"192.168.1.{100 + miner['id']}"),
                'online': False,
                'hashrate': 0,
                'shares_accepted': 0,
                'shares_rejected': 0,
                'uptime': 0,
                'difficulty': 0
            })

    def get_cluster_stats(self) -> Dict:
        """Get current cluster statistics"""
        # In production, this would poll actual miners
        # For now, return simulated data

        online_miners = sum(1 for m in self.miners if m['online'])
        total_hashrate = sum(m['hashrate'] for m in self.miners)
        total_shares = sum(m['shares_accepted'] for m in self.miners)

        return {
            'cluster': {
                'total_miners': len(self.miners),
                'online_miners': online_miners,
                'offline_miners': len(self.miners) - online_miners,
                'total_hashrate': total_hashrate,
                'total_shares_accepted': total_shares,
                'total_shares_rejected': sum(m['shares_rejected'] for m in self.miners),
                'avg_hashrate': total_hashrate / online_miners if online_miners > 0 else 0
            },
            'miners': self.miners,
            'timestamp': datetime.now().isoformat()
        }


# Initialize API
api = ClusterAPI('../config/miner_configs.json')


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/stats')
def stats():
    """API endpoint for statistics"""
    return jsonify(api.get_cluster_stats())


def main():
    print("=" * 60)
    print("DuinoCoin ESP32 Cluster Web Dashboard")
    print("=" * 60)
    print("\nStarting web server...")
    print("Access dashboard at: http://YOUR_K2B_IP:5000")
    print("\nPress Ctrl+C to stop\n")

    app.run(host='0.0.0.0', port=5000, debug=False)


if __name__ == '__main__':
    main()
