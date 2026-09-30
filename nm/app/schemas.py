from typing import Literal

from pydantic import BaseModel, Field


class TextRequest(BaseModel):
    text: str = Field(min_length=1, max_length=12000)


class TopicRequest(BaseModel):
    topic: str = Field(min_length=1, max_length=500)


class QuizQuestion(BaseModel):
    question: str
    options: list[str] = Field(min_length=2, max_length=6)
    answer: str


class QuizResponse(BaseModel):
    questions: list[QuizQuestion]
    source: Literal["gemini", "demo"]


class ContentResponse(BaseModel):
    content: str
    source: Literal["gemini", "demo"]
