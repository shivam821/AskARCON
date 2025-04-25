import streamlit as st
import json
import clipboard

# Load questions and answers
with open("data.json", "r") as file:
    qa_data = json.load(file)

def get_top_matches(user_input, top_n=3):
    user_words = set(user_input.lower().split())
    scored_matches = []

    for qa in qa_data:
        question_words = set(qa['question'].lower().split())
        common_words = user_words & question_words
        score = len(common_words)
        if score > 0:
            scored_matches.append((score, qa))

    scored_matches.sort(reverse=True, key=lambda x: x[0])
    return [qa for score, qa in scored_matches[:top_n]]

def on_copy_click(text):
    st.session_state.copied.append(text)
    clipboard.copy(text)

# Initialize session states
if "messages" not in st.session_state:
    st.session_state.messages = []

if "copied" not in st.session_state:
    st.session_state.copied = []

# Title
st.title("🧠 AskARCON")

# Show chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question from the knowledge base..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    top_matches = get_top_matches(prompt)

    if top_matches:
        with st.chat_message("assistant"):
            for i, match in enumerate(top_matches, start=1):
                with st.expander(f"Match {i}: {match['question']}"):
                    st.markdown(
                        f"""
                        <div style="border:1px solid #ddd; border-radius:5px; padding:10px; background-color:#0000; margin-bottom : 20px;">
                            <pre style="height: 150px; overflow-y: auto; font-family: monospace;">{match['answer']}</pre>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # Unique key for each button
                    # if st.button(f"📋 Copy Resolution", key=f"copy_btn_{i}"):
                    #     on_copy_click(match['answer'])

    else:
        with st.chat_message("assistant"):
            st.warning("Sorry, I don't understand that.")

# Show toast for copied messages
for text in st.session_state.copied:
    st.toast(f"Copied to clipboard: {text}", icon="✅")

