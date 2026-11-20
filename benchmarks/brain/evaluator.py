from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .benchmark import BenchmarkCase, get_cases
from .metrics import CapabilityScore, PerformanceMetrics, save_json


@dataclass
class CaseResult:
    case_id: str
    category: str
    response: str = ""
    score: float | None = None
    notes: str = ""
    performance: PerformanceMetrics = field(
        default_factory=PerformanceMetrics
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "category": self.category,
            "response": self.response,
            "score": self.score,
            "notes": self.notes,
            "performance": self.performance.to_dict(),
        }


class BrainEvaluator:
    """
    Model-agnostic evaluator.

    The evaluator does not know which LLM is being tested.
    A future BrainAdapter will provide the model response.
    """

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.results: list[CaseResult] = []

    def add_result(
        self,
        case: BenchmarkCase,
        response: str,
        score: float | None = None,
        notes: str = "",
        performance: PerformanceMetrics | None = None,
    ):
        self.results.append(
            CaseResult(
                case_id=case.id,
                category=case.category,
                response=response,
                score=score,
                notes=notes,
                performance=performance or PerformanceMetrics(),
            )
        )

    def capability_score(self) -> CapabilityScore:
        grouped: dict[str, list[float]] = {}

        for result in self.results:
            if result.score is None:
                continue

            grouped.setdefault(result.category, []).append(result.score)

        def average(category: str) -> float:
            values = grouped.get(category, [])
            if not values:
                return 0.0
            return sum(values) / len(values)

        return CapabilityScore(
            reasoning=average("reasoning"),
            coding=average("coding"),
            planning=average("planning"),
            tool_use=average("tool_use"),
            conversation=average("conversation"),
            reliability=average("reliability"),
        )

    def summary(self) -> dict[str, Any]:
        capability = self.capability_score()

        return {
            "model": self.model_name,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "cases_evaluated": len(self.results),
            "capability": capability.to_dict(),
            "results": [
                result.to_dict()
                for result in self.results
            ],
        }

    def save(self, output_path: str | Path):
        save_json(output_path, self.summary())


if __name__ == "__main__":
    print("JARVIS Brain Evaluator v0.1")
    print("===========================")

    cases = get_cases()

    evaluator = BrainEvaluator(
        model_name="UNSELECTED"
    )

    print(f"Model: {evaluator.model_name}")
    print(f"Benchmark cases: {len(cases)}")
    print()
    print("Evaluator ready.")
    print("No model loaded.")