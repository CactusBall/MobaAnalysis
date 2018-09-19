import csv
import json
import os

import redis

redis = redis.Redis('0.0.0.0')

count = 1


def is_game_already_has(game_sql):
    return redis.hexists('_user_game', game_sql)


def dump_user_index_to_battle(csv_writer, json_name):
    global count
    json_path = os.path.join(file_dir, json_name)
    openid = json_name[8:-4]
    with open(json_path, 'r') as data_json:
        data_dict = json.loads(data_json.read())
        if 'battle_info' not in data_dict:
            return
        battle_list = data_dict['battle_info']['battle_list']

        for battle in battle_list:
            if 'hero_icon' not in battle.keys():
                battle['hero_icon'] = ''
            if battle['game_type'] > 19:
                continue
            if is_game_already_has(battle['game_seq']):
                print('Already has')
                continue
            if 'has_video' not in battle:
                battle['has_video'] = False
            csv_writer.writerow({
                'openid': openid,
                'game_seq': battle['game_seq'],
                'dt_event_time': battle['dt_event_time'],
                'is_victory': battle['is_victory'],
                'kill_cnt': battle['kill_cnt'],
                'dead_cnt': battle['dead_cnt'],
                'assist_cnt': battle['assist_cnt'],
                'kda': battle['kda'],
                'multi_camp_rank': battle['multi_camp_rank'],
                'is_mvp': battle['is_mvp'],
                'lose_mvp': battle['lose_mvp'],
                'is_friend': battle['is_friend'],
                'game_type': battle['game_type'],
                'hero_icon': battle['hero_icon'],
                'hero_position': battle['hero_position'],
                'honor_desc': battle['honor_desc'],
                'label_list': battle['label_list'],
                'has_video': battle['has_video'],
                'relay_svr_entity': battle['relay_svr_entity'],
                'game_svr_entity': battle['game_svr_entity']
            })
        count = count + 1


file_dir = '/Users/emrys/Documents/Moba/MobaUserIndex'
csv_path = '/Users/emrys/Documents/BattleList.csv'


def get_writer(csv_file):
    form_headers = [
        'openid',
        'game_seq',
        'dt_event_time',
        'is_victory',
        'kill_cnt',
        'dead_cnt',
        'assist_cnt',
        'kda',
        'multi_camp_rank',
        'is_mvp',
        'lose_mvp',
        'is_friend',
        'game_type',
        'hero_icon',
        'hero_position',
        'honor_desc',
        'label_list',
        'has_video',
        'relay_svr_entity',
        'game_svr_entity'
    ]
    writer = csv.DictWriter(csv_file, fieldnames=form_headers)
    return writer


def start():
    with open(csv_path, 'a', encoding='utf-8', newline='') as csv_file:
        writer = get_writer(csv_file)
        for root, dirs, files in os.walk(file_dir):
            size = len(files)
            for file in files:
                dump_user_index_to_battle(writer, file)
                csv_file.flush()
                print('''current is %s, total %s''' % (count, size))


start()
