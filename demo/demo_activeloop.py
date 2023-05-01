import os
from typing import List

import requests
import streamlit as st
from dotenv import load_dotenv
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import PagedPDFSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import DeepLake

load_dotenv()

urls = ['https://s2.q4cdn.com/299287126/files/doc_financials/Q1_2018_-_8-K_Press_Release_FILED.pdf',
        'https://s2.q4cdn.com/299287126/files/doc_financials/Q2_2018_Earnings_Release.pdf',
        'https://s2.q4cdn.com/299287126/files/doc_news/archive/Q318-Amazon-Earnings-Press-Release.pdf',
        'https://s2.q4cdn.com/299287126/files/doc_news/archive/AMAZON.COM-ANNOUNCES-FOURTH-QUARTER-SALES-UP-20-TO-$72.4-BILLION.pdf',
        'https://s2.q4cdn.com/299287126/files/doc_financials/Q119_Amazon_Earnings_Press_Release_FINAL.pdf',
        'https://s2.q4cdn.com/299287126/files/doc_news/archive/Amazon-Q2-2019-Earnings-Release.pdf',
        'https://s2.q4cdn.com/299287126/files/doc_news/archive/Q3-2019-Amazon-Financial-Results.pdf',
        'https://s2.q4cdn.com/299287126/files/doc_news/archive/Amazon-Q4-2019-Earnings-Release.pdf',
        'https://s2.q4cdn.com/299287126/files/doc_financials/2020/Q1/AMZN-Q1-2020-Earnings-Release.pdf',
        'https://s2.q4cdn.com/299287126/files/doc_financials/2020/q2/Q2-2020-Amazon-Earnings-Release.pdf',
        'https://s2.q4cdn.com/299287126/files/doc_financials/2020/q4/Amazon-Q4-2020-Earnings-Release.pdf',
        'https://s2.q4cdn.com/299287126/files/doc_financials/2021/q1/Amazon-Q1-2021-Earnings-Release.pdf',
        'https://s2.q4cdn.com/299287126/files/doc_financials/2021/q2/AMZN-Q2-2021-Earnings-Release.pdf',
        'https://s2.q4cdn.com/299287126/files/doc_financials/2021/q3/Q3-2021-Earnings-Release.pdf',
        'https://s2.q4cdn.com/299287126/files/doc_financials/2021/q4/business_and_financial_update.pdf',
        'https://s2.q4cdn.com/299287126/files/doc_financials/2022/q1/Q1-2022-Amazon-Earnings-Release.pdf',
        'https://s2.q4cdn.com/299287126/files/doc_financials/2022/q2/Q2-2022-Amazon-Earnings-Release.pdf',
        'https://s2.q4cdn.com/299287126/files/doc_financials/2022/q3/Q3-2022-Amazon-Earnings-Release.pdf',
        'https://s2.q4cdn.com/299287126/files/doc_financials/2022/q4/Q4-2022-Amazon-Earnings-Release.pdf'
        ]


def load_reports(urls: List[str]) -> List[str]:
    """ Load data from urls """
    pages = []

    for url in urls:
        r = requests.get(url)
        path = url.split('/')[-1]

        with open(path, 'wb') as f:
            f.write(r.content)

        loader = PagedPDFSplitter(path)
        local_pages = loader.load_and_split()
        pages.extend(local_pages)

    return pages


def main():
    llm = OpenAI(temperature=0.9)
    pages = load_reports(urls)

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(pages)

    embeddings = OpenAIEmbeddings()

    db = DeepLake(dataset_path="hub://subodhjena/amazon_earnings",
                  embedding_function=embeddings, token=os.environ['ACTIVELOOP_TOKEN'])
    db.add_documents(texts)

    chat_history = []
    qa = ConversationalRetrievalChain.from_llm(llm=llm, retriever=db.as_retriever())

    st.title("Q&A From Amazon Earnings Calls")
    prompt = st.text_input("Ask anything related to Amazon's earnings")

    if prompt:
        result = qa({'question': prompt, 'chat_history': chat_history})
        st.write(result['answer'])


main()
