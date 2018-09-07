import json
import os
import shutil

src_path = '/Users/emrys/Documents/Moba/MobaBattleList'
dest_dir = '/Users/emrys/Documents/bak_list'


def get_files(path):
    need_move_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            with open(os.path.join(path, file), 'r') as f:
                if file == '.DS_Store':
                    continue
                j = json.loads(f.read())
                if 'appitem' in j:
                    need_move_files.append(file)

    return need_move_files


def mv_files(files, dest_path):
    for file in files:
        file_p = os.path.join(src_path, file)
        dest_p = os.path.join(dest_path, file)
        shutil.move(file_p, dest_p)
        # shutil.move(file_p, )


files = get_files(src_path)
print(files)
# mv_files(files, dest_dir)
