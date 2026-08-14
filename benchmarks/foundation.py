import json
import time
from datetime import datetime, timezone
from pathlib import Path

import psutil


ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = ROOT / "benchmarks" / "results"


def cpu_benchmark(duration: float = 5.0) -> dict:
    start = time.perf_counter()
    iterations = 0

    while time.perf_counter() - start < duration:
        # Deterministic CPU workload.
        value = 0
        for i in range(1, 10001):
            value += (i * i) % 9973
        iterations += 1

    elapsed = time.perf_counter() - start

    return {
        "duration_seconds": elapsed,
        "iterations": iterations,
        "iterations_per_second": iterations / elapsed,
    }


def memory_snapshot() -> dict:
    memory = psutil.virtual_memory()

    return {
        "total_mb": round(memory.total / (1024 ** 2)),
        "available_mb": round(memory.available / (1024 ** 2)),
        "used_mb": round(memory.used / (1024 ** 2)),
        "usage_percent": memory.percent,
    }


def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    print("JARVIS Benchmark Foundation v0.1")
    print("=================================")
    print("Running CPU benchmark...")
    
    before = memory_snapshot()
    result = cpu_benchmark()
    after = memory_snapshot()

    benchmark = {
        "benchmark": "foundation_v0.1",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "cpu": {
            "name": "Intel Xeon X5650",
            "cores": psutil.cpu_count(logical=False),
            "threads": psutil.cpu_count(logical=True),
        },
        "memory_before": before,
        "memory_after": after,
        "cpu_result": result,
    }

    output = RESULTS_DIR / "foundation_v0.1.json"

    with output.open("w", encoding="utf-8") as file:
        json.dump(benchmark, file, indent=2)

    print()
    print("CPU:")
    print(f"  Cores: {benchmark['cpu']['cores']}")
    print(f"  Threads: {benchmark['cpu']['threads']}")
    print(f"  Iterations: {result['iterations']}")
    print(f"  Iterations/sec: {result['iterations_per_second']:.2f}")

    print()
    print("RAM Before:")
    print(f"  Available: {before['available_mb']} MB")

    print("RAM After:")
    print(f"  Available: {after['available_mb']} MB")

    print()
    print(f"Saved: {output}")


if __name__ == "__main__":
    main()
