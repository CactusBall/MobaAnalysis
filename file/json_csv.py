import csv
import json
import os

count = 1
size = 0


def json2csv(json_name, csv_name):
    global count
    with open(csv_name, 'a'):
        pass
    with open(csv_name, 'r+', newline='') as data_csv, open(json_name, 'r') as data_json:
        data_dict = json.loads(data_json.read())
        battle_list = data_dict['battle_info']['battle_list']
        form_headers = [
            'index',
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
        writer = csv.DictWriter(data_csv, fieldnames=form_headers)
        has_header = False
        try:
            has_header = csv.Sniffer().has_header(sample=data_csv.read())
        except Exception:
            pass
        if not has_header:
            writer.writeheader()
        # writer.writerows(battle_list)
        for battle in battle_list:
            if 'hero_icon' not in battle.keys():
                battle['hero_icon'] = ''
            if battle['game_type'] > 19:
                continue
            writer.writerow({
                'index': count,
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


i = 1
file_dir = '/Users/emrys/Documents/Moba/MobaBattleList'
csv_path = '/Users/emrys/Documents/BattleList.csv'
for root, dirs, files in os.walk(file_dir):
    size = len(files)
    for file in files:
        print('current is %d , total %d' % (i, size))
        i = i + 1
        json_file = os.path.join(file_dir, file)
        json2csv(json_file, csv_path)
