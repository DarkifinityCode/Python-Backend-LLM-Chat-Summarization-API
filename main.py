from fastapi import FastAPI
import asyncio

import chats
import users
import summarize
from database import db

app = FastAPI(
    title="Chat Summarization and Insights API",
    description="Store, retrieve, and summarize chat conversations with optional LLM integration.",
    version="1.0.0",
)

# Routers
app.include_router(chats.router, prefix="/chats", tags=["Chats"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(summarize.router, prefix="/summarize", tags=["Summarization"])

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to the Chat Summarization and Insights API"}

@app.get("/health", tags=["Health"])
async def health():
    """
    Health check for API and database connectivity.
    Returns "ok" if DB ping works, "degraded" otherwise.
    """
    try:
        await db.command("ping")
        return {"status": "ok", "database": "up"}
    except Exception:
        return {"status": "degraded", "database": "down"}
