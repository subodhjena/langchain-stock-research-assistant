import streamlit as st
from dotenv import load_dotenv
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.document_loaders import PlaywrightURLLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

load_dotenv()

stock_symbol = "AMARAJABAT"
stock = "Amara Raja Batteries Ltd"

urls = [
    "https://www.moneycontrol.com/india/stockpricequote/auto-ancillaries/amararajabatteries/ARB",
    "https://www.fortuneindia.com/long-reads/eye-on-evs-amara-raja-to-reinvent-itself/112252",
    "https://www.moneycontrol.com/news/business/stocks/amara-raja-batteries-why-analysts-expect-20-40-upside-despite-challenges-10249511.html",
]

def main():
    st.title("Stock Market Chatbot")
    prompt = st.text_input("Ask anything")

    llm = OpenAI(temperature=0.9)

    loader = PlaywrightURLLoader(urls=urls, remove_selectors=[
                                 "nav", "sub-nav" "header", "footer", "footer_container", "nw_breadcrumb", "button", "a", "chart", "documents"])
    data = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(data)

    embeddings = OpenAIEmbeddings()
    docsearch = Chroma.from_documents(texts, embeddings)

    retriver = docsearch.as_retriever(
        search_type="similarity", search_kwargs={"k": 2})

    memory = ConversationBufferMemory(
        memory_key="chat_history", return_messages=True)

    qa = ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=retriver, memory=memory)

    if prompt:
        result = qa({'question': prompt})
        st.write(result['answer'])


main()
