import json
import requests

CHAT = """
Tobi: I'm in for Saturday
Kevin: count me in, bringing my cousin Brian
Amina: can't make it, work
Joel: maybe, depends on my shift
Wanjiru: in!
Peter: sorry guys, out this week
"""

PROMPT = f"""You read a football group chat and list who is playing on Saturday.
Reply with JSON only, in exactly this shape:
{{"players": [{{"name": "Tobi", "status": "in"}}]}}
Rules:
- status must be exactly one of: "in", "out", "maybe".
- If someone brings a guest, add the guest as a separate player with status "in".
- Include every person who posted, even those who are out.

Chat:
{CHAT}"""

response = requests.post(
    "http://localhost:11434/api/chat",
    json={
        "model": "gemma4:e2b-it-qat",
        "messages": [{"role": "user", "content": PROMPT}],
        "format": "json",
        "stream": False,
        "keep_alive": "30m",
        "options": {"temperature": 0},
    },
    timeout=300,
)

reply = response.json()["message"]["content"]
data = json.loads(reply)

for player in data["players"]:
    print(player["name"], "->", player["status"])