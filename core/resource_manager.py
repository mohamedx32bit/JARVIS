from core.hardware_monitor import HardwareMonitor
from core.gpu_monitor import GPUMonitor


class ResourceManager:
    """Central resource state for JARVIS."""

    def __init__(self, vram_safety_mb: int = 512, ram_safety_mb: int = 1024):
        self.system = HardwareMonitor()
        self.gpu = GPUMonitor()

        self.vram_safety_mb = vram_safety_mb
        self.ram_safety_mb = ram_safety_mb

    def snapshot(self) -> dict:
        system = self.system.snapshot()
        gpu = self.gpu.snapshot()

        usable_vram = max(
            0,
            gpu["vram_free_mb"] - self.vram_safety_mb
        )

        usable_ram = max(
            0,
            system["memory"]["available_mb"] - self.ram_safety_mb
        )

        return {
            "cpu": system["cpu"],
            "memory": {
                **system["memory"],
                "usable_mb": usable_ram,
            },
            "gpu": {
                **gpu,
                "usable_vram_mb": usable_vram,
            },
        }

    def close(self):
        self.gpu.close()


if __name__ == "__main__":
    manager = ResourceManager()

    try:
        state = manager.snapshot()

        print("JARVIS Resource Manager v0.1")
        print("============================")

        cpu = state["cpu"]
        memory = state["memory"]
        gpu = state["gpu"]

        print(
            f"CPU: {cpu['usage_percent']:.1f}% "
            f"({cpu['cores']}C/{cpu['threads']}T)"
        )

        print(
            f"RAM: {memory['used_mb']} / "
            f"{memory['total_mb']} MB | "
            f"Available: {memory['available_mb']} MB | "
            f"Usable: {memory['usable_mb']} MB"
        )

        print(
            f"VRAM: {gpu['vram_used_mb']} / "
            f"{gpu['vram_total_mb']} MB | "
            f"Free: {gpu['vram_free_mb']} MB | "
            f"Usable: {gpu['usable_vram_mb']} MB"
        )

        print(
            f"GPU: {gpu['gpu_utilization_percent']}% | "
            f"{gpu['temperature_c']}°C | "
            f"{gpu['power_usage_w']:.1f}W"
        )

    finally:
        manager.close()
