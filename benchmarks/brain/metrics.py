from dataclasses import dataclass, asdict
from typing import Optional
import json
from pathlib import Path


@dataclass
class PerformanceMetrics:
    load_time_seconds: Optional[float] = None
    prompt_tokens: Optional[int] = None
    generated_tokens: Optional[int] = None
    generation_time_seconds: Optional[float] = None
    tokens_per_second: Optional[float] = None

    ram_before_mb: Optional[float] = None
    ram_peak_mb: Optional[float] = None
    vram_before_mb: Optional[float] = None
    vram_peak_mb: Optional[float] = None

    @property
    def ram_delta_mb(self):
        if self.ram_before_mb is None or self.ram_peak_mb is None:
            return None
        return self.ram_peak_mb - self.ram_before_mb

    @property
    def vram_delta_mb(self):
        if self.vram_before_mb is None or self.vram_peak_mb is None:
            return None
        return self.vram_peak_mb - self.vram_before_mb

    def to_dict(self):
        data = asdict(self)
        data["ram_delta_mb"] = self.ram_delta_mb
        data["vram_delta_mb"] = self.vram_delta_mb
        return data


@dataclass
class CapabilityScore:
    reasoning: float = 0.0
    coding: float = 0.0
    planning: float = 0.0
    tool_use: float = 0.0
    conversation: float = 0.0
    reliability: float = 0.0

    def weighted_score(self):
        return (
            self.reasoning * 0.25
            + self.coding * 0.20
            + self.planning * 0.15
            + self.tool_use * 0.15
            + self.conversation * 0.10
            + self.reliability * 0.10
        )

    def to_dict(self):
        data = asdict(self)
        data["weighted_score"] = self.weighted_score()
        return data


def save_json(path: str | Path, data: dict):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)