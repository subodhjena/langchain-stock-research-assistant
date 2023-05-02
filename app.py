import streamlit as st

from core.assistant import run

symbol = "ADANIGREEN"
st.title("Stock market research assistant")
st_text_input = st.text_input("Ask anything")

if st_text_input:
    result = run(symbol, st_text_input)
    st.write(result['answer'])
