from core.resource_manager import ResourceManager


class ResourceAnalyzer:
    """Interpret JARVIS resource state without taking actions."""

    def __init__(
        self,
        ram_warning_mb: int = 2048,
        ram_critical_mb: int = 1024,
        vram_warning_mb: int = 2048,
        vram_critical_mb: int = 1024,
        gpu_temp_warning_c: int = 80,
        gpu_temp_critical_c: int = 88,
    ):
        self.ram_warning_mb = ram_warning_mb
        self.ram_critical_mb = ram_critical_mb
        self.vram_warning_mb = vram_warning_mb
        self.vram_critical_mb = vram_critical_mb
        self.gpu_temp_warning_c = gpu_temp_warning_c
        self.gpu_temp_critical_c = gpu_temp_critical_c

    def analyze(self, state: dict) -> dict:
        memory = state["memory"]
        gpu = state["gpu"]
        cpu = state["cpu"]

        warnings = []
        critical = []

        # RAM
        if memory["available_mb"] <= self.ram_critical_mb:
            critical.append("RAM_CRITICAL")
        elif memory["available_mb"] <= self.ram_warning_mb:
            warnings.append("RAM_PRESSURE")

        # VRAM
        if gpu["vram_free_mb"] <= self.vram_critical_mb:
            critical.append("VRAM_CRITICAL")
        elif gpu["vram_free_mb"] <= self.vram_warning_mb:
            warnings.append("VRAM_PRESSURE")

        # GPU temperature
        if gpu["temperature_c"] >= self.gpu_temp_critical_c:
            critical.append("GPU_TEMPERATURE_CRITICAL")
        elif gpu["temperature_c"] >= self.gpu_temp_warning_c:
            warnings.append("GPU_TEMPERATURE_HIGH")

        if critical:
            status = "CRITICAL"
        elif warnings:
            status = "CONSTRAINED"
        else:
            status = "NORMAL"

        recommendations = []

        if "RAM_CRITICAL" in critical:
            recommendations.append("Avoid large RAM allocations.")

        elif "RAM_PRESSURE" in warnings:
            recommendations.append("Prefer memory-efficient workloads.")

        if "VRAM_CRITICAL" in critical:
            recommendations.append("Avoid loading large GPU workloads.")

        elif "VRAM_PRESSURE" in warnings:
            recommendations.append("Preserve VRAM headroom.")

        if "GPU_TEMPERATURE_HIGH" in warnings:
            recommendations.append("Monitor GPU temperature.")

        if "GPU_TEMPERATURE_CRITICAL" in critical:
            recommendations.append("Reduce GPU workload immediately.")

        if not recommendations:
            recommendations.append("Resources are within normal operating range.")

        return {
            "status": status,
            "warnings": warnings,
            "critical": critical,
            "recommendations": recommendations,
            "cpu_usage_percent": cpu["usage_percent"],
            "ram_available_mb": memory["available_mb"],
            "ram_usable_mb": memory["usable_mb"],
            "vram_free_mb": gpu["vram_free_mb"],
            "vram_usable_mb": gpu["usable_vram_mb"],
            "gpu_temperature_c": gpu["temperature_c"],
        }


if __name__ == "__main__":
    manager = ResourceManager()
    analyzer = ResourceAnalyzer()

    try:
        state = manager.snapshot()
        analysis = analyzer.analyze(state)

        print("JARVIS Resource Analyzer v0.1")
        print("==============================")
        print(f"STATUS: {analysis['status']}")

        print("\nWarnings:")
        if analysis["warnings"]:
            for item in analysis["warnings"]:
                print(f"  - {item}")
        else:
            print("  None")

        print("\nCritical:")
        if analysis["critical"]:
            for item in analysis["critical"]:
                print(f"  - {item}")
        else:
            print("  None")

        print("\nRecommendations:")
        for item in analysis["recommendations"]:
            print(f"  - {item}")

        print("\nLive Resources:")
        print(f"  CPU: {analysis['cpu_usage_percent']:.1f}%")
        print(f"  RAM Available: {analysis['ram_available_mb']} MB")
        print(f"  RAM Usable: {analysis['ram_usable_mb']} MB")
        print(f"  VRAM Free: {analysis['vram_free_mb']} MB")
        print(f"  VRAM Usable: {analysis['vram_usable_mb']} MB")
        print(f"  GPU Temperature: {analysis['gpu_temperature_c']}°C")

    finally:
        manager.close()
