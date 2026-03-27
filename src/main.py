from langchain_core.messages import HumanMessage, AIMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0, max_tokens=None, max_retries=2)

def multiply(a: int,b: int) ->int:

    """
    Multiply a and b.

    Args:
        a: firt int
        b: second int
    """ 
    return a * b

llm_with_tools = llm.bind_tools([multiply])
tool_call = llm_with_tools.invoke([HumanMessage(content=f"What is 1 multiply by 1", name= "Gokul")])

from langgraph.graph import MessagesState
from langgraph.graph import StateGraph,START,END

# Created messagestate 
class MessagesState(MessagesState):
    pass

# Creating node's here

def tool_calling_llm(state: MessagesState):
    return  {"messages":[llm_with_tools.invoke(state["messages"])]}

builder= StateGraph(MessagesState)

builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_edge(START,"tool_calling_llm")
builder.add_edge("tool_calling_llm",END)
graph = builder.compile()

messages = graph.invoke({"messages": [HumanMessage(content="hellow", name= "gokul")]})
for m in messages['messages']:
    m.pretty_print()

messages = graph.invoke({"messages": [HumanMessage(content="what is 11 * 100", name= "gokul")]})
for m in messages['messages']:
    m.pretty_print()