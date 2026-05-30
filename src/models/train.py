import pandas as pd
import joblib
from pathlib import Path
from sklearn.ensemble import IsolationForest

DATA = Path("data/processed/window_features.csv")
MODEL_OUT = Path("src/models/network_iforest.joblib")

def main():
    df = pd.read_csv(DATA)

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

    model = IsolationForest(
        n_estimators=400,
        contamination=0.05,
        random_state=42,
        n_jobs=-1
    )

    model.fit(features)

    MODEL_OUT.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_OUT)

if __name__ == "__main__":
    main()
