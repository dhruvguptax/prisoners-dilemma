
import matplotlib.pyplot as plt
import os
from pathlib import Path
import random

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
    """Generates and saves outcome visualization"""
    project_root = Path(__file__).parent.parent
    data_dir = project_root / 'data'
    data_dir.mkdir(exist_ok=True)  
    
    outcomes = ['CC', 'CD', 'DC', 'DD']
    p1_scores = [3, 0, 5, 1]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(outcomes, p1_scores, color=['green', 'red', 'blue', 'grey'])
    plt.title("Prisoner's Dilemma Outcomes (Player 1 Perspective)", pad=20)
    plt.ylabel('Years in Prison')
    plt.ylim(0, 6)
    
   
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height}',
                 ha='center', va='bottom')
    
    output_path = data_dir / 'pd_outcomes.png'
    plt.savefig(output_path)
    plt.close()
    print(f"Saved plot to: {output_path}")

def simulate_rounds(num_rounds=100):
    """Simulates random choices between two players"""
    results = []
    for _ in range(num_rounds):
        p1 = random.choice(['cooperate', 'defect'])
        p2 = random.choice(['cooperate', 'defect'])
        results.append(payoff(p1, p2))
    return results

if __name__ == "__main__":
   
    plot_outcomes()
    
    
    print("\n🎮 Prisoner's Dilemma Simulator 🎮")
    print("----------------------------------")
    
    while True:
        p1 = input("\nPlayer 1 decision (cooperate/defect/q to quit): ").lower()
        if p1 == 'q':
            break
            
        p2 = input("Player 2 decision (cooperate/defect/q to quit): ").lower()
        if p2 == 'q':
            break

        if p1 not in ['cooperate', 'defect'] or p2 not in ['cooperate', 'defect']:
            print("⚠️ Invalid input! Must choose 'cooperate' or 'defect'")
            continue

        p1_score, p2_score = payoff(p1, p2)
        print(f"\n🔍 Results:")
        print(f"Player 1: {p1_score} years | Player 2: {p2_score} years")
    
    print("\n📊 Check the 'data' folder for outcome visualization!")
