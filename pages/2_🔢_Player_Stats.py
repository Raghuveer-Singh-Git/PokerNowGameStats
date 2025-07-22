import streamlit as st
from PlayerStats import get_player_stats
import matplotlib.pyplot as plt
import re

st.set_page_config(layout="wide")
st.title("Player Stats")

if 'log_df' not in st.session_state:
    st.warning('Upload log file on Game Stats Page!')

else:
    players = st.session_state.PnL.columns
    player_id = st.selectbox('Select Player ID/Name:', players)
    
    st.write(f'### Showing Stats for "{player_id}"')

    # raises = []
    # calls = 0
    # checks = 0
    # folds = 0
    # hands = set()
    # won = 0

    # for index, row in st.session_state.log_df.iterrows():
    #     if player_id in row['entry']:
    #         if 'folds' in row['entry']:
    #             folds += 1
    #             hands.add(row['hand'])
            
    #         elif 'calls' in row['entry']:
    #             calls += 1
    #             hands.add(row['hand'])
            
    #         elif 'checks' in row['entry']:
    #             checks += 1
    #             hands.add(row['hand'])
            
    #         elif 'raises' in row['entry']:
    #             raises.append(int(re.search(r'raises to (\d+)', row['entry']).group(1)))
    #             hands.add(row['hand'])
            
    #         elif 'collected' in row['entry']:
    #             won += 1
    #             hands.add(row['hand'])


    # col1, col2, col3 = st.columns(3)

    # with col1:
    #     st.metric(label="Total Raises", value=len(raises))
    #     st.metric(label="Total Calls", value=calls)
    #     st.metric(label="Custom VPIP", value=f'{(len(raises)+calls)/(folds+checks+len(raises)+calls)//0.001/10}%')

    # with col2:
    #     st.metric(label="Total Checks", value=checks)
    #     st.metric(label="Total Folds", value=folds)
    #     st.metric(label="Ave Raise", value=(sum(raises)/len(raises))//1)

    # with col3:
    #     st.metric(label="Total Hands Played", value=len(hands))
    #     st.metric(label="Hands Won", value=won)
    #     st.metric(label="No Fold Loss", value=len(hands)-folds-won)


    stats = get_player_stats(player_id, st.session_state.log_df)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="PnL", value=st.session_state.PnL[player_id].iloc[-1])
        st.metric(label="VPIP", value=f"{(len(stats['raises']['pre'])+stats['calls']['pre'])/(len(stats['raises']['pre'])+stats['calls']['pre']+stats['folds']['pre']+stats['checks']['pre'])//0.01}%")
        st.metric(label='Wins*', value=len(stats['won']['hands']))
        st.metric(label='Total Raises', value=len(stats['raises']['pre']+stats['raises']['post']))
        st.metric(label='Total Calls', value=stats['calls']['pre']+stats['calls']['post'])
        st.metric(label='Total Checks', value=stats['checks']['pre']+stats['checks']['post'])
        st.metric(label='Total Folds', value=stats['folds']['pre']+stats['folds']['post'])


    with col2:
        st.metric(label="In For", value=st.session_state.buyins[player_id].max())
        st.metric(label="Hands Dealt", value=len(stats['hands']))
        st.metric(label='Ave Won', value=sum(stats['won']['amount'])/len(stats['won']['amount'])//1)
        st.metric(label='Pre-Flop Raises', value=len(stats['raises']['pre']))
        st.metric(label='Pre-Flop  Calls', value=stats['calls']['pre'])
        st.metric(label='Pre-Flop  Checks', value=stats['checks']['pre'])
        st.metric(label='Pre-Flop  Folds', value=stats['folds']['pre'])
        

    with col3:
        st.metric(label="Out For", value=st.session_state.buyins[player_id].max()+st.session_state.PnL[player_id].iloc[-1])
        st.metric(label="Bets", value=len(stats['bets']['post']))
        st.metric(label='Total Won', value=sum(stats['won']['amount']))
        st.metric(label='Post-Flop Raises', value=len(stats['raises']['post']))
        st.metric(label='Post-Flop  Calls', value=stats['calls']['post'])
        st.metric(label='Post-Flop  Checks', value=stats['checks']['post'])
        st.metric(label='Post-Flop  Folds', value=stats['folds']['post'])
        


    
    st.write(f'VPIP = (raises + calls) / (folds + checks + raises + calls) *preflop')
    st.write('Note: if u run twice, each run won is ocunted as 1 win')



    
    st.write('### Raises and Bets')
    st.bar_chart(stats['raises']['pre']+stats['raises']['post']+stats['bets']['post'])

    fig, (ax1, ax2) = plt.subplots(1,2)
    fig.set_size_inches(8,3)
    ax1.hist(stats['raises']['pre'], bins=20)
    ax2.hist(stats['raises']['post']+stats['bets']['post'], bins=20)
    ax1.set_title("Pre Flop Raises")
    ax2.set_title("Post Flop Raises + Bets")
    st.pyplot(fig)

    st.write('### Profit/Loss')
    st.line_chart(st.session_state.PnL[player_id])

    st.write('### Stack')
    st.line_chart(st.session_state.stacks[player_id])

    st.write('### Buyin')
    st.line_chart(st.session_state.buyins[player_id])

    if st.toggle("Show Row Stats"):
        st.json(stats)