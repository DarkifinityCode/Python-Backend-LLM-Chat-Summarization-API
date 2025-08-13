import os
from typing import List, Tuple
from dotenv import load_dotenv

# Optional OpenAI usage with safe fallback
try:
    import openai  # legacy client import still widely used
except Exception:
    openai = None  # allow fallback without crashing

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def _fallback_summarize(messages: List[dict]) -> Tuple[str, List[str], str]:
    """Heuristic fallback so the API works even without OpenAI."""
    text = " ".join(m.get("message", "") for m in messages)
    words = [w.strip(".,!?()[]{}\"'").lower() for w in text.split()]
    # crude keyword pick: top 5 unique words > 3 chars
    freq = {}
    for w in words:
        if len(w) <= 3:
            continue
        freq[w] = freq.get(w, 0) + 1
    keywords = [w for w, _ in sorted(freq.items(), key=lambda x: (-x[1], x[0]))[:5]]

    # crude sentiment guess
    pos = {"good", "great", "love", "nice", "happy", "thanks"}
    neg = {"bad", "hate", "angry", "sad", "issue", "problem"}
    score = sum(1 for w in words if w in pos) - sum(1 for w in words if w in neg)
    sentiment = "Positive" if score > 0 else "Negative" if score < 0 else "Neutral"

    # naive summary (first 2-3 user lines)
    lines = [f"{m.get('sender_id')}: {m.get('message')}" for m in messages]
    summary = " | ".join(lines[:3])
    if len(lines) > 3:
        summary += " | …"
    return summary or "No content to summarize.", keywords, sentiment

def summarize_chat(messages: List[dict]) -> Tuple[str, List[str], str]:
    """
    Summarize chat messages and extract keywords & sentiment.
    Returns: (summary, keywords, sentiment)
    Uses OpenAI if OPENAI_API_KEY is set; otherwise uses a local heuristic.
    """
    if not (OPENAI_API_KEY and openai):
        return _fallback_summarize(messages)

    try:
        openai.api_key = OPENAI_API_KEY
        conversation = "\n".join(f"{m.get('sender_id')}: {m.get('message')}" for m in messages)

        prompt = (
            "Summarize the following conversation in 3-5 concise sentences. "
            "Then list 5 important keywords (comma-separated). "
            "Finally, classify overall sentiment as Positive, Negative, or Neutral.\n\n"
            f"Conversation:\n{conversation}"
        )

        # Compatible with classic ChatCompletion API; if your openai==1.x you may need the new client.
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that summarizes chat conversations."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )
        content = resp["choices"][0]["message"]["content"]

        # Parse very loosely
        lines = [ln.strip() for ln in content.split("\n") if ln.strip()]
        summary_lines = []
        keywords = []
        sentiment = "Neutral"

        for ln in lines:
            low = ln.lower()
            if low.startswith("keyword") or "keywords:" in low:
                tail = ln.split(":", 1)[-1]
                keywords = [k.strip(" ,.-") for k in tail.split(",") if k.strip()]
            elif "sentiment" in low:
                sentiment = ln.split(":", 1)[-1].strip().capitalize()
            else:
                summary_lines.append(ln)

        summary = " ".join(summary_lines).strip()
        if not summary:
            summary = content.strip()

        return summary, (keywords[:5] if keywords else []), (sentiment or "Neutral")

    except Exception:
        # If OpenAI fails, use local fallback
        return _fallback_summarize(messages)
