import streamlit as st
import pandas as pd
from PokerNowPnL import get_data

st.set_page_config(layout="wide")
st.title("Game Overview")

uploaded_file = st.file_uploader("Choose a PokerNow Game Log File", type="csv")

if uploaded_file is not None:
    log = pd.read_csv(uploaded_file, index_col='order')
    log = log.sort_index(axis=0, ascending=True)
    PnL, stacks, buyins = get_data(log)

    st.session_state.log_df = log
    st.session_state.PnL = PnL
    st.session_state.stacks = stacks
    st.session_state.buyins = buyins

if 'log_df' in st.session_state:
    
    st.write('### Profit/Loss')
    st.line_chart(st.session_state.PnL)

    st.write('### Stacks')
    st.line_chart(st.session_state.stacks)

    st.write('### Buyins')
    st.line_chart(st.session_state.buyins)