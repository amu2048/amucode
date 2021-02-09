import random
import time
import os
from flask import request
#图片保存
def Saveimg(img):
    print("进入保存图片依赖函数")
    IMG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), r'static\niushenqi\images\fabu')
    fn = time.strftime("%Y%m%d%H%M%S", time.localtime()) + '_%d' % random.randint(0, 100) + '.png'
    print("生成图片名字"+fn)
    avata = img

    # new = compression_img(avata)
    pic_dir = os.path.join(IMG_PATH, fn)
    avata.save(pic_dir)
    print("保存图片成功")
    # folder = photosSet.url(hash_openid)
    img_dir = fn  # 返回图片名字  案后其他接口调用这个图片名字获取图片地址
    print("保存图片函数返回数据")
    return img_dir
def return_img_stream(img_local_path):
  """
  工具函数:
  获取本地图片流
  :param img_local_path:文件单张图片的本地绝对路径
  :return: 图片流
  """
  import base64
  img_stream = ''
  with open(img_local_path, 'r') as img_f:
    img_stream = img_f.read()
    img_stream = base64.b64encode(img_stream)
  return img_stream

