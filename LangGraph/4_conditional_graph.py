from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from IPython .display import Image, display

class AgentState(TypedDict):
    number1: int
    operation: str
    number2: int
    finalNumber: int

def adder(state: AgentState)-> AgentState:
    "THis node adds the 2 numbers"

    state["finalNumber"] = state["number1"] + state["number2"]

    return state

def substractor(state: AgentState) ->AgentState:
    "This node substracts the 2 numbers"

    state["finalNumber"] = state["number1"] - state["number2"]

    return state

def decide_next_node(state:AgentState)-> AgentState:
    "This node will select the next node of the graph"

    if state["operation"] == "+":
        return "addition_operation"
    
    elif state["operation"] == "-":
        return "subtraction_operation"


graph = StateGraph(AgentState)

graph.add_node("add_node", adder)
graph.add_node("subtract_node", substractor)
graph.add_node("router", lambda state:state) # passthrough function

graph.add_edge(START, "router")

graph.add_conditional_edges(
    "router", # source
    decide_next_node, # path
    {
        # Edge: Node
        "addition_operation": "add_node",
        "subtraction_operation": "subtract_node"
    }
)

graph.add_edge("add_node", END)
graph.add_edge("subtract_node", END) 

app = graph.compile()

display(Image(app.get_graph().draw_mermaid_png()))
