def make_teams(names, ratings, default=3):
    #strongest players first
    players = sorted(names, key=lambda n: ratings.get(n, default), reverse=True)

    team_a, team_b = [], []
    score_a = score_b = 0
    max_size = (len(players) + 1) // 2  # no team gets more than half (rounded up)


    for name in players:
        score = ratings.get(name, default)
        a_full = len(team_a) >= max_size
        b_full = len(team_b) >= max_size

        # Give the player to the weaker team, unless that team is already full
        if b_full or (not a_full and score_a <= score_b):
            team_a.append(name)
            score_a += score
        else:
            team_b.append(name)
            score_b += score

    return team_a, team_b, score_a, score_b