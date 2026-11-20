from abc import ABC, abstractmethod

from .types import GenerationRequest, GenerationResult


class BrainAdapter(ABC):
    """
    Universal interface between JARVIS and an AI model.

    The rest of JARVIS must never depend directly on
    Qwen, Phi, llama.cpp, Transformers, etc.
    """

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.loaded = False

    @abstractmethod
    def load(self) -> None:
        """Load the model into memory."""
        raise NotImplementedError

    @abstractmethod
    def unload(self) -> None:
        """Unload the model and release resources."""
        raise NotImplementedError

    @abstractmethod
    def generate(
        self,
        request: GenerationRequest,
    ) -> GenerationResult:
        """Generate a response from the model."""
        raise NotImplementedError

    def health(self) -> dict:
        return {
            "model": self.model_name,
            "loaded": self.loaded,
        }