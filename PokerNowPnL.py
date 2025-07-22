import pandas as pd
import re
import matplotlib.pyplot as plt


def get_data(log):

    # Add row for hand number
    hand_no = 0
    curr_hand_no = []
    for entry in log['entry']:
        if 'starting hand' in entry:
            hand_no += 1
        curr_hand_no.append(hand_no)

    log['hand'] = curr_hand_no


    # Helper to extract stack ballances
    def extract_player_stacks(player_stacks_string):
        pattern = r'"([^"]*)" \((\d+)\)'
        matches = re.findall(pattern, player_stacks_string)

        stacks = []
        for match in matches:
            player = match[0] # The first captured group is the player name
            balance = int(match[1]) # The third captured group is the balance, converted to integer
            stacks.append({
                'player': player,
                'balance': balance
            })
        return stacks


    # Get player names
    def extract_player_names(string):
        return re.findall(r'"([^"]*)"', string)

    players = set()

    for entry in log['entry']:
        data = set(extract_player_names(entry))
        players = players.union(data)

    players = tuple(players)

    stacks = pd.DataFrame(columns=players, index=[i for i in range(hand_no+1)]) # 'Player stacks:'
    buyins = pd.DataFrame(columns=players, index=[i for i in range(hand_no+1)]) # 'updated' or 'approved'


    for index, row in log.iterrows():
        if 'Player stacks:' in row['entry']:
            hand_stacks = extract_player_stacks(row['entry'])
            for x in hand_stacks:
                stacks.at[row['hand'], x['player']] = x['balance']
        
        if 'quits the game with a stack of' in row['entry']:
            player = extract_player_names(row['entry'])[0]
            amount = int(row['entry'].split()[-1][:-1])
            # print(player, amount)
            # print(row['entry'])
            stacks.at[row['hand'], player] = 0
            buyins.at[row['hand'], player] = -amount

        if 'approved' in row['entry']:
            player = extract_player_names(row['entry'])[0]
            amount = int(row['entry'].split()[-1][:-1])
            buyins.at[row['hand'], player] = amount
        
        if 'updated' in row['entry']:
            player = extract_player_names(row['entry'])[0]
            og_amount  = int(row['entry'].split()[-3])
            to_amount = int(row['entry'].split()[-1][:-1])

            buyins.at[row['hand'], player] = to_amount - og_amount


    # Prefix sum buyins
    for idx in range(1, hand_no+1):
        for player in players:
            if pd.isna(buyins.at[idx, player]):
                buyins.at[idx, player] = buyins.at[idx-1, player]
            elif pd.isna(buyins.at[idx-1, player]):
                pass
            else:
                buyins.at[idx, player] += buyins.at[idx-1, player]


    # resolve NaNs in stacks
    # for idx in range(hand_no,1,-1):
    #     for player in players:
    #         if pd.isna(stacks.at[idx-1, player]):
    #             stacks.at[idx-1, player] = stacks.at[idx, player]
    for idx in range(1, hand_no+1):
        for player in players:
            if pd.isna(stacks.at[idx, player]):
                stacks.at[idx, player] = stacks.at[idx-1, player]

    PnL = stacks - buyins

    return PnL, stacks, buyins


if __name__ == "__main__":
    log = pd.read_csv('poker_log2.csv', index_col='order')
    log = log.sort_index(axis=0, ascending=True)
    PnL, stacks, buyins = get_data(log)
    PnL.plot(grid=True, title='Profit/Loss')
    stacks.plot(grid=True, title='Stacks')
    buyins.plot(title='Buyins')
    print(buyins.to_string())
    plt.show()