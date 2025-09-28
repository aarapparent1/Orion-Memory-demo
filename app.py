import streamlit as st
import requests

API_BASE = "https://orion-memory.onrender.com"
USER_ID = "1"   # simple fixed ID

st.set_page_config(page_title="🛰️ Orion Memory Demo", layout="wide")

st.title("🛰️ Orion Memory Demo (Live API)")
st.caption("This demo shows Orion remembering (/fact), recalling (/recall), summarizing, and forgetting.")

# -----------------------------
# Input section
# -----------------------------
user_input = st.text_input("💬 Type something for Orion to remember:")

if st.button("➕ Store in Orion"):
    if user_input.strip():
        payload = {"user_id": USER_ID, "fact": user_input.strip()}
        resp = requests.post(f"{API_BASE}/fact", json=payload)
        st.write(resp.json())
    else:
        st.warning("Please type something first!")

# -----------------------------
# Actions
# -----------------------------
if st.button("🔎 Recall"):
    resp = requests.get(f"{API_BASE}/recall/{USER_ID}")
    st.write(resp.json())

if st.button("📝 Summarize"):
    resp = requests.post(f"{API_BASE}/summarize/{USER_ID}")
    st.write(resp.json())

if st.button("🗑️ Forget"):
    resp = requests.post(f"{API_BASE}/decay")
    st.write(resp.json())
