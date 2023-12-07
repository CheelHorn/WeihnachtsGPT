import os
import streamlit as st
from langchain.agents.agent import AgentExecutor
from langchain.agents.openai_assistant import OpenAIAssistantRunnable

#Config 
OPENAI_API_KEY = "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"
ASSISTANT_ID = "asst_LkR1OSraGqfg4O63ctpFSIlT"
st.set_page_config(page_title="Nikolaus")

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

#define assistant
assistant = OpenAIAssistantRunnable(assistant_id=ASSISTANT_ID, as_agent=True)

#Streamlit Config
st.title("Nikolaus-Postbox 🎅💌")

agent_executor = AgentExecutor(agent=assistant, tools=[])  

# initialize message history  
if "messages" not in st.session_state:
    st.session_state["messages"] = []


# handle user input  
if user_input := st.chat_input(placeholder="Deine Nachricht mit deinen Weihnachtswünschen 🎁 an den Nikolaus!"):
    # extract thread_id from last message in message history
    thread_id = st.session_state.messages[-1]["id"] if st.session_state.messages else None
    # create context object with thread_id and message history
    context = {"thread_id": thread_id, "history": [msg["content"] for msg in st.session_state.messages[1:]]}
    # append user message to message history with thread_id
    st.session_state.messages.append({"role": "user", "content": user_input, "id": thread_id})
    with st.spinner("Der Weihnachtsmann denkt nach..."):  
        response = agent_executor.invoke({"content": user_input, "context": context})
        response_text = response["output"]
    # append AI message to message history with thread_id
    st.session_state.messages.append({"role": "assistant", "content": response_text, "id": thread_id})

# display message history  
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
