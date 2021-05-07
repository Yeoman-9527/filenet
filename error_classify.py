import os
import json
import shutil
import time


def main(t_path, d_path=None, d_path2=None):
    os.chdir(t_path)
    first = []  # all json file
    for file in os.listdir(t_path):
        if file.endswith('json'):
            first.append(file)
        else:
            pass

    second = []
    for file in first:
        with open(file, 'r') as f:
            data = json.load(f)
            for i in data['shapes']:
                if i['label'] == 'error':
                    second.append(file)
                    break
                else:
                    continue

    print(len(second))

    for j_file in second:
        if os.path.exists(j_file):
            path = os.path.join(d_path, j_file)
            shutil.move(j_file, path)
        else:
            print(f'{j_file} -> Error!')
            time.sleep(3)

    for i_file in second:
        img = i_file[:-5] + '.jpg'
        if os.path.exists(img):
            path = os.path.join(d_path, img)
            shutil.move(img, path)
        else:
            print(f'{i_file} -> Error!')


if __name__ == "__main__":
    t_path = "/home/ubuntu/Downloads/2021_04_28_6666"
    d_path = "/home/ubuntu/zh_classify"
    main(t_path, d_path)
