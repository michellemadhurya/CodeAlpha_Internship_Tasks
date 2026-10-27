
import json
import re
from pathlib import Path
from datetime import datetime

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ---------- NOVA: Mini AI Knowledge Assistant ----------

BOT_NAME = "NOVA"
VERSION = "1.1"

def clean_text(text):
    """Normalize text before matching."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return " ".join(text.split())


# Load FAQ dataset
file_path = Path(__file__).parent / "faqs.json"

with file_path.open("r", encoding="utf-8") as file:
    faqs = json.load(file)

questions = [faq["question"] for faq in faqs]
answers = [faq["answer"] for faq in faqs]

# Prepare TF-IDF question vectors
vectorizer = TfidfVectorizer(ngram_range=(1, 2))
faq_vectors = vectorizer.fit_transform(
    [clean_text(question) for question in questions]
)

# Session statistics
total_questions = 0
answered_questions = 0
conversation_history = []

# Start screen
print("\n" + "=" * 42)
print(f"       {BOT_NAME} | KNOWLEDGE ASSISTANT")
print(f"                Version {VERSION}")
print("=" * 42)
print("Hello! I'm NOVA, your mini AI knowledge assistant.")
print("Ask me about Python, AI, machine learning, and more.")
print("\nType 'help' to see commands.")
print("Type 'exit' to end the session.")


while True:
    user_input = input("\nYou: ").strip()
    command = user_input.lower()

    if command in ["exit", "quit", "bye"]:
        print("\nNOVA: Thanks for exploring with me!")
        print("NOVA: Keep learning, one question at a time.")

        if total_questions:
            rate = answered_questions / total_questions * 100
            print(f"\nSession answer rate: {rate:.1f}%")
            print(f"Questions asked: {total_questions}")
            print(f"Questions answered: {answered_questions}")

        print("Goodbye!\n")
        break

    if not user_input:
        print("NOVA: Type a question or enter 'help' for options.")
        continue

    # Friendly commands
    if command == "help":
        print("\nNOVA COMMAND GUIDE")
        print("------------------")
        print("help     - Show available commands")
        print("topics   - Show FAQ topics")
        print("stats    - Show session statistics")
        print("history  - Show your recent questions")
        print("time     - Show the current date and time")
        print("exit     - End the conversation")
        continue

    if command == "topics":
        print("\nNOVA: Here are the topics I know about:")
        for number, question in enumerate(questions, start=1):
            print(f"  {number}. {question}")
        continue

    if command == "stats":
        print("\nNOVA SESSION STATISTICS")
        print("-----------------------")
        print(f"Questions asked: {total_questions}")
        print(f"Questions answered: {answered_questions}")
        print(f"FAQs available: {len(faqs)}")

        if total_questions:
            rate = answered_questions / total_questions * 100
            print(f"Answer rate: {rate:.1f}%")
        else:
            print("Ask a question to begin your statistics.")

        continue

    if command == "history":
        if conversation_history:
            print("\nNOVA: Your recent questions:")
            for number, item in enumerate(
                conversation_history[-5:], start=1
            ):
                print(f"  {number}. {item}")
        else:
            print("NOVA: Your question history is empty.")
        continue

    if command == "time":
        print("NOVA:", datetime.now().strftime("%d %B %Y, %I:%M %p"))
        continue

    # Match the user's question against the FAQ dataset
    total_questions += 1
    conversation_history.append(user_input)

    cleaned_input = clean_text(user_input)
    user_vector = vectorizer.transform([cleaned_input])

    scores = cosine_similarity(user_vector, faq_vectors)[0]
    best_index = scores.argmax()
    best_score = scores[best_index]

    if best_score < 0.15:
        print("\nNOVA: Hmm, I couldn't find a reliable FAQ match.")
        print("NOVA: Try 'topics' to explore what I can answer.")
    else:
        answered_questions += 1
        print(f"\nNOVA: {answers[best_index]}")
        print(f"Matched topic: {questions[best_index]}")
        print(f"Match confidence (similarity): {best_score:.2f}")
        
        if best_score >= 0.50:
            print("NOVA: That looks like a strong match!")
