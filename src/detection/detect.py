import pandas as pd
import joblib
from pathlib import Path

MODEL = Path("src/models/network_iforest.joblib")
DATA = Path("data/processed/window_features.csv")
OUT = Path("data/processed/alerts.csv")

def main():
    df = pd.read_csv(DATA)
    model = joblib.load(MODEL)

    features = df[
        [
            "flow_count",
            "unique_dst_ports",
            "packets_sum",
            "bytes_sum",
            "bytes_per_packet",
            "avg_duration",
        ]
    ]

    scores = model.decision_function(features)
    preds = model.predict(features)

    df["anomaly_score"] = scores
    df["anomalous"] = preds == -1

    alerts = df[df["anomalous"]].sort_values("anomaly_score")
    alerts.to_csv(OUT, index=False)

if __name__ == "__main__":
    main()
