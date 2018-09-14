import csv
import json
import os

count = 1


def dump_user_index_to_csv(file_name, csv_writer):
    global count
    with open(file_name, 'r', encoding='utf-8') as data_json:
        data_dict = json.loads(data_json.read())
        user_info = data_dict['user_info']
        user_info['index'] = count
        count = count + 1
        csv_writer.writerow(user_info)


def write_headers(csv_file):
    form_headers = [
        'index',
        'open_id',
        'game_name',
        'nick_name',
        'rank_desc',
        'service_name',
        'win_desc',
        'is_block',
        'is_guest',
        'is_join_ladder',
        'is_new',
        'ladder_score',
        'mmgc_is_block',
        'nobility_rank',
        'rank_lift',
        'rank_star',
        'winning_percentage',
        'zone_area_id',
        'profile_url',
        'head_img_url'
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


data_dir = '/Users/emrys/Documents/Moba/MobaUserIndex'
csv_name = '/Users/emrys/Documents/Moba/UserIndex.csv'


def start():
    with open(csv_name, 'a'):
        pass
    with open(csv_name, 'r+', encoding='utf-8', newline='') as csv_file:
        writer = write_headers(csv_file)
        for root, dirs, files in os.walk(data_dir):
            size = len(files)
            for file in files:
                file_path = os.path.join(data_dir, file)
                dump_user_index_to_csv(file_path, writer)
                csv_file.flush()
                print('''current is %s, total %s''' % (count, size))


start()
