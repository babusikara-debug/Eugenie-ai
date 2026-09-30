from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import get_settings
from app.providers.factory import create_provider
from app.schemas import ContentResponse, QuizResponse, TextRequest, TopicRequest

BASE_DIR = Path(__file__).resolve().parent
settings = get_settings()
provider = create_provider(settings)

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app = FastAPI(title=settings.app_name, version="1.0.0", description="AI-powered learning assistant")
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


def clean(value: str) -> str:
    return value.strip()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="index.html", context={"app_name": settings.app_name})


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "provider": provider.name}


@app.post("/api/qa", response_model=ContentResponse)
async def answer_question(payload: TextRequest) -> ContentResponse:
    return ContentResponse(content=await provider.answer(clean(payload.text)), source=provider.name)


@app.post("/api/explain", response_model=ContentResponse)
async def explain_topic(payload: TopicRequest) -> ContentResponse:
    return ContentResponse(content=await provider.explain(clean(payload.topic)), source=provider.name)


@app.post("/api/summarize", response_model=ContentResponse)
async def summarize_text(payload: TextRequest) -> ContentResponse:
    return ContentResponse(content=await provider.summarize(clean(payload.text)), source=provider.name)


@app.post("/api/quiz", response_model=QuizResponse)
async def generate_quiz(payload: TextRequest) -> QuizResponse:
    return QuizResponse(questions=await provider.quiz(clean(payload.text)), source=provider.name)


@app.post("/api/recommendations", response_model=ContentResponse)
async def learning_recommendations(payload: TopicRequest) -> ContentResponse:
    return ContentResponse(content=await provider.recommend(clean(payload.topic)), source=provider.name)
