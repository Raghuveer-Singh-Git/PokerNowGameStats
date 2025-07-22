import streamlit as st

st.set_page_config(layout="wide")
st.title("Hand Viewer")

if 'log_df' not in st.session_state:
    st.warning('Upload log file on Game Stats Page!')

else:
    st.session_state.hand_no = st.number_input("Insert a number", min_value=1, max_value=len(st.session_state.PnL)-1, value=1)
    st.session_state.hand_no = st.slider("",min_value=1, max_value=len(st.session_state.PnL)-1, value=st.session_state.hand_no,  disabled=False, label_visibility='hidden')
    st.write(f'### Hand Number: {st.session_state.hand_no}')

    log = st.session_state.log_df
    hand_df = log[log['hand'] == st.session_state.hand_no]

    st.dataframe(hand_df['entry'])
