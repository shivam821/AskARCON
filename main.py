import json

# Load questions and answers
with open("data.json", "r") as file:
    qa_data = json.load(file)

def get_best_match(user_input):
    user_words = set(user_input.lower().split())
    best_match = None
    max_matches = 0

    for qa in qa_data:
        question_words = set(qa['question'].lower().split())
        common_words = user_words & question_words
        if len(common_words) > max_matches:
            max_matches = len(common_words)
            best_match = qa

    if best_match and max_matches > 0:
        return best_match['answer']
    else:
        return "Sorry, I don't understand that."

# Chat loop
print("Chatbot: Hello! Ask me something (type 'exit' to quit).")
while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        print("Chatbot: Goodbye!")
        break
    response = get_best_match(user_input)
    print("Chatbot:", response)
