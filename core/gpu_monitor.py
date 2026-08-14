import pynvml


class GPUMonitor:
    """Read-only NVIDIA GPU telemetry for JARVIS."""

    def __init__(self, index: int = 0):
        pynvml.nvmlInit()
        self.handle = pynvml.nvmlDeviceGetHandleByIndex(index)

    def snapshot(self) -> dict:
        memory = pynvml.nvmlDeviceGetMemoryInfo(self.handle)

        return {
            "name": pynvml.nvmlDeviceGetName(self.handle),
            "vram_total_mb": memory.total // (1024 ** 2),
            "vram_used_mb": memory.used // (1024 ** 2),
            "vram_free_mb": memory.free // (1024 ** 2),
            "gpu_utilization_percent":
                pynvml.nvmlDeviceGetUtilizationRates(self.handle).gpu,
            "temperature_c":
                pynvml.nvmlDeviceGetTemperature(
                    self.handle,
                    pynvml.NVML_TEMPERATURE_GPU
                ),
            "power_usage_w":
                pynvml.nvmlDeviceGetPowerUsage(self.handle) / 1000,
            "power_limit_w":
                pynvml.nvmlDeviceGetPowerManagementLimit(self.handle) / 1000,
        }

    def close(self):
        pynvml.nvmlShutdown()


if __name__ == "__main__":
    monitor = GPUMonitor()

    try:
        data = monitor.snapshot()

        print("JARVIS GPU Monitor")
        print("==================")
        print(f"GPU: {data['name']}")
        print(
            f"VRAM: {data['vram_used_mb']} / "
            f"{data['vram_total_mb']} MB "
            f"(Free: {data['vram_free_mb']} MB)"
        )
        print(f"GPU Utilization: {data['gpu_utilization_percent']}%")
        print(f"Temperature: {data['temperature_c']}°C")
        print(
            f"Power: {data['power_usage_w']:.1f} / "
            f"{data['power_limit_w']:.1f} W"
        )

    finally:
        monitor.close()
