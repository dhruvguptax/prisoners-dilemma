# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import random
from pathlib import Path
from typing import List, Tuple, Dict, Callable, Any # Added Any for manual history type
import os # Import os to help show current working directory if needed
import datetime # To add timestamp to manual plot filename

# Define type aliases for clarity
Move = str  # 'cooperate' or 'defect'
Payoff = Tuple[int, int]
HistoryRound = Tuple[Move, Move, Payoff] # For simulation history
History = List[HistoryRound]
PlayerHistory = List[Move]
StrategyFunction = Callable[[PlayerHistory, PlayerHistory], Move]
ManualHistoryItem = Tuple[Move, Move, int, int] # (p1_move, p2_move, p1_score, p2_score)
ManualHistory = List[ManualHistoryItem] # For manual play history

# Core Game Logic
def payoff(p1_move: Move, p2_move: Move) -> Payoff:
    """Calculates the payoffs for Player 1 and Player 2 based on their moves."""
    outcomes: Dict[Tuple[Move, Move], Payoff] = {
        ('cooperate', 'cooperate'): (3, 3),
        ('cooperate', 'defect'): (0, 5),
        ('defect', 'cooperate'): (5, 0),
        ('defect', 'defect'): (1, 1)
    }
    return outcomes[(p1_move, p2_move)]

# --- Strategies ---
def tit_for_tat(my_history: PlayerHistory, opponent_history: PlayerHistory) -> Move:
    if not opponent_history: return 'cooperate'
    return opponent_history[-1]

def random_strategy(my_history: PlayerHistory, opponent_history: PlayerHistory) -> Move:
    return random.choice(['cooperate', 'defect'])

def always_cooperate(my_history: PlayerHistory, opponent_history: PlayerHistory) -> Move:
    return 'cooperate'

def always_defect(my_history: PlayerHistory, opponent_history: PlayerHistory) -> Move:
    return 'defect'

# --- Path Helper Function ---
def get_data_dir() -> Path:
    """Determines the correct 'data' directory path (root folder/data)."""
    script_location = None
    try:
        script_location = Path(__file__).resolve().parent
        # If script is in 'simulations', go up one level
        if script_location.name == 'simulations':
             base_dir = script_location.parent
        else:
             base_dir = script_location
    except NameError:
         # Fallback: use cwd, hoping it's the project root
         base_dir = Path.cwd()
         print(f"[Warning] __file__ not defined. Assuming CWD is project root: {base_dir}")

    data_dir = base_dir / 'data'
    # Ensure the directory exists
    try:
        data_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(f"Error creating data directory {data_dir}: {e}")
        raise # Re-raise error if directory can't be made
    except Exception as e:
        print(f"An unexpected error occurred during data directory creation for {data_dir}: {e}")
        raise
    return data_dir


# --- Visualization ---
def plot_static_payoffs():
    """
    Generates and saves the STATIC bar chart of Player 1's base payoffs
    in the 'data/' subdirectory (root folder > data).
    Filename: pd_static_outcomes.png
    """
    try:
        data_dir = get_data_dir()
        print(f"[Debug-StaticPlot] Using data directory: {data_dir}")
    except Exception as e:
        print(f"Could not get or create data directory for static plot: {e}")
        return

    outcomes = ['P1 Coop.\nP2 Coop.', 'P1 Coop.\nP2 Defect',
                'P1 Defect\nP2 Coop.', 'P1 Defect\nP2 Defect']
    p1_scores = [payoff('cooperate', 'cooperate')[0], payoff('cooperate', 'defect')[0],
                 payoff('defect', 'cooperate')[0], payoff('defect', 'defect')[0]]

    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(10, 6))
    # ... (rest of plotting logic is the same as before) ...
    bars = ax.bar(outcomes, p1_scores, color=['#4c72b0', '#dd8452', '#55a868', '#c44e52'])
    ax.set_title("Prisoner's Dilemma Base Payoffs (Player 1's Score)", pad=20, fontsize=14)
    ax.set_ylabel('Payoff Score', fontsize=12)
    ax.tick_params(axis='x', labelsize=9)
    ax.tick_params(axis='y', labelsize=10)
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height}', ha='center', va='bottom', fontsize=10, fontweight='bold')

    output_filename = 'pd_static_outcomes.png' # Renamed to avoid confusion
    output_path = data_dir / output_filename
    print(f"[Debug-StaticPlot] Full output path: {output_path}")

    try:
        plt.savefig(output_path, dpi=120, bbox_inches='tight')
        resolved_path = output_path.resolve()
        print(f"--- Static payoff visualization successfully saved to: {resolved_path} ---")
        if not resolved_path.is_file():
             print(f"[Warning] Save command executed, but file not found immediately at: {resolved_path}")
    except Exception as e:
        print(f"Error saving static plot to {output_path}: {e}")
    finally:
        plt.close(fig)
        print("[Debug-StaticPlot] Plot figure closed.")


def plot_manual_session(manual_history: ManualHistory):
    """
    Plots the cumulative scores from a manual play session.
    Saves plot to 'data/' subdirectory (root folder > data).
    Filename includes timestamp, e.g., manual_play_scores_YYYYMMDD_HHMMSS.png
    """
    if not manual_history:
        print("No history recorded for manual play session. Cannot generate plot.")
        return

    try:
        data_dir = get_data_dir()
        print(f"[Debug-ManualPlot] Using data directory: {data_dir}")
    except Exception as e:
        print(f"Could not get or create data directory for manual plot: {e}")
        return

    rounds = list(range(1, len(manual_history) + 1))
    p1_cumulative_score = 0
    p2_cumulative_score = 0
    p1_scores_over_time = [0] # Start at 0 before round 1
    p2_scores_over_time = [0] # Start at 0 before round 1

    for _, _, p1_score, p2_score in manual_history:
        p1_cumulative_score += p1_score
        p2_cumulative_score += p2_score
        p1_scores_over_time.append(p1_cumulative_score)
        p2_scores_over_time.append(p2_cumulative_score)

    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot cumulative scores - note rounds list needs a 0 prepended for plotting alignment
    rounds_for_plot = [0] + rounds
    ax.plot(rounds_for_plot, p1_scores_over_time, marker='o', linestyle='-', label='Player 1 Cumulative Score', color='#4c72b0')
    ax.plot(rounds_for_plot, p2_scores_over_time, marker='x', linestyle='--', label='Player 2 Cumulative Score', color='#dd8452')

    ax.set_title('Manual Play Session: Cumulative Scores Over Rounds', pad=20, fontsize=14)
    ax.set_xlabel('Round Number', fontsize=12)
    ax.set_ylabel('Cumulative Score', fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.tick_params(axis='both', labelsize=10)
    # Ensure x-axis starts at 0 or 1 and shows integer rounds
    ax.set_xticks(range(0, len(rounds) + 1))
    ax.set_xlim(left=0)

    # Generate timestamp for unique filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f'manual_play_scores_{timestamp}.png'
    output_path = data_dir / output_filename
    print(f"[Debug-ManualPlot] Full output path: {output_path}")

    try:
        plt.savefig(output_path, dpi=120, bbox_inches='tight')
        resolved_path = output_path.resolve()
        print(f"--- Manual play visualization successfully saved to: {resolved_path} ---")
        if not resolved_path.is_file():
            print(f"[Warning] Save command executed, but file not found immediately at: {resolved_path}")
    except Exception as e:
        print(f"Error saving manual play plot to {output_path}: {e}")
    finally:
        plt.close(fig)
        print("[Debug-ManualPlot] Plot figure closed.")


# --- Simulation Engine ---
def simulate_rounds(strategy1: StrategyFunction, strategy2: StrategyFunction, rounds: int = 100) -> History:
    """Simulates multiple rounds of the Prisoner's Dilemma between two strategies."""
    # ... (no changes needed in this function) ...
    history_p1_moves: PlayerHistory = []
    history_p2_moves: PlayerHistory = []
    full_history: History = []
    for _ in range(rounds):
        p1_move = strategy1(history_p1_moves, history_p2_moves)
        p2_move = strategy2(history_p2_moves, history_p1_moves)
        history_p1_moves.append(p1_move)
        history_p2_moves.append(p2_move)
        payoffs = payoff(p1_move, p2_move)
        full_history.append((p1_move, p2_move, payoffs))
    return full_history

def cooperation_rate(history: History) -> float:
    """Calculates the cooperation rate of Player 1 in the given history."""
    # ... (no changes needed in this function) ...
    if not history: return 0.0
    coop_count = sum(1 for round_data in history if round_data[0] == 'cooperate')
    return (coop_count / len(history)) * 100

# --- User Interaction ---
def run_tournament():
    """Runs a round-robin tournament between all defined strategies."""
    # ... (no changes needed in this function) ...
    strategies: Dict[str, StrategyFunction] = {
        'TitForTat': tit_for_tat, 'Random': random_strategy,
        'AlwaysCooperate': always_cooperate, 'AlwaysDefect': always_defect
    }
    print("\n=== Strategy Tournament Results ===")
    print("(Showing Player 1's Cooperation Rate [%] for each matchup)")
    results: Dict[str, float] = {}
    num_rounds = 50
    for name1, strat1 in strategies.items():
        for name2, strat2 in strategies.items():
            simulation_history = simulate_rounds(strat1, strat2, num_rounds)
            rate = cooperation_rate(simulation_history)
            matchup_key = f"{name1} (P1) vs {name2} (P2)"
            results[matchup_key] = rate
    for matchup, rate in sorted(results.items()):
        print(f"{matchup:<35}: {rate:>6.1f}%")

def manual_play():
    """Allows two human players to play the Prisoner's Dilemma via CLI and records history."""
    print("\n--- Manual Play ---")
    print("Enter 'cooperate' or 'defect'. Enter 'q' to quit session.")
    round_num = 1
    session_history: ManualHistory = [] # Initialize history list for this session

    while True:
        print(f"\n--- Round {round_num} ---")
        # Get Player 1 input
        while True:
            p1_input = input("Player 1, your move (cooperate/defect/q): ").lower().strip()
            if p1_input == 'q':
                 print("Ending manual play session.")
                 plot_manual_session(session_history) # Plot results before returning
                 return
            if p1_input in ['cooperate', 'defect']: break
            print("Invalid input. Please enter 'cooperate', 'defect', or 'q'.")

        # Get Player 2 input
        while True:
            p2_input = input("Player 2, your move (cooperate/defect/q): ").lower().strip()
            if p2_input == 'q':
                print("Ending manual play session.")
                plot_manual_session(session_history) # Plot results before returning
                return
            if p2_input in ['cooperate', 'defect']: break
            print("Invalid input. Please enter 'cooperate', 'defect', or 'q'.")

        # Calculate and display results
        p1_score, p2_score = payoff(p1_input, p2_input)
        print(f"\nOutcome: P1 chose '{p1_input}', P2 chose '{p2_input}'")
        print(f"  -> Payoffs: Player 1 = {p1_score}, Player 2 = {p2_score}")

        # Add results to session history
        session_history.append((p1_input, p2_input, p1_score, p2_score))
        round_num += 1

# --- Main Program Execution ---
if __name__ == "__main__":
    print(f"--- Running Script ---")
    print(f"[Info] Current Working Directory (at script start): {Path.cwd()}")
    try:
        # Plot the static payoff matrix illustration at the start
        plot_static_payoffs()
    except ImportError:
        print("Error: matplotlib is required for plotting. Please install it (`pip install matplotlib`).")
    except Exception as e:
        print(f"An unexpected error occurred during plot generation: {e}")

    # Main application loop for user interaction
    while True:
        print("\n=== Prisoner's Dilemma Simulator Menu ===")
        print("1. Play Manually (Human vs Human) -> Generates cumulative score plot on quit")
        print("2. Run Strategy Tournament (AI vs AI)")
        print("3. Exit")
        choice = input("Select option [1-3]: ").strip()

        if choice == '1':
            manual_play()
        elif choice == '2':
            run_tournament()
        elif choice == '3':
            print("Exiting Prisoner's Dilemma Simulator...")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

    print(f"--- Script Finished ---")
