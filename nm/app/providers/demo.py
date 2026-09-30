from app.providers.base import LearningProvider
from app.schemas import QuizQuestion


class DemoProvider(LearningProvider):
    name = "demo"

    async def answer(self, question: str) -> str:
        lowered = question.lower()
        if "largest ocean" in lowered:
            return "The Pacific Ocean is the largest ocean on Earth."
        return f"Demo answer: {question} is a useful topic to explore. Add GEMINI_API_KEY for an AI-generated response."

    async def explain(self, topic: str) -> str:
        return (f"{topic.title()} is a concept that can be understood by breaking it into smaller ideas. "
                "Start with the definition, connect it to a familiar example, and then practice applying it.")

    async def summarize(self, text: str) -> str:
        sentences = [part.strip() for part in text.replace("!", ".").replace("?", ".").split(".") if part.strip()]
        if not sentences:
            return "No summary is available."
        return " ".join(sentences[:2]) + ("." if not sentences[0].endswith(".") else "")

    async def quiz(self, text: str) -> list[QuizQuestion]:
        topic = text.strip().split()[0].capitalize() if text.strip() else "the topic"
        return [
            QuizQuestion(question=f"What is a good first step when studying {topic}?", options=["Learn the definition", "Skip examples", "Avoid practice", "Memorize unrelated facts"], answer="Learn the definition"),
            QuizQuestion(question=f"Which approach helps make {topic} easier to understand?", options=["Break it into smaller ideas", "Use no examples", "Study without pauses", "Ignore questions"], answer="Break it into smaller ideas"),
            QuizQuestion(question=f"How can a learner build confidence with {topic}?", options=["Practice applying it", "Avoid feedback", "Only read the title", "Never review"], answer="Practice applying it"),
        ]

    async def recommend(self, topic: str) -> str:
        return (f"Learning path for {topic}\n\n"
                "1. Beginner: learn vocabulary and core concepts.\n"
                "2. Intermediate: work through guided examples and small exercises.\n"
                "3. Advanced: build a project, compare approaches, and teach the idea to someone else.\n\n"
                "Suggested rhythm: 30 minutes of study plus 20 minutes of practice, four days per week.")
