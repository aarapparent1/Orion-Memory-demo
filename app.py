import streamlit as st
import requests
from openai import OpenAI

# 🔧 Config
API_BASE = "https://orion-memory.onrender.com"
USER_ID = "demo-user"

# Load OpenAI key from secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="🛰️ Orion Memory Demo", layout="wide")

st.title("🛰️ Orion Memory Demo (Live API)")
st.caption("This demo shows Orion remembering, recalling, and summarizing in real time.")

# User input
user_input = st.text_area("💬 Type something for Orion to remember:")

if st.button("Store in Orion"):
    if user_input.strip():
        payload = {"user_id": USER_ID, "fact": user_input.strip()}
        resp = requests.post(f"{API_BASE}/fact", json=payload)
        if resp.status_code == 200:
            st.success("✅ Stored in Orion memory.")
        else:
            st.error(f"[Error {resp.status_code}] {resp.text}")
    else:
        st.warning("Please type something first!")

# Layout
col1, col2 = st.columns(2)

# Left column: recall
with col1:
    if st.button("🔎 Recall Memory"):
        try:
            resp = requests.get(f"{API_BASE}/recall/{USER_ID}")
            if resp.status_code == 200:
                facts = resp.json()
                if facts:
                    st.write("### Memory Recall")
                    for f in facts:
                        st.write("- " + f)
                else:
                    st.info("No facts stored yet.")
            else:
                st.error(f"[Error {resp.status_code}] {resp.text}")
        except Exception as e:
            st.error(f"[Exception] {e}")

# Right column: summarize + book mod
