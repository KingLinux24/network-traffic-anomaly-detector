def explain(row):
    reasons = []

    if row["unique_dst_ports"] > 20:
        reasons.append("Unusually high number of destination ports (possible scanning)")
    if row["bytes_sum"] > 10_000_000:
        reasons.append("Very high outbound data volume (possible exfiltration)")
    if row["avg_duration"] > 30:
        reasons.append("Long-lived connections atypical for baseline")
    if row["bytes_per_packet"] < 200:
        reasons.append("Low bytes per packet consistent with probing")

    if not reasons:
        reasons.append("Traffic pattern deviates from learned baseline")

    return reasons
