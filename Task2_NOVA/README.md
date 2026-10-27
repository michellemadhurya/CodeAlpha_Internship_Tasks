# NOVA - Mini AI Knowledge Assistant

## About the project

Hi! This is my FAQ chatbot project, which I built using Python as part of my CodeAlpha internship task.

I named it NOVA. It answers questions about Python, AI, machine learning, NLP, and a few other related topics. Instead of giving random answers, it checks the user's question against a list of FAQs and picks the closest match.

## What can it do?

- Answer questions from my FAQ dataset.
- Show the list of topics it knows about.
- Display help for the available commands.
- Keep track of questions asked during a session.
- Show recently asked questions.
- Display the current date and time.
- Give a message when it cannot find a suitable answer.

## Tools I used

- Python
- Scikit-learn
- JSON
- TF-IDF
- Cosine similarity

## Files in this project

- `main.py` - Contains the chatbot code.
- `faqs.json` - Stores the questions and answers.
- `README.md` - Explains the project and how to run it.

## How to run it

First, make sure Python is installed on your computer.

Install scikit-learn using this command:

```bash
py -m pip install scikit-learn
```

Then open the project folder in VS Code and run:

```bash
py main.py
```

The chatbot will start in the terminal, and you can begin asking questions.

## Commands

- `help` - Shows the available commands.
- `topics` - Lists the FAQ topics.
- `stats` - Shows session statistics.
- `history` - Shows recent questions.
- `time` - Displays the date and time.
- `exit` - Closes the chatbot.

## How it works

I used TF-IDF to convert the FAQ questions into numerical representations. When a user enters a question, the program compares it with the stored questions using cosine similarity and returns the answer with the closest match.

## What I learned

While building this project, I got practice working with Python, JSON files, text processing, and basic natural language processing. I also learned how similarity scores can help match a user's question with stored information.

## A small limitation

NOVA can answer questions based on the FAQs I added. It may not understand every way a question is written, and it cannot answer topics that are not covered well by its dataset.

## Conclusion

This project helped me understand how a simple FAQ chatbot works. I also added a few commands to make it easier to use than a basic question-and-answer program.
