#-*- coding:UTF-8 -*-
from src.widgets import constants

__author__ = 'icestar'


import resources
import skins
from cocos.sprite import Sprite

from button import *

def NewButton(name):
    skin = skins.Instance.get_skin(name)
    type = skin['type']

    if type != constants.UI_TYPE_BUTTON:
        raise "[creator] 类型错误"


    #name, text, x, y, width, height
    button = Button(skin['name'],
        skin['pos_x'],
        skin['pos_y'],
        skin['width'],
        skin['height']
    )

    #设置按钮状态图片
    for index, key in enumerate(skin['states']):
        image_name = skin['states'][key]

        img = resources.Instance.get_image(image_name)
        sp = Sprite(img, position=(img.width/2, img.height/2))
        button.set_item(key,sp)
    return button


