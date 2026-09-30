# EduGenie

EduGenie is a lightweight AI learning assistant built with FastAPI and a responsive HTML/CSS/JavaScript frontend. It supports question answering, beginner-friendly explanations, summaries, quiz generation, and personalized learning paths.

## Features

- Gemini-powered responses through the official `google-genai` SDK.
- Safe demo mode when `GEMINI_API_KEY` is not configured.
- Three-question quizzes with four options and immediate answer feedback.
- Typed Pydantic request and response models.
- Simple, dependency-light project structure suitable for macOS, Windows, and Linux.

## VS Code setup

1. Open the `/Users/sikara/Documents/nm` folder in VS Code.
2. Create a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   On Windows, activate with `.venv\\Scripts\\activate`.

3. Install dependencies:

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Optional: copy `.env.example` to `.env` and set `GEMINI_API_KEY`. Without a key, the app uses deterministic demo responses so the full interface remains testable.

## Run

Start the development server from the project root:

```bash
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000` in a browser. The API documentation is available at `http://127.0.0.1:8000/docs`.

You can also use the VS Code Run and Debug panel with the `EduGenie API` configuration in `.vscode/launch.json`.

## Test

Run the automated tests from the project root:

```bash
python -m pytest
```

The tests validate health checks, request validation, demo Q&A behavior, and quiz shape.

## API endpoints

- `POST /api/qa` with `{ "text": "..." }`
- `POST /api/explain` with `{ "topic": "..." }`
- `POST /api/summarize` with `{ "text": "..." }`
- `POST /api/quiz` with `{ "text": "..." }`
- `POST /api/recommendations` with `{ "topic": "..." }`
- `GET /health`
