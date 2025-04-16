import matplotlib.pyplot as plt
import random
from pathlib import Path

def payoff(p1, p2):
    outcomes = {
        ('cooperate', 'cooperate'): (3, 3),
        ('cooperate', 'defect'): (0, 5),
        ('defect', 'cooperate'): (5, 0),
        ('defect', 'defect'): (1, 1)
    }
    return outcomes[(p1, p2)]

def tit_for_tat(history):
    return 'cooperate' if not history else history[-1][1]

def random_strategy(_):
    return random.choice(['cooperate', 'defect'])

def always_cooperate(_):
    return 'cooperate'

def always_defect(_):
    return 'defect'

def plot_outcomes():
    project_root = Path(__file__).parent.parent
    data_dir = project_root / 'data'
    data_dir.mkdir(exist_ok=True)
    
    outcomes = ['CC', 'CD', 'DC', 'DD']
    scores = [3, 0, 5, 1]
    
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(10,6))
    bars = ax.bar(outcomes, scores, color=['#4c72b0','#dd8452','#55a868','#c44e52'])
    ax.set_title('Prisoner\'s Dilemma Outcomes', pad=20)
    ax.set_ylabel('Years in Prison')
    ax.grid(True, alpha=0.3)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height, f'{height}', ha='center', va='bottom')
    
    plt.savefig(data_dir / 'pd_outcomes.png', dpi=120, bbox_inches='tight')
    plt.close()

def simulate_rounds(strategy1, strategy2, rounds=100):
    history = []
    for _ in range(rounds):
        p1 = strategy1(history)
        p2 = strategy2(history)
        result = payoff(p1, p2)
        history.append((p1, p2, result))
    return history

def cooperation_rate(history):
    coop = sum(1 for round in history if round[0] == 'cooperate')
    return coop / len(history) * 100

def run_tournament(strategies, rounds=50):
    results = {}
    for s1 in strategies:
        for s2 in strategies:
            history = simulate_rounds(strategies[s1], strategies[s2], rounds)
            key = f"{s1} vs {s2}"
            results[key] = cooperation_rate(history)
    return results

if __name__ == "__main__":
    plot_outcomes()
    
    print("=== Interactive Prisoner's Dilemma ===")
    while True:
        print("\nChoose an option:")
        print("1. Play manually")
        print("2. Run strategy tournament")
        print("3. Exit")
        
        choice = input("Enter choice (1-3): ")
        
        if choice == '1':
            p1 = input("Player 1 (cooperate/defect): ").lower()
            p2 = input("Player 2 (cooperate/defect): ").lower()
            
            if p1 not in ['cooperate', 'defect'] or p2 not in ['cooperate', 'defect']:
                print("Invalid choice! Must choose 'cooperate' or 'defect'")
                continue
                
            result = payoff(p1, p2)
            print(f"\nPlayer 1 gets {result[0]} years")
            print(f"Player 2 gets {result[1]} years")
            
        elif choice == '2':
            strategies = {
                'TitForTat': tit_for_tat,
                'Random': random_strategy,
                'AlwaysCooperate': always_cooperate,
                'AlwaysDefect': always_defect
            }
            print("\n=== Strategy Tournament Results ===")
            results = run_tournament(strategies)
            for matchup, rate in results.items():
                print(f"{matchup}: {rate:.1f}% cooperation")
                
        elif choice == '3':
            break
            
        else:
            print("Invalid choice! Please enter 1, 2, or 3")
