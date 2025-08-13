from fastapi import FastAPI
import asyncio

# Import local modules directly (flat structure)
import chats
import users
import summarize
import insights  # Bonus feature: insights routes
import realtime  # Bonus feature: realtime WebSocket routes

from database import db

# Create FastAPI app
app = FastAPI(
    title="Chat Summarization and Insights API",
    description="Store, retrieve, and summarize chat conversations with optional LLM integration.",
    version="1.0.0",
)

# Routers
app.include_router(chats.router, prefix="/chats", tags=["Chats"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(summarize.router, prefix="/summarize", tags=["Summarization"])
app.include_router(insights.router, prefix="/insights", tags=["Insights"])
app.include_router(realtime.router, tags=["Realtime"])

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

# Allow running directly without uvicorn CLI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
