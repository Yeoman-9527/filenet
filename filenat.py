import os
from os.path import split
import cv2
import json
import shutil
import easygui as gui
from natsort import natsorted


class NeatenSlicer():

    def __init__(self) -> str:
        self.path = '~/'

    def repath(self):
        while True:
            code = gui.diropenbox(default=self.path)
            if code is None:  #
                break
            elif os.path.isdir(code):
                self.path = code
                break
            elif not os.path.isdir(code):
                continue

    def detect(self):
        # 检测文件名冲突
        d_list = []
        s_list = []
        for _, _, file in os.walk(self.path):
            for i in file:
                if not i in d_list:
                    d_list.append(i)
                else:
                    s_list.append(i)

        # logical judgement
        if s_list == []:
            centense = f'Without file impact \n File amount：{len(d_list)}'
            signal = gui.buttonbox(centense, choices=['< Back', 'X Quit'])
            return signal
        else:
            centense = f"Impact file name list: \n {s_list[:20]} \nImpact File amout : {len(s_list)} \nFile amount：{len(d_list) + len(s_list)}"
            signal = gui.buttonbox(centense, choices=['< Back', 'X Quit'])
            return signal

    def neaten(self):
        new_dir = ""
        for root, _, file in os.walk(self.path):
            if root == self.path:
                new_dir = gui.enterbox(' Enter new file name or path ',
                                       default=self.path + '_new')
                if not os.path.isdir(new_dir):
                    os.mkdir(new_dir)
                else:
                    pass
                gui.buttonbox(f'New path {new_dir}', choices=['Next >'])
            else:
                for i in file:
                    ipath = os.path.join(root, i)
                    fpath = os.path.join(new_dir, i)
                    shutil.move(ipath, fpath)

        signal = gui.buttonbox(f'Done !', choices=['< Back', 'X Quit'])
        return signal

    def slicer(self):
        param = gui.multenterbox(
            msg='Parameter Enter', title='File Slicer',
            fields=['Pices', 'File Prefix', 'Extract Path'],
            values=['', '', self.path])  # return int, name_prefix, path
        if param:
            group = 0
            count = 0
            group_dir = ""
            num = int(param[0])
            os.chdir(param[2])
            file_list = os.listdir('./')
            for file in natsorted(file_list):
                if count == 0:
                    # mkdir
                    group += 1
                    group_dir = param[1] + str(group)
                    os.mkdir(group_dir)
                    # mv file
                    shutil.move(file, group_dir)
                    count += 1
                else:
                    shutil.move(file, group_dir)
                    count += 1
                    while count == num:
                        count = 0
            signal = gui.buttonbox(f'File Group Amount : {group}', choices=[
                '< Back', 'X Quit'])
            return signal
        elif param is None:
            return '< Back'
        else:
            quit()

    def delable(self):
        delable = gui.enterbox(' Enter label ')
        l_dict = {}
        for root, _, file in os.walk(self.path):
            l_dict[root] = []
            for label in file:
                if label.endswith('json'):
                    l_dict[root].append(label)
            if l_dict[root]:
                continue
            else:
                del l_dict[root]

        for key, values in l_dict.items():
            for v in values:
                lname = os.path.join(key, v)
                f = open(lname, 'r')
                data = json.load(f)
                f.close
                # Detect
                shape = []
                for i in data['shapes']:
                    if i['label'] != delable:
                        shape.append(i)
                # Modify & Write
                data['shapes'] = shape
                with open(lname, 'w') as f:
                    f.write(json.dumps(data, indent=4))

        signal = gui.buttonbox(f'Done', choices=['< Back', 'X Quit'])
        return signal

    def iextract(self):
        singal = None
        while True:
            param = gui.multenterbox(msg='Parameter Enter', title='Image Extract',
                                     fields=['Video Format', 'Frame Num', 'Ouput Format'], values=['', '1', 'jpg'])
            # Verify Param
            if param:
                vformat = param[0]
                frame = int(param[1])
                iformat = param[2]
                if not iformat.startswith('.'):
                    iformat = '.' + iformat
            else:
                singal = '< Back'
                break

            # Started Get FilePath as a Dict
            vdict = {}
            for root, _, file in os.walk(self.path):
                vdict[root] = []
                for f in file:
                    if f.endswith(vformat):
                        vdict[root].append(f)
                if vdict[root] == []:
                    del vdict[root]

            # New Root Dir
            dirRoot = os.path.dirname(self.path)
            newName = 'IMG_' + self.path.split('/')[-1]
            newRoot = os.path.join(dirRoot, newName)
            if not os.path.exists(newRoot):
                os.makedirs(newRoot)

            # Extract Img
            for path, video in vdict.items():
                # OutPut Path
                outputPath = path.replace(self.path, newRoot)
                if not os.path.isdir(outputPath):
                    os.makedirs(outputPath)
                # Traverse Video File
                for v in video:
                    vpath = os.path.join(path, v)
                    times = 0
                    num = 0
                    camera = cv2.VideoCapture(vpath)
                    while True:
                        times += 1
                        ret, img = camera.read()
                        if not ret:
                            break
                        if times % frame == 0:
                            num += 1
                            if num < 10:
                                num2str = '00000' + str(num) + iformat
                            elif (num < 100):
                                num2str = '0000' + str(num) + iformat
                            elif (num < 1000):
                                num2str = '000' + str(num) + iformat
                            elif (num < 10000):
                                num2str = '00' + str(num) + iformat
                            elif (num < 100000):
                                num2str = '0' + str(num) + iformat
                            else:
                                num2str = str(num)
                            outputImg = os.path.join(outputPath, num2str)
                            cv2.imwrite(outputImg, img)
                            print(f'{outputImg} ---> 100%')
                    print(f'{v} ---> already extracted !')
                    camera.release()
            signal = gui.buttonbox(
                msg='All video files already transform images', title='Done', choices=['< back', 'X Quit'])
            break
        return singal

    def main(self):
        while True:
            code = ['1．Path Renew', '2. File Detect', '3. Extract File',
                    '4．File Slicer', '5.Delete Lable', '6.Image Extract', '7．Quit']
            num = gui.buttonbox(
                f"Current Path : {self.path} \n What you wanna do ?", choices=code)
            signal = None
            if num[0] == '1':
                signal = self.repath()
            elif num[0] == '2':
                signal = self.detect()
            elif num[0] == '3':
                signal = self.neaten()
            elif num[0] == '4':
                signal = self.slicer()
            elif num[0] == '5':
                signal = self.delable()
            elif num[0] == '6':
                signal = self.iextract()
            elif num[0] == '7':
                quit()
            # Function return param judgement
            if signal == '< Back':
                continue
            elif signal == None:
                continue
            elif signal == 'X Quit':
                quit()
            else:
                quit()


if __name__ == "__main__":
    run = NeatenSlicer()
    run.main()
