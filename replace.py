import os
import shutil


def main(tpath, dpath):

    tlist = []
    for root, _, file in os.walk(tpath):
        for f in file:
            if f.endswith('.jpg'):
                fname = os.path.join(root, f)
                tlist.append(fname)

    dlist = []
    for i in tlist:
        i = i.replace(tpath, dpath)
        dlist.append(i)

    print(tlist[:10], '\n', dlist[:10])

    for d in dlist:
        for t in tlist:
            shutil.move(t, d)
