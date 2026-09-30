import json
import re

from google import genai

from app.providers.base import LearningProvider
from app.schemas import QuizQuestion


class GeminiProvider(LearningProvider):
    name = "gemini"

    def __init__(self, api_key: str, model: str) -> None:
        self.client = genai.Client(api_key=api_key)
        self.model = model

    async def _generate(self, prompt: str) -> str:
        response = await self.client.aio.models.generate_content(model=self.model, contents=prompt)
        text = getattr(response, "text", None)
        if not text:
            raise RuntimeError("Gemini returned an empty response")
        return text.strip()

    async def answer(self, question: str) -> str:
        return await self._generate(f"Answer this learner question clearly and accurately in under 150 words:\n{question}")

    async def explain(self, topic: str) -> str:
        return await self._generate(f"Explain {topic} to a beginner using simple language, one analogy, and three key points.")

    async def summarize(self, text: str) -> str:
        return await self._generate(f"Summarize the following passage in simple language. Preserve the main facts:\n{text}")

    async def quiz(self, text: str) -> list[QuizQuestion]:
        prompt = ("Create exactly three multiple-choice questions from this text. "
                  "Return only a JSON array. Each object must contain question, options (exactly four strings), and answer "
                  "where answer exactly matches one option.\n\n" + text)
        raw = await self._generate(prompt)
        cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip(), flags=re.IGNORECASE | re.DOTALL)
        data = json.loads(cleaned)
        return [QuizQuestion.model_validate(item) for item in data[:3]]

    async def recommend(self, topic: str) -> str:
        return await self._generate(f"Create a structured learning path for {topic} from beginner to advanced. Include order, estimated time, practice tasks, and resources.")
