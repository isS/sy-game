#coding=utf-8
__author__ = 'icestar'

import config
import cocos

import pyglet

import resources

from connection import conn

import battlescene

if __name__ == '__main__':
    print "start"


    #初始化网络
    conn.init()

    # 初始化cocos
    cocos.director.director.init(width = config.window_width,
                                height = config.window_height,
                                caption = config.window_caption,
                                fullscreen = config.window_fullsreen
    )


    # A scene that contains the layer hello_layer
    main_scene = battlescene.CreateBattleScene()

    # And now, start the application, starting with main_scene
    cocos.director.director.run (main_scene)
