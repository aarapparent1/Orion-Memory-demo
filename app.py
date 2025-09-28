import streamlit as st
import requests
from openai import OpenAI

# Orion API config
API_BASE = "https://orion-memory.onrender.com"
USER_ID = "1"

# OpenAI client (for Book Mode & Summarize)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="🛰️ Orion Memory Demo", layout="wide")
st.title("🛰️ Orion Memory Demo (Live API)")
st.caption("This demo shows Orion remembering, recalling, summarizing, and forgetting. Includes 📚 Book Mode.")

# -----------------------------
# Input
# -----------------------------
user_input = st.text_area("💬 Type something for Orion to remember:")

if st.button("➕ Store in Orion"):
    if user_input.strip():
        payload = {"user_id": USER_ID, "fact": user_input.strip()}
        resp = requests.post(f"{API_BASE}/fact", json=payload)
        if resp.status_code == 200:
            st.success("✅ Stored in Orion memory.")
        else:
            st.error(f"[Error {resp.status_code}] {resp.text}")
    else:
        st.warning("Please type something first!")

# -----------------------------
# Two-column layout
# -----------------------------
col1, col2 = st.columns(2)

# Left column: memory tools
with col1:
    st.subheader("🧾 Memory Tools")

    if st.button("🔎 Recall"):
        resp = requests.get(f"{API_BASE}/recall/{USER_ID}")
        if resp.status_code == 200:
            facts = resp.json()
            if facts:
                st.write("### Current Memory")
                for f in facts:
                    st.write("- " + f)
            else:
                st.info("No facts stored yet.")
        else:
            st.error(f"[Error {resp.status_code}] {resp.text}")

    if st.button("🗑️ Forget"):
        resp = requests.post(f"{API_BASE}/decay")
        if resp.status_code == 200:
            st.success("🗑️ Orion memory cleared.")
        else:
            st.error(f"[Error {resp.status_code}] {resp.text}")

# Right column: AI summaries
with col2:
    st.subheader("🧠 AI Summaries")

    if st.button("📝 Summarize with AI"):
        resp = requests.get(f"{API_BASE}/recall/{USER_ID}")
        if resp.status_code == 200:
            facts = resp.json()
            if facts:
                text = "\n".join(facts)
                ai_resp = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful summarizer."},
                        {"role": "user", "content": f"Summarize these notes:\n{text}"}
                    ],
                    max_tokens=400
                )
                st.success("**Summary:** " + ai_resp.choices[0].message.content.strip())
            else:
                st.warning("No facts stored yet.")
        else:
            st.error(f"[Error {resp.status_code}] {resp.text}")

    if st.button("📚 Book Mode"):
        resp = requests.get(f"{API_BASE}/recall/{USER_ID}")
        if resp.status_code == 200:
            facts = resp.json()
            if facts:
                batch_size = 20
                summaries = []
                # Step 1: summarize batches
                for i in range(0, len(facts), batch_size):
                    batch = facts[i:i+batch_size]
                    prompt = "Summarize these facts:\n" + "\n".join(f"- {f}" for f in batch)
                    ai_resp = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "You are a helpful summarizer."},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=300
                    )
                    summaries.append(ai_resp.choices[0].message.content.strip())

                # Step 2: combine summaries
                mega_prompt = "Combine these section summaries into one full-book summary:\n" + "\n".join(summaries)
                ai_final = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful summarizer."},
                        {"role": "user", "content": mega_prompt}
                    ],
                    max_tokens=600
                )
                st.success("**Full Digest:** " + ai_final.choices[0].message.content.strip())
            else:
                st.warning("No facts stored yet.")
        else:
            st.error(f"[Error {resp.status_code}] {_]()
