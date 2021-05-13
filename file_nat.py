import os
import shutil
import easygui as gui
from natsort import natsorted
import json


class NeatenSlicer():

    def __init__(self) -> str:
        self.path = '~'
        self.re_path()

    def re_path(self):
        path = gui.diropenbox(default=self.path)
        if path:
            self.path = path
            return '< Back'
        elif path is None:
            return '< Back'
        else:
            print(path)

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
            'Parameter Enter', 'File Slicer',
            ('Pices', 'File Prefix', 'Default path'),
            ('', '', self.path))  # return int, name_prefix, path
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

    def del_label(self):
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

    def main(self):
        while True:
            choice = ['1. File Detect', '2. Extract File',
                      '3．File Slicer', '4．Path Renew', '5.Delete Lable', '6．Quit']
            num = gui.buttonbox(
                f"Current Path : {self.path} \n What you wanna do ?", choices=choice)
            signal = ''
            if num[0] == '1':
                signal = self.detect()
            elif num[0] == '2':
                signal = self.neaten()
            elif num[0] == '3':
                signal = self.slicer()
            elif num[0] == '4':
                signal = self.re_path()
            elif num[0] == '5':
                signal = self.del_label()
            elif num[0] == '6':
                quit()
            else:
                print(num[0])

            # Function return param judgement
            if signal == '< Back':
                continue
            elif signal == 'X Quit':
                quit()
            else:
                print(signal)


if __name__ == "__main__":
    run = NeatenSlicer()
    run.main()
