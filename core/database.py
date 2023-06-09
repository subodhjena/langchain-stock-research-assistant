
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

from core.stock import load_data


def get_db(symbol: str, refresh: bool = False):
    embedding = OpenAIEmbeddings()
    collection_name = f"{symbol}_collection".lower()
    db = Chroma(persist_directory=".db", embedding_function=embedding,
                collection_name=collection_name)

    if refresh:
        load_data(symbol)

        loader = TextLoader(f".data/{symbol}/data.txt", encoding='utf-8')
        documents = loader.load()

        text_splitter = CharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=0,
        )
        texts = text_splitter.split_documents(documents)
        db.add_documents(texts)

    return db
