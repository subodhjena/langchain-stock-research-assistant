import streamlit as st
from dotenv import load_dotenv
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

load_dotenv()


def main():
    llm = OpenAI(temperature=0.9)

    loader = TextLoader('./data/state_of_the_union.txt', encoding='utf-8')
    # index = VectorstoreIndexCreator(
    #     text_splitter=CharacterTextSplitter(chunk_size=1000, chunk_overlap=0),
    #     embedding=OpenAIEmbeddings(),
    #     vectorstore_cls=Chroma
    # ).from_loaders([loader])
    index = VectorstoreIndexCreator().from_loaders([loader])

    st.title("State of the Union Bot")
    prompt = st.text_input("Ask anything about the state of the union")
    if (prompt):
        res = index.query(llm=llm, question=prompt, chain_type='stuff')
        st.write(res)


main()
