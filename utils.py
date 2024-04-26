import cv2   #导入调用opencv库

import numpy as np   #以np别名导入docopt

import os

from queue import Queue

queue = Queue()

class OpenFailed(Exception):
    pass

def get_file_list(file_path):
    """
    :param file_path: the file path where you want to get file
    :return: list, files sorted by name
    """
    dir_list = os.listdir(file_path)
    if not dir_list:
        return
    else:
        # 注意，这里使用lambda表达式，将文件按照最后修改时间顺序升序排列
        # os.path.getmtime() 函数是获取文件最后修改时间
        # os.path.getctime() 函数是获取文件最后创建时间
        # dir_list = sorted(dir_list, key=lambda x: os.path.getmtime(os.path.join(file_path, x)))
        dir_list = sorted(dir_list, key=lambda x: int(x[:-4]))  # 按名称排序
        # print(dir_list)
        return dir_list

fullbody_img_json={}
def wirte_fullbody_cache(file_path,start :int=None,end:int=None,data_add:int=None):
    i=0
    lun_num = end-start
    if data_add != None:
        i=data_add
        lun_num = lun_num+data_add
    dir_list = get_file_list(file_path)
    for filename in dir_list:
        if i > lun_num:
            break
        name = filename.split(".")
        if start != None:
            if int(name[0]) < start:
                continue
        if end != None:
            if int(name[0]) > end:
                continue
        file_name = os.path.join(file_path, filename)
        print(str(i)+":"+file_name)
        imagehead = cv2.imread(file_name)
        imagehead = cv2.cvtColor(imagehead, cv2.COLOR_BGR2RGB)
        fullbody_img_json[i]=imagehead
        i+=1

head_img_json={}
def write_head_cache(file_path,start :int=None,end:int=None,data_add:int=None):
    i=0
    lun_num = end-start
    if data_add != None:
        i=data_add
        lun_num = lun_num+data_add
    dir_list = get_file_list(file_path)
    for filename in dir_list:
        if i > lun_num:
            break
        name = filename.split(".")
        if start != None:
            if int(name[0]) < start:
                continue
        if end != None:
            if int(name[0]) > end:
                continue
        file_name = os.path.join(file_path, filename)
        print(str(i)+":"+file_name)
        imagehead = cv2.imread(file_name)
        imagehead = cv2.cvtColor(imagehead, cv2.COLOR_BGR2RGB)
        head_img_json[i]=imagehead
        i+=1

def load_head_cache_json_que(key,start:int=None):
    #发送消息启动数据队列，从第0位置开始
    # if start != None:
    #     queue.put(start)
    im = head_img_json[key]
    if im is None:
        raise OpenFailed
    #获取特征点
    # s = get_landmarks(im)
    cache_file='./cache/'+str(key)+'_data_cache.pkl'
    with open(cache_file, 'rb') as f:
        s=pickle.load(f)
    #返回图片和特征点组成的元组
    return im, s
def load_img_cache_json_que(key,start:int=None):
    #发送消息启动数据队列，从第0位置开始
    if start != None:
        queue.put(start)
    return fullbody_img_json[key]


if __name__=='__main__':

    wirte_fullbody_cache('./data/fullbody/img/',6500,6849,500)
    # wirte_fullbody_cache('./data/fullbody/img/',1500,1500+499,500)