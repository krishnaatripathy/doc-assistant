import ollama

SYSTEM_PROMPT = (
    "You are a question-answering system.\n"
    "Answer ONLY using the provided context.\n"
    'If the answer is not found in the context, say "Not found in the provided documents."'
)

def generate_answer(context: str, question: str) -> str:
    if not context.strip():
        return "Not found in the provided documents."

    prompt = f"""
{SYSTEM_PROMPT}

Context:
{context}

Question:
{question}
"""

    response = ollama.chat(
        model="mistral",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"].strip()
