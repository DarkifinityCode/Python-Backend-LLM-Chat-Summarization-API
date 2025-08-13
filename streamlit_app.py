import os
import requests
import streamlit as st

API_BASE = os.getenv("API_BASE", "http://127.0.0.1:8000")

st.set_page_config(page_title="Chat Summarization Demo", page_icon="💬", layout="centered")
st.title("💬 Chat Summarization & Insights")

with st.sidebar:
    st.markdown("### Settings")
    user_id = st.text_input("User ID", value="u1")
    conversation_id = st.text_input("Conversation ID", value=f"{user_id}_conv")

st.subheader("1) Add Messages")
with st.form("add_msgs"):
    new_text = st.text_area("Message (from user)", height=80, placeholder="Type a message")
    submitted = st.form_submit_button("Send")
    if submitted and new_text.strip():
        payload = {
            "user_id": user_id,
            "conversation_id": conversation_id,
            "messages": [{"sender_id": user_id, "message": new_text.strip()}],
        }
        r = requests.post(f"{API_BASE}/chats", json=payload)
        if r.ok:
            st.success(f"Message saved to {conversation_id}")
        else:
            st.error(f"Error: {r.text}")

st.subheader("2) View Conversation")
if st.button("Refresh Conversation"):
    r = requests.get(f"{API_BASE}/chats/{conversation_id}")
    if r.ok:
        chat = r.json()
        for m in chat.get("messages", []):
            st.write(f"**{m.get('sender_id')}**: {m.get('message')}")
    else:
        st.error(f"Error: {r.text}")

st.subheader("3) Summarize")
if st.button("Summarize Conversation"):
    r = requests.post(f"{API_BASE}/summarize", json={"conversation_id": conversation_id})
    if r.ok:
        data = r.json()
        st.write("**Summary:**", data.get("summary"))
        st.write("**Keywords:**", ", ".join(data.get("keywords", [])))
        st.write("**Sentiment:**", data.get("sentiment"))
    else:
        st.error(f"Error: {r.text}")

st.subheader("4) Insights")
if st.button("Get Insights"):
    r = requests.get(f"{API_BASE}/insights/{conversation_id}")
    if r.ok:
        d = r.json()
        st.json(d)
    else:
        st.error(f"Error: {r.text}")
