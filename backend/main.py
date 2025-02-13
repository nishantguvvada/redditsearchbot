from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END # StateGraph object defines structure of our chatbot
from langgraph.graph.message import add_messages
from langchain_mistralai import ChatMistralAI
from langchain_anthropic import ChatAnthropic
from langchain_groq import ChatGroq
from langchain_community.tools.reddit_search.tool import RedditSearchRun, RedditSearchSchema
from langchain_community.utilities.reddit_search import RedditSearchAPIWrapper
from dotenv import load_dotenv
import os

load_dotenv()

class State(TypedDict):
    messages: Annotated[list, add_messages] # https://stackoverflow.com/questions/71898644/how-to-use-python-typing-annotated

graph_builder = StateGraph(State)

llm = ChatMistralAI(model="mistral-small-latest", api_key=os.getenv('MISTRAL_KEY'))
# llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv('GROQ_API_KEY'))
# llm = ChatAnthropic(model='claude-3-5-sonnet-latest', api_key=os.getenv('CLAUDE_KEY')')

def chatbot(state: State):
    llm_response = llm.invoke([
        {"role": "user", "content": f"Answer the questions: {state["messages"]}"}
    ])
    return {"message": llm_response.content}

graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")

graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()

search_tool = RedditSearchRun(
    api_wrapper=RedditSearchAPIWrapper(
        reddit_client_id=os.getenv('REDDIT_CLIENT_ID'),
        reddit_client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        reddit_user_agent=os.getenv('USER_AGENT'),
    )
)
search_params = RedditSearchSchema(
    query="beginner", sort="new", time_filter="week", subreddit="python", limit="3"
)
response = search_tool.run(tool_input=search_params.dict())
print("Reddit search response: ", response)



# def stream_graph_updates(user_input: str):
#     for message_chunk, metadata in graph.stream(
#     {"messages": user_input},
#     stream_mode="messages",
#     ):
#         if message_chunk.content:
#             print(message_chunk.content, end="|", flush=True)

# while True:
#     try:
#         user_input = input("User: ")
#         if user_input.lower() in ["quit", "exit", "q"]:
#             print("Goodbye!")
#             break
#         stream_graph_updates(user_input)
#     except:
#         user_input = "What do you know about LangGraph?"
#         print("User: " + user_input)
#         stream_graph_updates(user_input)
#         break