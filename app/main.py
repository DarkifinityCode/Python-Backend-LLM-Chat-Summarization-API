from fastapi import FastAPI
from app.routes import chats, users, summarize

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
