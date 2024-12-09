import streamlit as st
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_groq import ChatGroq
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()  # This loads the environment variables

# Retrieve the API key
groq_api_key = os.getenv("GROQ_API_KEY")  # Make sure the environment variable is named correctly

os.environ["GROQ_API_KEY"] = groq_api_key

llm =ChatGroq(
    api_key=groq_api_key,
    model="mixtral-8x7b-32768",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)

wrapper_api = WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=200)
tools = WikipediaQueryRun(api_wrapper=wrapper_api)


class State(TypedDict):
  messages : Annotated[list,add_messages]  #append this message in the form of list

graph_builder = StateGraph(State)

#2: bind llm with the tools
llm_with_tools=llm.bind_tools(tools=[tools])


#3: define our chatbot
def chatbot(state:State):
  return {"messages":[llm_with_tools.invoke(state["messages"])]}

#entire flow of the execution
graph_builder.add_node("chatbot",chatbot)
graph_builder.add_edge(START,"chatbot") #start node is connected with chabot
tool_node=ToolNode(tools=[tools])
graph_builder.add_node("tools",tool_node)
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition  #bidirection itself with the chatbot
)
graph_builder.add_edge("tools","chatbot") #tools node is connected with chatbot
graph_builder.add_edge("chatbot",END) #end node is connected with tools

graph_built = graph_builder.compile() 


st.title("LANG-GRAPH-CHATBOT🤖📚")
st.subheader("Welcome! Ask me anything about Artificial Intelligence, and I'll find the best answer for you. 🚀")

st.write("Ask your question")

question = st.text_input("Ask your Question?")

submit = st.button("Submit") 

if submit:
    events = graph_built.stream(
    {"messages" : [("user" , question)]},stream_mode="values"
    )

    for event in events:
        response=event["messages"][-1].content
        st.write(response)
        
