import streamlit as st
from dotenv import load_dotenv

from core.assistant import run

load_dotenv()

symbol = ""

# Sidebar
st.sidebar.write("## Analyze any stock")
st.sidebar.write(
    "Enter a stock name and press enter (Currently only works with indian stocks)")
stock_input = st.sidebar.text_input("Enter a stock name")
if stock_input:
    symbol = stock_input.upper()

# Content Page
if symbol:
    st.title(symbol)
    st_text_input = st.text_input("Ask anything")

    if st_text_input:
        result = run(symbol, st_text_input)
        st.write(result['answer'])
    else:
        run(symbol, "")  # this is just to trigger the data refresh if needed
