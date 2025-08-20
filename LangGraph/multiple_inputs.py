from typing import TypedDict, List
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    values: List[int]
    name: str
    result: str

def process_values(state: AgentState) -> AgentState:
    "This function handles multiple difference iputs"

    state["result"] = f"Hi there {state['name']}! Your sum = {sum(state["values"])}"
    return state

graph = StateGraph(AgentState)



