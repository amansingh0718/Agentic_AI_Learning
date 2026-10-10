import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage


Config = {"configurable" : {"thread_id" : "thread-1"}}


if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.text(message["content"])


user_input = st.chat_input("Ask anything!!!")

if user_input:
    st.session_state["message_history"].append({"role" : "user", "content" : user_input})
    with st.chat_message("user"):
        st.text(user_input)


    response = chatbot.invoke({"messages" : [HumanMessage(content = user_input)]}, config = Config)
    ai_response = response["messages"][-1].content


 
    with st.chat_message("assistant"):

        ai_response = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {"messages" : [HumanMessage(content = user_input)]},
                config = Config,
                stream_mode = "messages"
            )
        )
        
    st.session_state["message_history"].append({"role" : "assistant", "content" : ai_response})