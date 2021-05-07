from glob import glob
import json
import sys
import os


def main(path):
    os.chdir(path)
    for file in glob('./*.json'):
        f = open(file, 'r')
        data = json.load(f)
        f.close()
        shape = []
        for i in data['shapes']:
            if i['label'] != 'error':
                shape.append(i)
        data['shapes'] = shape
        data = json.dumps(data, indent=4)
        f = open(file, 'w')
        f.write(data)
        f.close()


if __name__ == "__main__":
    path = sys.argv[1]
    main(path)
