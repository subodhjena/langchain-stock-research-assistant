import streamlit as st
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.utilities import WikipediaAPIWrapper

load_dotenv()


# Prompt Template
title_template = PromptTemplate(
    input_variables=['topic'],
    template='Write a story title about {topic}',
)

script_template = PromptTemplate(
    input_variables=['title', 'wikipedia_research'],
    template='Write a script for the story title about {title}, while researching {wikipedia_research}',
)

title_memory = ConversationBufferMemory(
    input_key='topic', memory_key='chat_history')
script_memory = ConversationBufferMemory(
    input_key='title', memory_key='chat_history')

wiki = WikipediaAPIWrapper()


# LLMs
llm = OpenAI(temperature=0.9)
title_chain = LLMChain(llm=llm, prompt=title_template,
                       verbose=True, output_key='title', memory=title_memory)
script_chain = LLMChain(llm=llm, prompt=script_template,
                        verbose=True, output_key='script', memory=script_memory)


# App
st.title("Langchain Demo")
prompt = st.text_input("Prompt")
if prompt:
    title = title_chain.run(prompt)
    wiki_research = wiki.run(title)
    script = script_chain.run(title=title, wikipedia_research=wiki_research)

    st.header(title)
    st.write(script)

    with st.expander('Title History'):
        st.info(title_memory.buffer)

    with st.expander('Script History'):
        st.info(script_memory.buffer)

    with st.expander('Wikipedia Research'):
        st.info(wiki_research)
