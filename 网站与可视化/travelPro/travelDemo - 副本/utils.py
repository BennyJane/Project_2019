import os
import hashlib
import time
from urllib.request import urlretrieve


# 生成32位id
import requests


def produce_id():
    '''生成32位id'''
    filePath = os.getcwd()
    # print(filePath)
    src = filePath + str(time.time())
    m = hashlib.md5()
    m.update(src.encode('utf8'))
    res = m.hexdigest()
    return res


def loadImg(url='', filePath=''):
    # 图片下载的三种方法: https://blog.csdn.net/jiahao1186/article/details/89471819
    if not url:
        url = 'http://www.pptbz.com/pptpic/UploadFiles_6909/201401/2014012906353538.jpg'
    if not filePath:
        filePath = './images/img1.jpg'
    urlretrieve(url, filePath)
    # 第二种方法
    # r = requests.get(url)
    # with open('./images/img2.jpg', 'wb') as f:
    #     f.write(r.content)
