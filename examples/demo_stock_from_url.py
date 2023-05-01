import streamlit as st
from dotenv import load_dotenv
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import SeleniumURLLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

load_dotenv()

urls = [
    "https://www.screener.in/company/ADANIENT/consolidated/",
]


def main():
    st.title("Q&A From URls")
    prompt = st.text_input("Ask anythin from the provided urls")

    llm = OpenAI(temperature=0.9)

    # Load Document
    loader = SeleniumURLLoader(urls=urls)
    data = loader.load()

    # Split the documents into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(data)

    # Create the document search as per open api standard
    embeddings = OpenAIEmbeddings()
    docsearch = Chroma.from_documents(texts, embeddings)

    retriver = docsearch.as_retriever(
        search_type="similarity", search_kwargs={"k": 2})

    chat_history = []
    qa = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriver)

    if prompt:
        result = qa({'question': prompt, 'chat_history': chat_history})
        st.write(result['answer'])


main()
