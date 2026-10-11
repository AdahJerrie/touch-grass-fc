import json
import requests
from teams import make_teams

# 1. Read the chat you pasted into chat.txt
with open("chat.txt") as f:
    CHAT = f.read()

PROMPT = f"""You read a football group chat and list who is playing on Saturday.
Reply with JSON only, in exactly this shape:
{{"players": [{{"name": "Tobi", "status": "in"}}]}}
Rules:
- status must be exactly one of: "in", "out", "maybe".
- If someone brings a guest, add the guest as a separate player with status "in".
- Include every person who posted, even those who are out.

Chat:
{CHAT}"""

# 2. Ask the local model (the "secretary") to read it
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

data = json.loads(response.json()["message"]["content"])

# 3. Load ratings if the file exists (optional)
try:
    with open("players.json") as f:
        ratings = json.load(f)
except FileNotFoundError:
    ratings = {}

# 4. Split into teams (the "coach")
playing = [p["name"] for p in data["players"] if p["status"] == "in"]
maybes = [p["name"] for p in data["players"] if p["status"] == "maybe"]

team_a, team_b, score_a, score_b = make_teams(playing, ratings)

print("Team A:", ", ".join(team_a), f"(strength {score_a})")
print("Team B:", ", ".join(team_b), f"(strength {score_b})")
print("Maybe (reserves):", ", ".join(maybes) or "none")