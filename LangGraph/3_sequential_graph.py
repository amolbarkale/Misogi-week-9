from typing import TypedDict
from langgraph.graph import StateGraph
from IPython.display import Image, display

class AgnetState(TypedDict):
    name: str
    age: str
    final: str


def first_node(state: AgnetState)->AgnetState:
    """
    This is the first nore of our sequence
    """

    state["final"] = f"Hi {state['name']} !"

    return state

def second_node(state: AgnetState)-> AgnetState:
    """
    This is the second nore of our sequence
    """

    state['final'] = state["final"] + f"You are {state['age']} years old !"

    return state

graph = StateGraph(AgnetState)

graph.add_node("first_node", first_node)
graph.add_node("second_node", second_node)

graph.set_entry_point("first_node")
graph.add_edge("first_node", "second_node")
graph.set_finish_point("second_node")

app = graph.compile()

display(Image(app.get_graph().draw_mermaid_png))

result = app.invoke({"name": "Charlie", "age": 20})