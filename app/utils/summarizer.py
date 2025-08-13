import os
from dotenv import load_dotenv
from typing import List, Tuple
import openai

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_chat(messages: List[dict]) -> Tuple[str, List[str], str]:
    """
    Summarizes a list of chat messages and extracts keywords and sentiment.
    Returns: (summary, keywords, sentiment)
    """

    # Combine all messages into a single text block
    conversation_text = "\n".join(
        [f"{msg['sender_id']}: {msg['message']}" for msg in messages]
    )

    prompt = f"""
    Summarize the following conversation in 4-5 sentences.
    Then list 5 important keywords.
    Then determine the overall sentiment (Positive, Negative, Neutral).

    Conversation:
    {conversation_text}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Change to your preferred LLM
            messages=[
                {"role": "system", "content": "You are an assistant that summarizes chat conversations."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )

        result_text = response["choices"][0]["message"]["content"]

        # Simple parsing
        parts = result_text.split("\n")
        summary = ""
        keywords = []
        sentiment = "Neutral"

        for part in parts:
            lower_part = part.lower()
            if "keyword" in lower_part:
                keywords = [kw.strip(" ,") for kw in part.split(":")[-1].split(",")]
            elif "positive" in lower_part or "negative" in lower_part or "neutral" in lower_part:
                sentiment = part.split(":")[-1].strip()
            else:
                summary += part + " "

        return summary.strip(), keywords, sentiment

    except Exception as e:
        return f"Error generating summary: {str(e)}", [], "Unknown"
