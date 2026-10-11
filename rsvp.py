import json
import requests


def extract_players(chat_text):
    prompt = f"""You read a football group chat and list who is playing on Saturday.
Reply with JSON only, in exactly this shape:
{{"players": [{{"name": "Tobi", "status": "in"}}]}}
Rules:
- status must be exactly one of: "in", "out", "maybe".
- If someone brings a guest, add the guest as a separate player with status "in".
- Include every person who posted, even those who are out.

Chat:
{chat_text}"""

    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "gemma4:e2b-it-qat",
            "messages": [{"role": "user", "content": prompt}],
            "format": "json",
            "stream": False,
            "keep_alive": "30m",
            "options": {"temperature": 0},
        },
        timeout=300,
    )
    return json.loads(response.json()["message"]["content"])["players"]