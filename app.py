import streamlit as st
import requests

API_BASE = "https://orion-memory.onrender.com"  # your backend
USER_ID = "1"  # must be a string per API schema

st.set_page_config(page_title="Orion Memory Demo", page_icon="🛰️", layout="wide")

# -------------------------------
# Initialize session state
# -------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("🛰️ Orion Memory Demo (Live API)")
st.write("This demo shows Orion remembering (`/fact`), recalling (`/recall`), summarizing (`/summarize`), and decaying (`/decay`).")

col1, col2 = st.columns([2, 1])

# -------------------------------
# Left Panel: Store in Memory
# -------------------------------
with col1:
    user_input = st.text_input("💬 Type something for Orion to remember:")

    if user_input:
        st.session_state.chat_history.append(("You", user_input))

        try:
            # Send fact to Orion memory (user_id as string)
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

    # Show chat log
    st.subheader("Conversation")
    for role, msg in st.session_state.chat_history:
        if role == "You":
            st.markdown(f"**🧑 {role}:** {msg}")
        else:
            st.markdown(f"**🤖 {role}:** {msg}")

# -------------------------------
# Right Panel: Recall / Summarize / Decay
# -------------------------------
with col2:
    st.subheader("🧠 Orion’s Tools")

    # Recall
    if st.button("🔎 Recall Now"):
        try:
            resp = requests.get(f"{API_BASE}/recall/{USER_ID}")
            if resp.status_code == 200:
                results = resp.json()
                if results:
                    st.write("**Memories Found:**")
                    for i, r in enumerate(results, start=1):
                        if isinstance(r, dict):
                            fact_text = r.get("fact", str(r))
                            st.markdown(f"**{i}.** {fact_text}")
                        else:
                            st.markdown(f"**{i}.** {r}")
                else:
                    st.write("No memories found.")
            else:
                st.write(f"[Error {resp.status_code}] {resp.text}")
        except Exception as e:
            st.write(f"[Exception] {e}")

    # Summarize
    if st.button("📝 Summarize"):
        try:
            resp = requests.get(f"{API_BASE}/summarize/{USER_ID}")
            if resp.status_code == 200:
                summary = resp.json().get("summary", "No summary available.")
                st.success(f"**Summary:** {summary}")
            else:
                st.write(f"[Error {resp.status_code}] {resp.text}")
        except Exception as e:
            st.write(f"[Exception] {e}")

    # Decay
    if st.button("🔥 Decay (Forget All)"):
        try:
            resp = requests.post(f"{API_BASE}/decay")
            if resp.status_code == 200:
                st.warning("🧹 Orion’s memory has been cleared.")
            else:
                st.write(f"[Error {resp.status_code}] {resp.text}")
        except Exception as e:
            st.write(f"[Exception] {e}")
