import cv2
import os 
import glob

webms = glob.glob('*.webm')

for video in webms:
    print(video)
    sourceVideo = video.split('.webm')[0]
    print(sourceVideo)
    currentPath = os.getcwd()
    video_path = os.path.join(currentPath, video)
    
    times = 0
    num = 0
    
    # 视频帧率
    videoFrequency = 1
    # 输出图片到当前目录vedio文件下
    outputPath = os.path.join(currentPath, sourceVideo)
    if not os.path.isdir(outputPath):
        os.makedirs(outputPath)
    camera = cv2.VideoCapture(video_path)
    input()
    while True:
        times += 1
       
        res, img = camera.read()
        if not res:
            print('Not res and img')
            break
        if times % videoFrequency == 0:
            num += 1
            if num < 10:
                num2str = '00000' + str(num)
            elif (num < 100):
                num2str = '0000' + str(num)
            elif (num < 1000):
                num2str = '000' + str(num)
            elif (num < 10000):
                num2str = '00' + str(num)
            elif (num < 100000):
                num2str = '0' + str(num)
            else:
                num2str = str(num)
            cv2.imwrite(outputPath + '/' + num2str +'.jpg', img)  # sourceFileName + '_' +
            print (outputPath + num2str + '.jpg')
    print(video + '图片提取结束')
    camera.release()

        
