def payoff(player1, player2):
    """Returns tuple of (p1_score, p2_score)"""
    outcomes = {
        ('cooperate', 'cooperate'): (3, 3),
        ('cooperate', 'defect'): (0, 5),
        ('defect', 'cooperate'): (5, 0),
        ('defect', 'defect'): (1, 1)
    }
    return outcomes[(player1, player2)]
    
if __name__ == "__main__":
    print("Prisoner's Dilemma Simulator")
    p1 = input("Player 1 (cooperate/defect): ").lower()
    p2 = input("Player 2 (cooperate/defect): ").lower()
    
    result = payoff(p1, p2)
    print(f"\nPlayer 1 gets {result[0]} years")
    print(f"Player 2 gets {result[1]} years")
