import os
import shutil
import json
import sys

def main(path):

    # GET DIR NAME
    dir_list = []
    for root, _, file in os.walk(path):
        for f in file:
            d_name = f.replace('#', '/')
            d_name = os.path.join(root, d_name)
            d_name = os.path.dirname(d_name)
            if d_name not in dir_list:
                dir_list.append(d_name)
            else:
                continue

    for d in dir_list:
        if not os.path.isdir(d):
            os.mkdir(d)
            print(d)
        else:
            continue
    
    input()
       
    # MV FILE TO NEW DIR
    for root, _, file in os.walk(path):
        for f in file:
            f_name = os.path.join(root, f)
            d_name = f_name.replace('#', '/')
            if f_name == d_name:
                continue
            else:
                shutil.move(f_name, d_name)
                
    input()
    
    # MODIFY JSON FILE IMAGEPATH
    
    for root, _, file in os.walk(path):
        for f in file:
            if f.endswith('json'):
                file = os.path.join(root, f)
                j = open(file)
                data = json.load(j)
                j.close()
                with open(file, 'w') as j:
                    data['imagePath'] = f[:-5] + '.jpg'
                    j.write(json.dumps(data, indent=4))


path = sys.argv[1]
main(path)