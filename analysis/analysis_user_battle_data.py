import json

import pandas as pd
import redis

redis = redis.Redis('0.0.0.0')


hash_map_name = '_user_game'


def dump_user_and_battle(csv_file):
    redis.delete(hash_map_name)
    csv_data = pd.read_csv(csv_file)
    openids = csv_data.get('openid')
    game_seqs = csv_data.get('game_seq')
    dt_event_times = csv_data.get('dt_event_time')
    is_friends = csv_data.get('is_friend')
    # print(openids)
    for (game_seq, openid, dt_event_time, is_friend) in zip(game_seqs, openids, dt_event_times, is_friends):
        value = {
            'openid': openid,
            'dt_event_time': dt_event_time,
            'is_friend': is_friend
        }
        j = json.dumps(value)
        redis.hset(hash_map_name, game_seq, j)


dump_user_and_battle('/Users/emrys/Documents/BattleList.csv')

# def dump_battle(csv_file):
#     redis.delete('_asdadasd')
#     csv_data = pd.read_csv(csv_file)
#     game_seqs = csv_data.get('game_seq')
#     for game_seq in game_seqs:
#         redis.hset('_asdadasd', game_seq, 1)
# dump_battle('/Users/emrys/Documents/BattleDetail.csv')