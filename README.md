# Chat Summarization and Insights API

A FastAPI-based backend service for storing, retrieving, and summarizing chat conversations using optional LLM integration.  
This version uses a **flat project structure** for simplicity and ease of running.

---

## Features
- Store and retrieve chats
- AI-powered summarization via OpenAI API (optional)
- Pagination and filtering for heavy chat loads
- Delete chats
- Modular, clean code with async MongoDB queries
- Health check endpoint

---

## Tech Stack
- **FastAPI** for the API framework
- **MongoDB** (local or cloud)
- **OpenAI API** (optional) for summarization
- **Uvicorn** for the ASGI server

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2. Create a virtual environment
```bash
python -m venv venv
# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the project root based on `.env.example`:

```env
DATABASE_URL=mongodb://localhost:27017/chatdb
OPENAI_API_KEY=your_openai_api_key_here
```

> `OPENAI_API_KEY` is optional. If not set, the app will use a simple local summarizer.

---

## Running the App

From the project root (same folder as `main.py`):

```bash
python -m uvicorn main:app --reload
```

The API will be available at:  
[http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## API Endpoints

### Health Check
```
GET /health
```
Returns API and database status.

### Create or Append to a Chat
```
POST /chats
```
Body:
```json
{
  "user_id": "u1",
  "messages": [
    {"sender_id": "u1", "message": "hello"},
    {"sender_id": "bot", "message": "hi there!"}
  ]
}
```

### Get a Chat by Conversation ID
```
GET /chats/{conversation_id}
```

### Summarize a Chat
```
POST /summarize
```
Body:
```json
{"conversation_id": "u1_conv"}
```

### List User Chats (Paginated)
```
GET /users/{user_id}/chats?page=1&limit=10
```

### Delete a Chat
```
DELETE /chats/{conversation_id}
```

---

## Deployment

You can deploy on:
- **Render**, **Railway**, **Fly.io**, or any cloud hosting platform
- Or run locally with Docker (optional)

Docker example:
```bash
docker build -t chat-api .
docker run -p 8000:8000 chat-api
```

---

## License
This project is open source and available under the MIT License.
