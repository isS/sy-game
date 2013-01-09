#coding=utf-8
__author__ = 'icestar'

import pyglet
from cocos.layer import Layer
from cocos.sprite import Sprite
from cocos.scene import Scene

from widgets.container import Container
from widgets import creator

import resconfig

class Background(Layer):

    def __init__(self):
        Layer.__init__(self)
        image = pyglet.resource.image(resconfig.battle_ground_1)
        self.backgound = Sprite(image, position=(image.width/2, image.height/2))


    def draw(self, *args, **kwargs):
        self.backgound.draw()


class Controller(Container):

    is_event_handler = True
    def __init__(self):
        Container.__init__(self)
        #self.add( label )
        button = creator.NewButton("test")
        button.set_callback(self.click)

        self.add(button)

    def click(self):
        print "test click"


    def draw(self, *args, **kwargs):
        pass


def CreateBattleScene():
    scene = Scene()
    scene.add(Background())
    scene.add(Controller())
    return scene



