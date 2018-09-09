import json
import os
import shutil

src_path = '/Users/emrys/Documents/Moba/MobaBattleDetail'
dest_dir = '/Users/emrys/Documents/BattleDetail'


def get_files(path):
    need_move_files = []
    for root, dirs, files in os.walk(path):
        return files
        # for file in files:
            # with open(os.path.join(path, file), 'r') as f:
            #     if file == '.DS_Store':
            #         continue
            #     j = json.loads(f.read())
            #     if 'appitem' in j:
            #         need_move_files.append(file)

    return need_move_files


def mv_files(files, dest_path):
    for file in files:
        file_p = os.path.join(src_path, file)
        dest_p = os.path.join(dest_path, file)
        shutil.move(file_p, dest_p)
        # shutil.move(file_p, )


def cp_file(file, dest_path):
    file_p = os.path.join(src_path, file)
    dest_p = os.path.join(dest_path, file)
    shutil.copy(file_p, dest_p)


files = get_files(src_path)
print(files)
cp_file(files[0], dest_dir)
# print(files)
# mv_files(files, dest_dir)
