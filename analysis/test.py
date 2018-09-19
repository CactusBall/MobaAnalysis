import pandas as pd

csv = pd.read_csv('/Users/emrys/Documents/BattleList.csv')
openids = csv.get('openid')
games = csv.get('game_seq')
for o in openids:
    # print(o)
    if 'owanlsn0eMVK8aKyiWf0sYWxW5VU' == o:

        print('yes')

# print('owanlsoStRgq-MP1HX3ueUHLE73U' is 'owanlsoStRgq-MP1HX3ueUHLE73U')