import json
import random
from datetime import datetime, timedelta
from pathlib import Path

OUT = Path("data/raw/flows.jsonl")
OUT.parent.mkdir(parents=True, exist_ok=True)

INTERNAL_IPS = ["10.0.1.10", "10.0.1.11", "10.0.2.20"]
EXTERNAL_IPS = ["198.51.100.10", "203.0.113.55", "192.0.2.77"]
NORMAL_PORTS = [80, 443, 53]
SCAN_PORTS = list(range(20, 1024))

def ts(base, seconds):
    return (base + timedelta(seconds=seconds)).isoformat() + "Z"

def main():
    base = datetime.utcnow() - timedelta(hours=1)
    rows = []

    # Normal traffic
    for i in range(1500):
        rows.append({
            "timestamp": ts(base, i * 2),
            "src_ip": random.choice(INTERNAL_IPS),
            "dst_ip": random.choice(EXTERNAL_IPS),
            "dst_port": random.choice(NORMAL_PORTS),
            "protocol": "tcp",
            "packets": random.randint(5, 40),
            "bytes": random.randint(500, 50000),
            "duration": random.uniform(0.2, 2.0),
            "direction": "outbound"
        })

    # Port scan anomaly
    attacker = "198.51.100.10"
    victim = "10.0.1.10"
    for i, port in enumerate(random.sample(SCAN_PORTS, 300)):
        rows.append({
            "timestamp": ts(base, 4000 + i),
            "src_ip": attacker,
            "dst_ip": victim,
            "dst_port": port,
            "protocol": "tcp",
            "packets": random.randint(1, 3),
            "bytes": random.randint(40, 200),
            "duration": random.uniform(0.01, 0.2),
            "direction": "inbound"
        })

    # Data exfiltration anomaly
    for i in range(60):
        rows.append({
            "timestamp": ts(base, 4600 + i * 5),
            "src_ip": "10.0.2.20",
            "dst_ip": "203.0.113.55",
            "dst_port": 443,
            "protocol": "tcp",
            "packets": random.randint(300, 800),
            "bytes": random.randint(5_000_000, 20_000_000),
            "duration": random.uniform(30, 120),
            "direction": "outbound"
        })

    random.shuffle(rows)

    with OUT.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")

if __name__ == "__main__":
    main()
