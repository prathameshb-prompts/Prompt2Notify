
import os
import sqlite3
import requests
from typing import Annotated, TypedDict, List

from dotenv import load_dotenv
from IPython.display import Image, display
import gradio as gr

from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.sqlite import SqliteSaver

from langchain_openai import ChatOpenAI
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import Tool

load_dotenv(override=True)

# Define the Google search tool
serper = GoogleSerperAPIWrapper()
tool_search = Tool(
    name="search",
    func=serper.run,
    description="Useful for when you need more information from an online search."
)

# Define the push notifications tool
PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN")
PUSHOVER_USER = os.getenv("PUSHOVER_USER")
PUSHOVER_URL = "https://api.pushover.net/1/messages.json"

def send_push_notification(text: str) -> None:
    """Send a push notification to the user via Pushover API."""
    requests.post(
        PUSHOVER_URL,
        data={
            "token": PUSHOVER_TOKEN,
            "user": PUSHOVER_USER,
            "message": text,
        },
        timeout=10,
    )

tool_push = Tool(
    name="send_push_notification",
    func=send_push_notification,
    description="Useful for when you want to send a push notification."
)

# Combine tools
tools = [tool_search, tool_push]

# Build the conversational graph
DB_PATH = "memory.db"
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
sql_memory = SqliteSaver(conn)

class State(TypedDict):
    messages: Annotated[List, add_messages]

graph_builder = StateGraph(State)

llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State) -> dict:
    """Invoke the LLM with tools and return the updated messages."""
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools=tools))
graph_builder.add_conditional_edges("chatbot", tools_condition, "tools")
graph_builder.add_edge("tools", "chatbot")  # Return to chatbot after tool
graph_builder.add_edge(START, "chatbot")

graph = graph_builder.compile(checkpointer=sql_memory)
display(Image(graph.get_graph().draw_mermaid_png()))

CONFIG = {"configurable": {"thread_id": "3"}}

def chat(user_input: str, history):
    """Gradio chat interface callback."""
    result = graph.invoke({"messages": [{"role": "user", "content": user_input}]}, config=CONFIG)
    return result["messages"][-1].content

def main() -> None:
    """Main entry point for the application."""
    gr.ChatInterface(chat, type="messages").launch()

if __name__ == "__main__":
    main()
