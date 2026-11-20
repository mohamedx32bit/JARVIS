from dataclasses import dataclass, field
from typing import Any


@dataclass
class GenerationRequest:
    prompt: str
    system_prompt: str | None = None
    max_tokens: int = 512
    temperature: float = 0.7
    top_p: float = 0.9
    stop: list[str] = field(default_factory=list)


@dataclass
class GenerationResult:
    text: str
    prompt_tokens: int | None = None
    generated_tokens: int | None = None
    generation_time_seconds: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)