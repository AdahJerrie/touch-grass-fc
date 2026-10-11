def make_teams(names, ratings, num_teams=2, default=3):
    # Strongest players first
    players = sorted(names, key=lambda n: ratings.get(n, default), reverse=True)

    teams = [[] for _ in range(num_teams)]
    scores = [0] * num_teams
    max_size = (len(players) + num_teams - 1) // num_teams  # biggest team size allowed

    for name in players:
        score = ratings.get(name, default)
        # Teams that still have room
        open_teams = [i for i in range(num_teams) if len(teams[i]) < max_size]
        # Give the player to the weakest of those teams
        weakest = min(open_teams, key=lambda i: scores[i])
        teams[weakest].append(name)
        scores[weakest] += score

    return teams, scores