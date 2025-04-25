import streamlit as st
import json

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


# Streamlit UI
st.title("🧠 AskARCON")
user_input = st.text_input("Ask your question here:")

if st.button("Submit"):
    top_matches = get_top_matches(user_input)
    if top_matches:
        for i, match in enumerate(top_matches, start=1):
            with st.expander(f"Match {i}: {match['question']}"):
                st.markdown(f"**Resolution:** {match['answer']}")
    else:
        st.warning("Sorry, I don't understand that.")
