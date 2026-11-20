from dataclasses import dataclass
from typing import Literal


Category = Literal[
    "reasoning",
    "coding",
    "planning",
    "tool_use",
    "conversation",
    "reliability",
]


@dataclass(frozen=True)
class BenchmarkCase:
    id: str
    category: Category
    prompt: str
    description: str
    max_score: float = 10.0


BENCHMARK_CASES = [
    BenchmarkCase(
        id="reasoning_001",
        category="reasoning",
        description="Resource-constrained decision making",
        prompt=(
            "You are running on a computer with limited RAM and VRAM. "
            "You need to complete a large computational task without "
            "exhausting system resources. Explain a safe strategy and "
            "the decisions you would make before starting the task."
        ),
    ),

    BenchmarkCase(
        id="coding_001",
        category="coding",
        description="Design a resource monitoring component",
        prompt=(
            "Design a Python module that monitors CPU, RAM, GPU and VRAM "
            "usage and returns a structured JSON status. Explain the "
            "architecture and important edge cases before writing code."
        ),
    ),

    BenchmarkCase(
        id="planning_001",
        category="planning",
        description="Multi-step project planning",
        prompt=(
            "You are given a large software project that must be built "
            "incrementally. Create a practical development plan that "
            "starts with a minimal working core and gradually adds "
            "capabilities while keeping the system testable."
        ),
    ),

    BenchmarkCase(
        id="tool_use_001",
        category="tool_use",
        description="Tool selection",
        prompt=(
            "A user tells you: 'Check whether the computer has enough "
            "free memory before starting a heavy task.' "
            "Explain which tool or system information you would need, "
            "what you would check, and what you would do with the result."
        ),
    ),

    BenchmarkCase(
        id="conversation_001",
        category="conversation",
        description="Natural assistant interaction",
        prompt=(
            "The user is working on a long-running personal project and "
            "suddenly encounters an unexpected technical problem. "
            "Respond naturally as a persistent personal AI assistant: "
            "understand the situation, ask only necessary questions, "
            "and propose the next useful action."
        ),
    ),

    BenchmarkCase(
        id="reliability_001",
        category="reliability",
        description="Handling uncertainty",
        prompt=(
            "You do not have enough information to determine the exact "
            "cause of a technical failure. Explain how you would respond "
            "without inventing facts, and describe what evidence you "
            "would collect next."
        ),
    ),
]


def get_cases(category: Category | None = None) -> list[BenchmarkCase]:
    if category is None:
        return BENCHMARK_CASES

    return [
        case
        for case in BENCHMARK_CASES
        if case.category == category
    ]


def get_case(case_id: str) -> BenchmarkCase:
    for case in BENCHMARK_CASES:
        if case.id == case_id:
            return case

    raise KeyError(f"Unknown benchmark case: {case_id}")


if __name__ == "__main__":
    print("JARVIS Brain Benchmark v0.1")
    print("==========================")
    print(f"Cases: {len(BENCHMARK_CASES)}")

    for case in BENCHMARK_CASES:
        print(
            f"[{case.category.upper():13}] "
            f"{case.id}: {case.description}"
        )
        