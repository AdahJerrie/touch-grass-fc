[1mdiff --git a/rsvp.py b/rsvp.py[m
[1mindex 2833b5b..19935e1 100644[m
[1m--- a/rsvp.py[m
[1m+++ b/rsvp.py[m
[36m@@ -1,5 +1,6 @@[m
 import json[m
 import requests[m
[32m+[m[32mfrom teams import make_teams[m
 [m
 CHAT = """[m
 Tobi: I'm in for Saturday[m
[36m@@ -37,5 +38,14 @@[m [mresponse = requests.post([m
 reply = response.json()["message"]["content"][m
 data = json.loads(reply)[m
 [m
[31m-for player in data["players"]:[m
[31m-    print(player["name"], "->", player["status"])[m
\ No newline at end of file[m
[32m+[m[32mwith open("players.json") as f:[m
[32m+[m[32m    ratings = json.load(f)[m
[32m+[m
[32m+[m[32mplaying = [p["name"] for p in data["players"] if p["status"] == "in"][m
[32m+[m[32mmaybes = [p["name"] for p in data["players"] if p["status"] == "maybe"][m
[32m+[m
[32m+[m[32mteam_a, team_b, score_a, score_b = make_teams(playing, ratings)[m
[32m+[m
[32m+[m[32mprint("Team A:", ", ".join(team_a), f"(strength {score_a})")[m
[32m+[m[32mprint("Team B:", ", ".join(team_b), f"(strength {score_b})")[m
[32m+[m[32mprint("Maybe (reserves):", ", ".join(maybes) or "none")[m
\ No newline at end of file[m
