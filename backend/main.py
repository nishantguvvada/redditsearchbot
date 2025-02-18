from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END # StateGraph object defines structure of our chatbot
from langgraph.graph.message import add_messages
from langchain_mistralai import ChatMistralAI
from langchain_anthropic import ChatAnthropic
from langchain_groq import ChatGroq
from langchain_community.tools.reddit_search.tool import RedditSearchRun, RedditSearchSchema
from langchain_community.utilities.reddit_search import RedditSearchAPIWrapper
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from dotenv import load_dotenv
import os
from basictoolnode import BasicToolNode

load_dotenv()

memory = MemorySaver()

class State(TypedDict):
    messages: Annotated[list, add_messages] # https://stackoverflow.com/questions/71898644/how-to-use-python-typing-annotated

graph_builder = StateGraph(State)

# TOOL - start

# open_search_tool = TavilySearchResults(max_results=2, api_key=os.getenv('TAVILY_API_KEY'))

search_tool = RedditSearchRun(
    api_wrapper=RedditSearchAPIWrapper(
        reddit_client_id=os.getenv('REDDIT_CLIENT_ID'),
        reddit_client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        reddit_user_agent=os.getenv('USER_AGENT'),
    ),
    name="reddit_search",
    description="A tool that searches for posts on Reddit about the brand. Useful when you need to know customer post information on a subreddit."
)

# reddit_search_params = RedditSearchSchema(
#         query="beginner", sort="new", time_filter="week", subreddit="cocacola", limit="3"
# )

tools = [search_tool]
# TOOL - end

# response = search_tool.run(tool_input=search_params.model_dump())
# print("Reddit search response: ", response)

llm = ChatMistralAI(model="mistral-small-latest", api_key=os.getenv('MISTRAL_KEY'))
# llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv('GROQ_API_KEY'))
# llm = ChatAnthropic(model='claude-3-5-sonnet-latest', api_key=os.getenv('CLAUDE_KEY')')
llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):
    # llm_response = llm.invoke([
    #     {"role": "user", "content": f"Answer the questions: {state["messages"]}"}
    # ])
    llm_response = llm_with_tools.invoke([
        {"role": "user", "content": f"Answer the questions: {state["messages"]}"}
    ])
    return {"messages": llm_response}

graph_builder.add_node("chatbot", chatbot) # Nodes represent units of work. They are typically regular python functions.

# graph_builder.add_edge(START, "chatbot")
graph_builder.set_entry_point("chatbot")

# graph = graph_builder.compile() # Creates a compiled graph

# tool_node = BasicToolNode(tools=tools) # Node that runs tools if they are called
tool_node = ToolNode(tools=tools) # Using prebuilt ToolNode
graph_builder.add_node("tools", tool_node) 

# Conditional edges route the control flow from one node to the next
# These functions receive current graph state and return a string indicating which node to call next
# The condition will route to tools if tool calls are present and END if not.

def route_tools(state: State):
    """
    Use in the conditional_edge to route to the ToolNode if the last message
    has tool calls. Otherwise, route to the end.
    """
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    
    return END

# graph_builder.add_conditional_edges(
#     "chatbot",
#     route_tools,
#     { "tools": "tools", END: END}
# )

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)

graph_builder.add_edge("tools", "chatbot") 

graph = graph_builder.compile(checkpointer=memory) # Checkpointing the State as the graph works through each node.

config = {"configurable": {"thread_id": "1"}}

def stream_graph_updates(user_input: str):
    # for message_chunk, metadata in graph.stream(
    # {"messages": user_input},
    # stream_mode="messages",
    # ):
    #     if message_chunk.content:
    #         print(message_chunk.content, end="|", flush=True)
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}, config):
        for value in event.values():
            print("Assistant:", value["messages"])

while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        stream_graph_updates(user_input)
    except:
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        stream_graph_updates(user_input)
        break