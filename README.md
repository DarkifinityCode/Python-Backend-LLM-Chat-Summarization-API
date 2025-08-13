# Chat Summarization and Insights API

A FastAPI-based backend service for storing, retrieving, and summarizing chat conversations using LLM integration. Designed for scalability with support for real-time ingestion, pagination, and filtering.

---

## Features
- Store and retrieve chats
- AI-powered summarization via LLM API
- Pagination and filtering for heavy chat loads
- Delete chats
- Modular, clean code with async DB queries

---

## Tech Stack
- **FastAPI** for the API framework
- **MongoDB / PostgreSQL / MySQL** (choose one)
- **OpenAI API** (or any LLM API) for summarization
- **Uvicorn** for ASGI server

---

## Project Structure
```
your-repo/
├── README.md
├── requirements.txt
├── .env.example
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── crud.py
│   ├── routes/
│   │   ├── chats.py
│   │   ├── users.py
│   │   └── summarize.py
│   └── utils/
│       ├── summarizer.py
│       └── filters.py
```

---

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

2. **Create a virtual environment**
```bash
python -m venv venv
# Activate virtual environment
# Linux / MacOS
source venv/bin/activate
# Windows
venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set environment variables**
Copy `.env.example` to `.env` and fill in your credentials:
```env
DATABASE_URL=mongodb://localhost:27017/chatdb
OPENAI_API_KEY=your_openai_api_key
```

---

## Running the App
```bash
uvicorn app.main:app --reload
```
The API will be available at:
```
http://127.0.0.1:8000
```

---

## API Endpoints
- **POST** `/chats` → Store chat messages
- **GET** `/chats/{conversation_id}` → Retrieve chat by conversation ID
- **POST** `/chats/summarize` → Summarize conversation
- **GET** `/users/{user_id}/chats` → Paginated chat history
- **DELETE** `/chats/{conversation_id}` → Delete conversation

Swagger documentation will be available at:
```
http://127.0.0.1:8000/docs
```

---

## Deployment
- Deploy on **Render**, **Railway**, or **Fly.io**
- Or use Docker for containerized deployment

---

## Development Tips
- Add `.gitignore` to exclude unnecessary files:
```
venv/
__pycache__/
.env
```
- Use `.env.example` for sharing configuration requirements without exposing secrets.
- Consider adding a `/health` endpoint for quick service checks.

---

## License
MIT License
