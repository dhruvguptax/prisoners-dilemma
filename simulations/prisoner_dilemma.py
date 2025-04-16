import matplotlib.pyplot as plt

def payoff(player1, player2):
    """Returns tuple of (p1_score, p2_score)"""
    outcomes = {
        ('cooperate', 'cooperate'): (3, 3),
        ('cooperate', 'defect'): (0, 5),
        ('defect', 'cooperate'): (5, 0),
        ('defect', 'defect'): (1, 1)
    }
    return outcomes[(player1, player2)]
    
def plot_outcomes():
    outcomes = ['CC', 'CD', 'DC', 'DD']
    scores = [3, 0, 5, 1]
    
    plt.bar(outcomes, scores, color=['green', 'red', 'blue', 'gray'])
    plt.title("Prisoner's Dilemma Outcomes (Player 1)")
    plt.ylabel('Years in Prison')
    plt.savefig('pd_outcomes.png')  
    plt.close()

if __name__ == "__main__":
    print("Prisoner's Dilemma Simulator")
    p1 = input("Player 1 (cooperate/defect): ").lower()
    p2 = input("Player 2 (cooperate/defect): ").lower()
    
    result = payoff(p1, p2)
    print(f"\nPlayer 1 gets {result[0]} years")
    print(f"Player 2 gets {result[1]} years")
    
    plot_outcomes()  

if __name__ == "__main__":
    plot_outcomes()  
    
    print("Prisoner's Dilemma Simulator")
    p1 = input("Player 1 (cooperate/defect): ").lower()
    p2 = input("Player 2 (cooperate/defect): ").lower()
    result = payoff(p1, p2)
    print(f"\nPlayer 1 gets {result[0]} years")
    print(f"Player 2 gets {result[1]} years")
