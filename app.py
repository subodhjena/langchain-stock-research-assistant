import asyncio
import os
import shutil

import streamlit as st
from dotenv import load_dotenv
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import SeleniumURLLoader, TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.vectorstores import Chroma

from web_driver import get_all_links, process_urls_async

load_dotenv()


def get_stock_urls(symbol: str) -> list[str]:
    """
    Get stock urls

    Input: stock_symbol (str)
    Output: stock_urls (list[str])
    """

    url = f'https://www.screener.in/company/{symbol}/consolidated/'
    return [url]


def get_stock_news_urls(symbol: str) -> list[str]:
    """
    Get stock news urls

    Input: stock_symbol (str)
    Output: stock_news_urls (list[str])
    """
    urls = []

    search_queries = [
        f"moneycontrol {symbol} news",
    ]
    search_results_count = 10
    search = GoogleSearchAPIWrapper()

    for query in search_queries:
        results = search.results(query, search_results_count)
        for result in results:
            link = result['link']

            # if link contains news in it, then it's a news page, get all the links from that page
            if "news" in link:
                news_links = get_all_links(link)
                urls.extend(news_links)
            else:
                urls.append(link)

    # only return unique urls
    return list(set(urls))


def crawl(urls: list[str]):
    """
    Get data from the urls

    Input: urls (list[str])
    Output: documents (list[Document ])
    """

    loader = SeleniumURLLoader(urls=urls, browser="firefox",)
    documents = loader.load()

    return documents


def get_data(symbol: str) -> str:
    """
    Get stock data, If the current time is less than 30 minuts by the time when the data was fetched last time
    load fresh data, otherwise don't load any data

    Input: stock_symbol (str)
    Output: the data folder path (str)
    """

    # Get data source urls
    stock_urls = get_stock_urls(symbol)
    stock_news_urls = get_stock_news_urls(symbol)
    urls = stock_urls + stock_news_urls

    # Get data from the urls
    documents = crawl(urls)

    return documents


def load_data(symbol: str):
    stock_urls = get_stock_urls(symbol)
    stock_news_urls = get_stock_news_urls(symbol)
    urls = stock_urls + stock_news_urls

    print(urls)

    folder_path = f".data/{symbol}"
    # recreate the folder
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.makedirs(folder_path)

    elements_to_ignore = ["nav", "header", "footer"]
    classes_to_ignore = ["company-nav"]
    ids_to_ignore = ["documents"]

    asyncio.run(process_urls_async(urls, folder_path,
                elements_to_ignore, classes_to_ignore, ids_to_ignore))


def run(symbol: str):
    """
    Run the app

    Input: stock_symbol (str)
    """

    # Load the language model
    llm = OpenAI(temperature=0.9)

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

    chat_history = []
    qa = ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=retriver, chain_type="stuff")

    st.title("Stock market research assistant")
    prompt = st.text_input("Ask anything about the stock")
    if prompt:
        result = qa({'question': prompt, 'chat_history': chat_history})
        st.write(result['answer'])


symbol = "TCS"
run(symbol)
