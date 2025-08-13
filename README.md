# Chat Summarization and Insights API 💬 + Brownie Points 🍫

A **FastAPI** backend with real-time chat updates, AI-powered summarization, keyword extraction, sentiment analysis, and a **Streamlit UI** for quick demos.  
Built for **Simplify Money** internship assignment — with all *three brownie points* completed.

---

## ✨ Features
- **Store and retrieve chats**
- **AI-powered summaries** via `summarizer.py`
- **Keyword extraction** & **sentiment analysis**
- **Real-time updates** with WebSockets
- **Simple Streamlit UI** to interact with the API
- Modular, async-ready codebase

---

## 🏆 Brownie Points Completed
1. **Extra Problem**:  
   - Implemented `/insights` and real-time WebSocket updates for AI summaries, keywords, and sentiment.
2. **Simple Realtime Feature**:  
   - Fully functional `/ws/{conversation_id}` endpoint broadcasting live updates to all connected clients.
3. **Simple Streamlit UI**:  
   - `ui.py` lets you interact with the API without Postman or Swagger.

---

## 🛠 Tech Stack
- **FastAPI** – API framework
- **MongoDB** – Chat storage
- **OpenAI API** – Summarization & insights (mock/replaceable)
- **Uvicorn** – ASGI server
- **Streamlit** – Simple front-end UI

---

## 📦 Installation

### 1️⃣ Clone the repo
```bash
git clone https://github.com/your-username/Python-Backend-LLM-Chat-Summarization-API.git
cd Python-Backend-LLM-Chat-Summarization-API
```

### 2️⃣ Create & activate a virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure environment variables
Create a `.env` file in the project root:
```env
DATABASE_URL=mongodb://localhost:27017/chatdb
OPENAI_API_KEY=your_openai_api_key
```

---

## 🚀 Running the Backend

### **Method 1 – Python**
```bash
python main.py
```

### **Method 2 – Uvicorn CLI**
```bash
uvicorn main:app --reload
```

**Backend runs at:**  
[http://127.0.0.1:8000](http://127.0.0.1:8000)  

Swagger docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
(*Note: WebSockets `/ws` are not visible in Swagger.*)

---

## 💬 Real-time WebSocket

### Connect Example (Browser Console):
```javascript
let ws = new WebSocket("ws://127.0.0.1:8000/ws/demo_conv");
ws.onmessage = e => console.log("Message:", e.data);
ws.onopen = () => ws.send(JSON.stringify({
    "user_id": "u1",
    "sender_id": "u1",
    "message": "Hello"
}));
```

Open **two browser tabs**, run this code in both, and watch the magic.

---

## 🖥 Running the Streamlit UI
With backend running, open another terminal:
```bash
venv\Scripts\activate
streamlit run ui.py
```

Visit:  
[http://localhost:8501](http://localhost:8501)  

Features:
- Send messages to any conversation ID
- Get live summaries, keywords, and sentiment
- Simple interface for demos

---

## 📸 Demo Flow for Submission
1. **Backend running** in terminal
2. **Swagger screenshot** showing endpoints
3. **Browser console** showing WebSocket live updates
4. **Streamlit UI** sending a message and fetching summary
5. **Two tabs WebSocket test** for real-time effect

---

## 📄 License
MIT License – free to use and modify.
