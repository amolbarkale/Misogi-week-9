from langgraph.graph import StateGraph
from IPython.display import Image, display
from typing import TypedDict, List
from math import prod

class AgentState(TypedDict):
    values: List[int]
    name: str
    result: str
    operation: str

def process_values(state: AgentState) -> AgentState:
    "This function handles multiple difference iputs"
    # Do not try to update the 'result' state here as langgrapg will assign its initial value as unknown. 
    # In below case it is working because we are just assigning the value to the 'result'
    if (state["operation"] == "add"):
        state["result"] = f"Hi there {state['name']}! Your sum = {sum(state["values"])}"
    else:
        state["result"] = f"Hi there {state['name']}! Your sum = {prod(state["values"])}"

    return state

graph = StateGraph(AgentState)

graph.add_node("processor", process_values)
graph.set_entry_point("processor")
graph.set_finish_point("processor")

app = graph.compile() # Compiling the graph

display(Image(app.get_graph().draw_mermaid_png()))

answers = app.invoke({"values": [1,2,3,4,], "name": "Steve", "operation": "multiply"})
print('answers:', answers["result"])



