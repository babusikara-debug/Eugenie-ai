from app.config import Settings
from app.providers.base import LearningProvider
from app.providers.demo import DemoProvider
from app.providers.gemini import GeminiProvider


def create_provider(settings: Settings) -> LearningProvider:
    if settings.gemini_api_key:
        return GeminiProvider(settings.gemini_api_key, settings.gemini_model)
    return DemoProvider()
