import streamlit as st
from dotenv import load_dotenv

from core.assistant import run

load_dotenv()

symbol = "DMART"
st.title("Stock market research assistant")
st_text_input = st.text_input("Ask anything")

if st_text_input:
    result = run(symbol, st_text_input)
    st.write(result['answer'])
else:
    run(symbol, "")  # this is just to trigger the data refresh if needed
