import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

st.set_page_config(page_title="Chatbot - Vitor", page_icon="custom\selbettioficial_logo.jpg")

def get_response(query, chat_history):    
    template = '''
        you are a helpful assistant, and you will answer the user based on the chat history.
        chat history: {chat_history}
        user question: {query}
    '''
    prompt = ChatPromptTemplate.from_template(template)

    llm = ChatOpenAI(
        api_key=st.secrets["OPENAI_SECRET_KEY"],
        model="gpt-4o-mini",
        temperature=0.5
    )

    chain = prompt | llm | StrOutputParser()

    return chain.stream(
        {"query": query, "chat_history": chat_history}
    )

if "chat_history" not in st.session_state:
    st.markdown("<h2 style='text-align: center; margin-top: 270px'>Como posso ajudar?</h3>", unsafe_allow_html=True)
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)
    else:
        with st.chat_message("AI"):
            st.markdown(message.content)

if user_query := st.chat_input("Envie uma mensagem para o ChatBot"):
    with st.chat_message("Human"):
        st.markdown(user_query)

    st.session_state.chat_history.append(HumanMessage(user_query))

    with st.chat_message("AI"):
        response = st.write_stream(get_response(user_query, st.session_state.chat_history))
    st.session_state.chat_history.append(AIMessage(response))

