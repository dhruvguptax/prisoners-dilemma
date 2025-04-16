def payoff(player1, player2):
    """Returns tuple of (p1_score, p2_score)"""
    outcomes = {
        ('cooperate', 'cooperate'): (3, 3),
        ('cooperate', 'defect'): (0, 5),
        ('defect', 'cooperate'): (5, 0),
        ('defect', 'defect'): (1, 1)
    }
    return outcomes[(player1, player2)]
