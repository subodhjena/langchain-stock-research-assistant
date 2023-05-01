import streamlit as st
from dotenv import load_dotenv
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.memory import ConversationBufferMemory


load_dotenv()


def main():
    # Load the language model
    llm = OpenAI(temperature=0.9)

    # Load the documents
    loader = TextLoader('./data/amararaja.txt', encoding='utf-8')
    data = loader.load()

    print(data[0].page_content)

    # Split the documents into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(data)

    # Create the document search as per open api standard
    embeddings = OpenAIEmbeddings()
    docsearch = Chroma.from_documents(texts, embeddings)

    retriver = docsearch.as_retriever(
        search_type="similarity", search_kwargs={"k": 2})

    memory = ConversationBufferMemory(
        memory_key="chat_history", return_messages=True)

    qa = ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=retriver, memory=memory)

    st.title("Stock Market Chatbot")
    prompt = st.text_input("Ask anything")

    if prompt:
        result = qa({'question': prompt})
        st.write(result['answer'])


main()
