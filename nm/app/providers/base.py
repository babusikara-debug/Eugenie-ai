from abc import ABC, abstractmethod

from app.schemas import QuizQuestion


class LearningProvider(ABC):
    name: str

    @abstractmethod
    async def answer(self, question: str) -> str:
        raise NotImplementedError

    @abstractmethod
    async def explain(self, topic: str) -> str:
        raise NotImplementedError

    @abstractmethod
    async def summarize(self, text: str) -> str:
        raise NotImplementedError

    @abstractmethod
    async def quiz(self, text: str) -> list[QuizQuestion]:
        raise NotImplementedError

    @abstractmethod
    async def recommend(self, topic: str) -> str:
        raise NotImplementedError
