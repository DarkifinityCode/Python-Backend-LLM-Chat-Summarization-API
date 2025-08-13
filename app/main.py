from fastapi import FastAPI
from app.routes import chats, users, summarize
from app.database import db

app = FastAPI(
    title="Chat Summarization and Insights API",
    description="A backend API for storing, retrieving, and summarizing chats with LLM integration.",
    version="1.0.0"
)

# Include routers
app.include_router(chats.router, prefix="/chats", tags=["Chats"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(summarize.router, prefix="/summarize", tags=["Summarization"])

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to the Chat Summarization and Insights API"}

@app.get("/health", tags=["Health"])
async def health():
    """
    Health check endpoint that verifies API is up and checks database connectivity.
    Returns "ok" if everything is fine, "degraded" if DB is not reachable.
    """
    db_ok = True
    try:
        await db.command("ping")  # MongoDB ping command
    except Exception:
        db_ok = False
    return {
        "status": "ok" if db_ok else "degraded",
        "database": "up" if db_ok else "down"
    }
