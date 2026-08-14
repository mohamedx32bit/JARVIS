import json
from pathlib import Path


class HardwareProfile:
    def __init__(self, path: str = "config/hardware.json"):
        self.path = Path(path)
        self.data = self._load()

    def _load(self) -> dict:
        if not self.path.exists():
            raise FileNotFoundError(
                f"Hardware profile not found: {self.path}"
            )

        with self.path.open("r", encoding="utf-8-sig") as file:
            return json.load(file)

    @property
    def gpu(self) -> dict:
        return self.data["gpu"]

    @property
    def cpu(self) -> dict:
        return self.data["cpu"]

    @property
    def ram_mb(self) -> int:
        return self.data["ram_mb"]

    def summary(self) -> str:
        return (
            f"GPU: {self.gpu['name']} | "
            f"VRAM: {self.gpu['vram_mb']} MB | "
            f"CPU: {self.cpu['name']} "
            f"({self.cpu['cores']}C/{self.cpu['threads']}T) | "
            f"RAM: {self.ram_mb} MB"
        )


if __name__ == "__main__":
    hardware = HardwareProfile()
    print("JARVIS Hardware Profile")
    print("------------------------")
    print(hardware.summary())
