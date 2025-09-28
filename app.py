import streamlit as st
import requests
import openai
import os

# -------------------------------
# Config
# -------------------------------
API_BASE = "https://orion-memory.onrender.com"
USER_ID = "1"

st.set_page_config(
    page_title="Orion Memory Demo",
    page_icon="🛰️",
    layout="wide"
)

# Load OpenAI API key (from Streamlit secrets or environment variable)
openai.api_key = os.getenv("OPENAI_API_KEY", st.secrets.get("OPENAI_API_KEY", None))

if not openai.api_key:
    st.warning("⚠️ OpenAI API key not found. Please set it in Streamlit secrets.")

# -------------------------------
# Session State
# -------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------------------
# UI
# -------------------------------
st.title("🛰️ Orion Memory Demo")
st.markdown("""
Welcome to the live demo of **Orion Memory**.  
You can store facts, recall them, generate **AI-powered summaries**, and clear Orion’s memory.
---
""")

col1, col2 = st.columns([2, 1])

# -------------------------------
# Left Panel: Add Facts
# -------------------------------
with col1:
    user_input = st.text_input("💬 Type something for Orion to remember:")

    if user_input:
        st.session_state.chat_history.append(("You", user_input))
        try:
            resp = requests.post(
                f"{API_BASE}/fact",
                json={"user_id": USER_ID, "fact": user_input}
            )
            if resp.status_code == 200:
                reply = "✅ Stored in Orion memory."
            else:
                reply = f"[Error {resp.status_code}] {resp.text}"
        except Exception as e:
            reply = f"[Exception] {e}"

        st.session_state.chat_history.append(("Orion", reply))

    st.subheader("Conversation")
    for role, msg in st.session_state.chat_history:
        icon = "🧑" if role == "You" else "🤖"
        st.markdown(f"**{icon} {role}:** {msg}")

# -------------------------------
# Right Panel: Tools
# -------------------------------
with col2:
    st.subheader("🧠 Orion’s Tools")

    # Recall
    if st.button("🔎 Recall"):
        try:
            resp = requests.get(f"{API_BASE}/recall/{USER_ID}")
            if resp.status_code == 200:
                results = resp.json()
                if results:
                    st.write("**Memories Found:**")
                    for i, r in enumerate(results, start=1):
                        text = r.get("fact", str(r)) if isinstance(r, dict) else str(r)
                        st.markdown(f"**{i}.** {text}")
                else:
                    st.info("No memories found.")
            else:
                st.error(f"[Error {resp.status_code}] {resp.text}")
        except Exception as e:
            st.error(f"[Exception] {e}")

    # Summarize with AI
    if st.button("📝 Summarize with AI"):
        try:
            resp = requests.get(f"{API_BASE}/recall/{USER_ID}")
            if resp.status_code == 200:
                facts = resp.json()
                if facts and openai.api_key:
                    prompt = (
                        "Here are facts about a user:\n"
                        + "\n".join(f"- {fact}" for fact in facts)
                        + "\n\nSummarize the key themes in 2–3 natural sentences."
                    )
                    ai_resp = openai.ChatCompletion.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "You are a helpful summarizer."},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=150
                    )
                    summary = ai_resp["choices"][0]["message"]["content"].strip()
                    st.success(f"**Summary:** {summary}")
                else:
                    st.warning("No facts stored yet.")
            else:
                st.error(f"[Error {resp.status_code}] {resp.text}")
        except Exception as e:
            st.error(f"[Exception] {e}")

    # Decay
    if st.button("🔥 Forget All"):
        try:
            resp = requests.post(f"{API_BASE}/decay")
            if resp.status_code == 200:
                st.warning("🧹 Orion’s memory has been cleared.")
            else:
                st.error(f"[Error {resp.status_code}] {resp.text}")
        except Exception as e:
            st.error(f"[Exception] {e}")
