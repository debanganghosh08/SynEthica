# FILE: agents/reasoning_node.py
import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv(override=True)
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def reasoning_node(state):
    print(f"\n--- [NODE] Reasoning Agent (Loop {state['loop_count'] + 1}) ---")
    
    # Context
    loop_idx = state['loop_count']
    current_dir = state['current_dir']
    
    # --- PROMPT ENGINEERING ---
    if loop_idx == 0:
        # First Run
        prompt = f"""
        You are a Data Fairness Architect.
        Initial DIR is {state['initial_dir']:.2f}. We need to generate fair synthetic data.
        
        Task:
        1. Suggest a baseline sample count (e.g. 400).
        2. Suggest an INITIAL boost for the unprivileged group (Gender=0, Loan=1).
        
        Output JSON:
        {{
            "strategy_description": "text",
            "baseline_count": 400,
            "boost_count": 100,
            "boost_condition": {{"Gender": 0, "Loan_Approval": 1}}
        }}
        """
    else:
        # Feedback Loop (CRITICAL FIX HERE)
        prompt = f"""
        FEEDBACK LOOP TRIGGERED (Loop {loop_idx}).
        Previous Result: DIR = {current_dir:.2f}. Target > 0.80.
        Status: FAILED.
        
        Analysis:
        The previous boost was insufficient. The data is still biased (DIR is too low).
        We MUST increase the ratio of the unprivileged group (Gender=0, Loan=1).
        
        CRITICAL RULE:
        - You MUST provide a 'boost_condition' for Gender=0, Loan_Approval=1.
        - Do NOT set 'boost_condition' to null.
        - INCREASE 'boost_count' significantly (e.g. +150 from previous).
        
        Output JSON:
        {{
            "strategy_description": "Increasing boost to fix bias.",
            "baseline_count": 400,
            "boost_count": <INTEGER_HIGHER_THAN_BEFORE>,
            "boost_condition": {{"Gender": 0, "Loan_Approval": 1}}
        }}
        """

    # Call Gemini
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )
    
    try:
        strategy_raw = json.loads(response.text)
        strategy = strategy_raw[0] if isinstance(strategy_raw, list) else strategy_raw
        
        # --- ROBUSTNESS FIX: Force Condition if missing ---
        if not strategy.get('boost_condition'):
            print("(!) Gemini returned null condition. Overriding with Hardcoded Fix.")
            strategy['boost_condition'] = {"Gender": 0, "Loan_Approval": 1}
            # Ensure we actually have a boost count
            if strategy.get('boost_count', 0) < 50:
                strategy['boost_count'] = 250
        
        print(f"Strategy Decided: {strategy.get('strategy_description')}")
        print(f"Plan: Base={strategy.get('baseline_count')} | Boost={strategy.get('boost_count')} | Cond={strategy.get('boost_condition')}")
        
        return {"current_strategy": strategy}
        
    except Exception as e:
        print(f"Error parsing Gemini response: {e}")
        # Ultimate Fallback
        return {
            "current_strategy": {
                "baseline_count": 400, 
                "boost_count": 300 + (loop_idx * 100), # Increase with loops
                "boost_condition": {"Gender": 0, "Loan_Approval": 1}
            }
        }