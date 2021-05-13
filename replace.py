import os
import shutil
import sys


def main(tpath, dpath):

    tlist = []
    for root, _, file in os.walk(tpath):
        for f in file:
            if f.endswith('jpg'):
                t = os.path.join(root, f)
                tlist.append(t)

    dlist = []
    for i in tlist:
        d = i.replace(tpath, dpath)
        dlist.append(d)

    for z in zip(dlist, tlist):
        shutil.move(z[0], z[1])


tpath = sys.argv[1]
dpath = sys.argv[2]
main(tpath, dpath)
