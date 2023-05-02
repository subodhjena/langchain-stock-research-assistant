
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import OpenAI
from core.database import get_db

from helpers.utilities import file_exists


def run(symbol: str, prompt: str = ""):
    """
    Run the app

    Input: stock_symbol (str)
    """

    data_path = f".data/{symbol}/data.txt"
    data_exists = not file_exists(data_path)

    db = get_db(symbol, data_exists)
    retriver = db.as_retriever(
        search_type="similarity", search_kwargs={"k": 2})

    llm = OpenAI(temperature=0.9)
    chat_history = []
    qa = ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=retriver, chain_type="stuff")

    result = qa({'question': prompt, 'chat_history': chat_history})
    return result
