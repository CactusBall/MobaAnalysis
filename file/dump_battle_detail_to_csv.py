import csv
import json
import os

count = 1


def dump_battle_list_to_csv(json_name, csv_writer):
    global count
    json_path = os.path.join(file_dir, json_name)
    game_seq = json_name[8:-4]
    with open(json_path, 'r') as data_json:
        data_dict = json.loads(data_json.read())
        battle = data_dict['normal_battle_detail']
        if battle['is_blue']:
            if battle['is_victory']:
                victory_color = 'blue'
            else:
                victory_color = 'red'
        else:
            if battle['is_victory']:
                victory_color = 'red'
            else:
                victory_color = 'blue'
        csv_writer.writerow({
            'game_seq': game_seq,
            'victory_color': victory_color,
            'blue_kill_cnt': battle['blue_kill_cnt'],
            'red_kill_cnt': battle['red_kill_cnt'],
            'game_time': battle['game_time'],
            'game_type': battle['game_type']
        })
        count = count + 1


i = 1


def write_headers(csv_file):
    form_headers = [
        'game_seq',
        'victory_color',
        'blue_kill_cnt',
        'red_kill_cnt',
        'game_time',
        'game_type'
    ]
    writer = csv.DictWriter(csv_file, fieldnames=form_headers)
    has_header = False
    try:
        has_header = csv.Sniffer().has_header(sample=csv_file.read())
    except Exception:
        pass
    if not has_header:
        writer.writeheader()
    return writer


file_dir = '/Users/emrys/Documents/Moba/MobaBattleDetail'
csv_path = '/Users/emrys/Documents/BattleDetail.csv'


def start():
    with open(csv_path, 'a'):
        pass
    with open(csv_path, 'r+', encoding='utf-8', newline='') as csv_file:
        writer = write_headers(csv_file)
        for root, dirs, files in os.walk(file_dir):
            size = len(files)
            for file in files:
                dump_battle_list_to_csv(file, writer)
                csv_file.flush()
                print('''current is %s, total %s''' % (count, size))


# start()
s = 'profile_1536244790.txt'
print(s[8:-4])