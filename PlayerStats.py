import re

# Note: if u run twice, each run won is ocunted as 1 win

def get_player_stats(player_id, log_df):


    stats = {
                'raises' : {'pre':[], 'post':[]},
                'calls'  : {'pre':0,  'post':0},
                'bets'   : {'pre':[], 'post':[]},
                'checks' : {'pre':0,  'post':0},
                'folds'  : {'pre':0,  'post':0},
                'hands'  : set(),
                'won'    : {'hands':[], 'amount':[]}
            }
    

    last_flop = 0
    for index, row in log_df.iterrows():
        hand  = row['hand']
        entry = row['entry']

        if 'Flop:' == entry[:5]:
            last_flop = hand

        if player_id in entry:

            actions = ['folds', 'calls', 'checks']
            for action in actions:
                if action in entry:
                    if hand > last_flop:
                        stats[action]['pre'] += 1
                    else:
                        stats[action]['post'] += 1

                    stats['hands'].add(hand)
                    break
            
            if 'raises' in entry:
                amount = int(re.search(r'raises to (\d+)', entry).group(1))
                if hand > last_flop:
                    stats['raises']['pre'].append(amount)
                else:
                    stats['raises']['post'].append(amount)
                stats['hands'].add(hand)
            
            elif 'bets' in entry:
                amount = int(re.search(r'bets (\d+)', entry).group(1))
                if hand > last_flop:
                    stats['bets']['pre'].append(amount)
                else:
                    stats['bets']['post'].append(amount)
                stats['hands'].add(hand)
            
            elif 'collected' in row['entry']:
                amount = amount = int(re.search(r'collected (\d+)', entry).group(1))
                stats['won']['hands'].append(hand)
                stats['won']['amount'].append(amount)
                stats['hands'].add(hand)

    return stats




if __name__ == '__main__':
    import pandas as pd
    from PokerNowPnL import get_data
    log = pd.read_csv('poker_log.csv', index_col='order')
    log = log.sort_index(axis=0, ascending=True)
    PnL, stacks, buyins = get_data(log)
    stats = get_player_stats(PnL.columns[0], log)
    print(PnL.columns[0])
    print(stats)