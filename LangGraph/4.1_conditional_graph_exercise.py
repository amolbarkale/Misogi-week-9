from typing import List, TypedDict
from langgraph.graph import StateGraph, START, END
from IPython.display import display, Image

class AgentState(TypedDict):
    number1: int
    number2:  int
    number3: int
    number4: int
    operation1: str
    operation2: str
    finalNumber1: int
    finalNumber2: int

def adder1(state: AgentState)-> AgentState:
    """This node adds the number1 and number2"""

    state["finalNumber1"] = state["number1"] + state["number2"]

    return state

def subtractor1(state: AgentState)-> AgentState:
    """This node subtracts number 1 and number 2"""

    state["finalNumber1"] = state["number1"] - state["number2"]
    return state

def decide_next_node_one(state: AgentState)-> AgentState:
    """This node will selects the next node of the graph"""
    
    if state["operation1"] == "+":
        return "add_operation"
    
    elif state["operation1"] == "-":
        return "subtract_operation"

def adder2(state: AgentState)-> AgentState:
    """This node will add number3 and number4"""

    state["finalNumber2"] = state["number3"] + state["number4"]

    return state

def subtractor2(state: AgentState)-> AgentState:
    """This node will subtract number3 and number4"""

    state["finalNumber2"] = state["number3"] - state["number4"]
    
    return state

def decide_next_node_two(state: AgentState)-> AgentState:
    """This node will selects the next node of the graph"""
    
    if state["operation2"] == "+":
        return "add_operation_two"
    
    elif state["operation2"] == "-":
        return "subtract_operation"

# Build the graph
graph = StateGraph(AgentState)

# first stage
graph.add_node("add_node", adder1)
graph.add_node("subtract_node", subtractor1)
graph.add_node("router", lambda state:state)

graph.add_edge(START, "router")

graph.add_conditional_edges(
    "router",
    decide_next_node_one,
    {
        # edge: node
        "add_operation": "add_node",
        "subtract_operation": "subtract_node"
    }
)

# merge to router2
graph.add_node("router2", lambda state:state)
graph.add_edge("add_node", "router2")
graph.add_edge("subtract_node", "router2")

#second stage
graph.add_node("add_node2", adder2)
graph.add_node("subtract_node2", subtractor2)

graph.add_conditional_edges(
    "router2",
    decide_next_node_two,
    # edge: node
    {
        "add_operation_two": "add_node2",
        "subtract_operation_two": "subtract_node2"
    }
)

graph.add_edge("add_node2", END)
graph.add_edge("subtract_node2", END)


app = graph.compile()

display(Image(app.get_graph().draw_mermaid_png()))

#__________________________________________________

initial_state: AgentState = {
    "number1": 10, "number2": 5,
    "number3": 7,  "number4": 2,
    "operation1": "-", "operation2": "+",
    "finalNumber1": 0, "finalNumber2": 0,
}
result = app.invoke(initial_state)

print(result["finalNumber1"], result["finalNumber2"])