#coding=utf-8
__author__ = 'icestar'

import pyglet
from lxml import etree

import config


class ResourceManager:

    def __init__(self):
        self.images = {}    #图片资源

    def init(self):
        self.load_imagesets(config.imageset_file)

    def load_imagesets(self, file):
        doc = etree.parse(file)
        root = doc.getroot()
        for imageset in root.getchildren():
            image_name = imageset.get("Name")
            image_file = imageset.get("Imagefile")
            image_res = pyglet.resource.image(image_file)

            for image in imageset.getchildren():
                name = image.get("Name")
                xpos = int(image.get("XPos"))
                ypos = int(image.get("YPos"))
                width = int(image.get("Width"))
                height = int(image.get("Height"))
                self.images[image_name+'.' + name] = image_res.get_region(x = xpos, y = ypos, width = width, height = height)

    def get_image(self, name):
        if self.images.has_key(name):
            return self.images[name]
        else:
            return None



#资源管理器实例
Instance = ResourceManager()
Instance.init()



