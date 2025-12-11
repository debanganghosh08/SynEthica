# FILE: state.py
from typing import TypedDict, Optional, Dict, Any

class AgentState(TypedDict):
    # Data Paths
    raw_data_path: str
    synthetic_data_path: Optional[str]
    
    # Metrics
    initial_dir: float
    current_dir: float
    quality_score: float
    
    # Loop Control
    loop_count: int
    max_loops: int
    status: str  # "START", "GENERATING", "EVALUATING", "SUCCESS", "FAILED"
    
    # Strategy (The "Brain's" decision)
    current_strategy: Dict[str, Any]