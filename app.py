import streamlit as st
from dotenv import load_dotenv
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

from core.stock import load_data
from helpers.utilities import file_exists

load_dotenv()


def run(symbol: str):
    """
    Run the app

    Input: stock_symbol (str)
    """

    data_path = f".data/{symbol}/data.txt"

    data_exist = file_exists(data_path)
    if not data_exist:
        load_data(symbol)

    # Load the documents
    loader = TextLoader(f".data/{symbol}/data.txt", encoding='utf-8')

    documents = loader.load()

    # Split the documents into chunks
    text_splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=0,
        length_function=len,
    )
    texts = text_splitter.split_documents(documents)

    # Create the document search as per open api standard
    embeddings = OpenAIEmbeddings()
    docsearch = Chroma.from_documents(texts, embeddings)

    retriver = docsearch.as_retriever(
        search_type="similarity", search_kwargs={"k": 2})

    llm = OpenAI(temperature=0.9)
    chat_history = []
    qa = ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=retriver, chain_type="stuff")

    st.title("Stock market research assistant")
    prompt = st.text_input("Ask anything about the stock")
    if prompt:
        result = qa({'question': prompt, 'chat_history': chat_history})
        st.write(result['answer'])


symbol = "ADANIGREEN"
run(symbol)
