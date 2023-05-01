import streamlit as st
from dotenv import load_dotenv
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

load_dotenv()


def main():
    # Load the language model
    llm = OpenAI(temperature=0.9)

    # Load the documents
    loader = TextLoader('./data/state_of_the_union.txt', encoding='utf-8')
    documents = loader.load()

    # Split the documents into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)

    # Create the document search as per open api standard
    embeddings = OpenAIEmbeddings()
    docsearch = Chroma.from_documents(texts, embeddings)

    retriver = docsearch.as_retriever(
        search_type="similarity", search_kwargs={"k": 2})

    chat_history = []
    qa = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriver)

    st.title("State of the Union QA")
    prompt = st.text_input("Ask anything about the state of the union")
    if prompt:
        result = qa({'question': prompt, 'chat_history': chat_history})
        st.write(result['answer'])


main()
