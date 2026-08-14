import os
import time
import psutil


class HardwareMonitor:
    """Read-only live system telemetry for JARVIS."""

    def cpu(self) -> dict:
        return {
            "usage_percent": psutil.cpu_percent(interval=0.2),
            "cores": psutil.cpu_count(logical=False),
            "threads": psutil.cpu_count(logical=True),
        }

    def memory(self) -> dict:
        mem = psutil.virtual_memory()

        return {
            "total_mb": round(mem.total / (1024 ** 2)),
            "available_mb": round(mem.available / (1024 ** 2)),
            "used_mb": round(mem.used / (1024 ** 2)),
            "usage_percent": mem.percent,
        }

    def snapshot(self) -> dict:
        return {
            "cpu": self.cpu(),
            "memory": self.memory(),
        }


if __name__ == "__main__":
    monitor = HardwareMonitor()

    print("JARVIS Live Hardware Monitor")
    print("============================")

    for _ in range(5):
        snapshot = monitor.snapshot()

        print(
            f"CPU: {snapshot['cpu']['usage_percent']:.1f}% | "
            f"RAM: {snapshot['memory']['used_mb']} / "
            f"{snapshot['memory']['total_mb']} MB "
            f"({snapshot['memory']['usage_percent']:.1f}%) | "
            f"Available: {snapshot['memory']['available_mb']} MB"
        )

        time.sleep(1)
