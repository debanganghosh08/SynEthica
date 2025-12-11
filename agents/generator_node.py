# FILE: agents/generator_node.py
import pandas as pd
from sdv.single_table import CTGANSynthesizer
from sdv.metadata import SingleTableMetadata
from sdv.sampling import Condition

def generator_node(state):
    print("\n--- [NODE] Generator Agent: Synthesizing Data ---")
    
    df = pd.read_csv(state['raw_data_path'])
    strategy = state['current_strategy']
    
    # Metadata
    metadata = SingleTableMetadata()
    metadata.detect_from_dataframe(df)
    
    # Train (low epochs for speed, increase for quality)
    synthesizer = CTGANSynthesizer(metadata)
    synthesizer.fit(df) # Add epochs=10 for faster testing if needed
    
    # 1. Baseline Sampling
    base_n = int(strategy.get('baseline_count', 400))
    print(f"Generating Baseline: {base_n} rows")
    synth_data = synthesizer.sample(num_rows=base_n)
    
    # 2. Boost Sampling (The Fix)
    boost_n = int(strategy.get('boost_count', 0))
    cond_raw = strategy.get('boost_condition')
    
    if boost_n > 0 and cond_raw:
        print(f"Generating Boost: {boost_n} rows for {cond_raw}")
        
        # Ensure values match the dataframe types (e.g. 0 vs 0.0)
        # This mapping is crucial for SDV
        condition = Condition(
            num_rows=boost_n,
            column_values=cond_raw
        )
        
        try:
            boost_data = synthesizer.sample_from_conditions(conditions=[condition])
            synth_data = pd.concat([synth_data, boost_data], ignore_index=True)
        except Exception as e:
            print(f"(!) Error during conditional sampling: {e}")
            print("Continuing with baseline only...")

    # Save
    output_path = "data/synthetic_output_current.csv"
    synth_data.to_csv(output_path, index=False)
    
    return {
        "synthetic_data_path": output_path,
        "status": "EVALUATING"
    }