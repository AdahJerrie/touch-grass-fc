import requests

response = requests.post(
    "http://localhost:11434/api/chat",
    json={
        "model": "gemma3:1b",
        "messages": [
            {"role": "user", "content": "Say hi to a football team in one sentence."}
        ],
        "stream": False,
    },
)

reply = response.json()
print(reply["message"]["content"])