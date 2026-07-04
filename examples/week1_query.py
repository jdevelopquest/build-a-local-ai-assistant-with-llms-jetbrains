# examples/week1_query.py
import httpx

API_URL = "http://localhost:8000/v1/chat/completions"


def ask(question: str, temperature: float = 0.7) -> str:
    payload = {
        "model": "llama3.1:8b",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant that formats answers as plain text.",
            },
            {"role": "user", "content": question},
        ],
        "temperature": temperature,
    }
    response = httpx.post(API_URL, json=payload, timeout=600.0)
    if response.status_code >= 400:
        print("Request failed with status code:", response.status_code)
        print("Server said:", response.text)  # reveals the real cause
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


if __name__ == "__main__":
    for idx, question in enumerate(
        [
            "Explain what embeddings are",
            "What is RAG in the context of LLMs?",
            "What is a vector database?",
        ]
    ):
        print(f"Question {idx + 1}: {question}")
        print(f"Answer: {ask(question)}")
