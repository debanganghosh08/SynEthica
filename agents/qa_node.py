# FILE: agents/qa_node.py
import pandas as pd
from sdv.metadata import SingleTableMetadata
from sdv.evaluation.single_table import evaluate_quality
from utils.helpers import calculate_dir

def qa_node(state):
    print("\n--- [NODE] QA Agent: Evaluating ---")
    
    real_df = pd.read_csv(state['raw_data_path'])
    synth_df = pd.read_csv(state['synthetic_data_path'])
    
    # 1. Fairness
    new_dir = calculate_dir(synth_df)
    
    # 2. Quality
    metadata = SingleTableMetadata()
    metadata.detect_from_dataframe(real_df)
    quality_report = evaluate_quality(real_df, synth_df, metadata=metadata)
    quality_score = quality_report.get_score()
    
    print(f"Results -> DIR: {new_dir:.2f} | Quality: {quality_score:.2f}")
    
    # Update State
    return {
        "current_dir": new_dir,
        "quality_score": quality_score,
        "loop_count": state['loop_count'] + 1
    }

def should_continue(state):
    """Conditional Edge Logic"""
    if state['current_dir'] >= 0.8:
        return "end"
    
    if state['loop_count'] >= state['max_loops']:
        print("Max loops reached. Stopping.")
        return "end"
        
    return "loop"