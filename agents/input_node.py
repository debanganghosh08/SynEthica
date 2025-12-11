# FILE: agents/input_node.py
import pandas as pd
from utils.helpers import calculate_dir

def input_node(state):
    print("\n--- [NODE] Input Agent: Profiling Data ---")
    
    df = pd.read_csv(state['raw_data_path'])
    
    # Calculate Baseline Bias
    baseline_dir = calculate_dir(df)
    
    print(f"Data Loaded. Shape: {df.shape}")
    print(f"Baseline Disparate Impact Ratio (DIR): {baseline_dir:.2f}")
    
    return {
        "initial_dir": baseline_dir,
        "current_dir": baseline_dir,  # Start current same as initial
        "loop_count": 0,
        "status": "START"
    }