# FILE: utils/helpers.py
import pandas as pd

def calculate_dir(df, protected_col='Gender', target_col='Loan_Approval', priv_group=1, unpriv_group=0):
    """Calculates Disparate Impact Ratio (DIR)."""
    # Safety check for empty frames
    if df.empty: return 0.0

    pos_outcome = df[target_col] == 1
    unpriv = df[protected_col] == unpriv_group
    priv = df[protected_col] == priv_group

    if df[unpriv].shape[0] == 0 or df[priv].shape[0] == 0:
        return 0.0

    rate_unpriv = df[unpriv & pos_outcome].shape[0] / df[unpriv].shape[0]
    rate_priv = df[priv & pos_outcome].shape[0] / df[priv].shape[0]

    if rate_priv == 0: return 0.0
    
    return rate_unpriv / rate_priv