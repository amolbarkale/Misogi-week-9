from langgraph.graph import StateGraph, END
import random
from typing import Dict, List, TypedDict
from IPython.display import Image, display

class AgentState(TypedDict):
    message: str
    number: List[int]
    counter: int

def greeting_node(state:AgentState)->AgentState:
    """Greeting Node which says hi to person"""

    state['message'] = f"Hi there"
    state['counter'] = 0

    return state

def random_node(state:AgentState)->AgentState:
    """Generates a random number form 0 to 10"""

    state['number'].append(random.randint(0,10))
    state['counter'] += 1

    return state

def should_continue(state:AgentState)->AgentState:
    """Function to decide what to do next"""

    if state['counter'] < 5:
        print("ENTERING LOOP, ", state["counter"])
        return "loop"
    else:
        return "exit"

# greeting -> random -> random -> random -> random -> random -> END

graph = StateGraph(AgentState)

graph.add_node("greeting", greeting_node)
graph.add_node("random", random_node)
graph.add_edge("greeting", "random")

graph.add_conditional_edges(
    "random", # source code
    should_continue, # action
    {
        "loop": "random", # self-loop back to the same loop
        "exit": END # end the graph
    }
)

graph.set_entry_point("greeting")

app = graph.compile()

display(Image(app.get_graph().draw_mermaid_png()))

app.invoke({"name": "Vaibhav", "number": [], "counter": -1})