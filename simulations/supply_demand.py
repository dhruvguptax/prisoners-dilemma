import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def plot_curves():
    project_root = Path(__file__).parent.parent
    data_dir = project_root / 'data'
    data_dir.mkdir(exist_ok=True)
    
    price = np.linspace(10, 100, 50)
    demand = 100 - price
    supply = price - 20
    
    plt.figure(figsize=(10, 6))
    plt.plot(price, demand, label='Demand', linewidth=2)
    plt.plot(price, supply, label='Supply', linewidth=2)
    plt.xlabel('Price')
    plt.ylabel('Quantity')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(data_dir / 'supply_demand.png', dpi=120)
    plt.close()

if __name__ == "__main__":
    plot_curves()
    print("Basic supply-demand curve generated")
