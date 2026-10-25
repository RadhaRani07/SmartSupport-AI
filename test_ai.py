import ollama

response = ollama.chat(
    model="qwen2.5:3b",
    messages=[
        {
            "role": "user",
            "content": "Explain customer support ticket classification in one sentence."
        }
    ]
)

print("\nAI Response:")
print(response["message"]["content"])