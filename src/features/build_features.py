import json
import pandas as pd
from pathlib import Path

IN = Path("data/raw/flows.jsonl")
OUT = Path("data/processed/window_features.csv")
OUT.parent.mkdir(parents=True, exist_ok=True)

def main():
    rows = []
    with IN.open("r") as f:
        for line in f:
            rows.append(json.loads(line))

    df = pd.DataFrame(rows)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["window"] = df["timestamp"].dt.floor("1min")

    grouped = df.groupby(["src_ip", "direction", "window"]).agg(
        flow_count=("dst_port", "count"),
        unique_dst_ports=("dst_port", "nunique"),
        packets_sum=("packets", "sum"),
        bytes_sum=("bytes", "sum"),
        avg_duration=("duration", "mean"),
    ).reset_index()

    grouped["bytes_per_packet"] = grouped["bytes_sum"] / (grouped["packets_sum"] + 1)

    grouped.to_csv(OUT, index=False)

if __name__ == "__main__":
    main()
