# FILE: main.py
from langgraph.graph import StateGraph, END
from state import AgentState
from agents.input_node import input_node
from agents.reasoning_node import reasoning_node
from agents.generator_node import generator_node
from agents.qa_node import qa_node, should_continue

# 1. Initialize Graph
workflow = StateGraph(AgentState)

# 2. Add Nodes
workflow.add_node("Input", input_node)
workflow.add_node("Reasoning", reasoning_node)
workflow.add_node("Generator", generator_node)
workflow.add_node("QA", qa_node)

# 3. Define Edges
workflow.set_entry_point("Input")
workflow.add_edge("Input", "Reasoning")
workflow.add_edge("Reasoning", "Generator")
workflow.add_edge("Generator", "QA")

# 4. Conditional Loop
workflow.add_conditional_edges(
    "QA",
    should_continue,
    {
        "loop": "Reasoning",
        "end": END
    }
)

app = workflow.compile()

print("--- Starting SynEthica Agentic System ---")

# Initial Config
initial_state = {
    "raw_data_path": "data/raw_data.csv",
    "loop_count": 0,
    "max_loops": 5,  # Increased to 5
    "current_dir": 0.0,
    "initial_dir": 0.0,
    "quality_score": 0.0,
    "current_strategy": {}
}

# Run
final_state = app.invoke(initial_state)

print("\n\n--- WORKFLOW FINISHED ---")
print(f"Final Status: {final_state.get('status', 'Unknown')}")
print(f"Final Fairness (DIR): {final_state['current_dir']:.2f}")
print(f"Final Quality: {final_state['quality_score']:.2f}")
print(f"Total Loops: {final_state['loop_count']}")