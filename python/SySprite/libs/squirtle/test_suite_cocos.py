#! usr/bin/env python

# Make sure we are using local version of cocos --NDT
import sys
sys.path = ['..'] + sys.path

import os
import cocos
import cocos.scene
import pyglet
from cocos.director import director
from cocos.actions import AccelDeccel, MoveTo, Place, RotateBy, Repeat
from cocos import euclid
import squirtle_cocos_adaptor as sqa
import time

filelist = [f for f in os.listdir('svgs')
            if f.endswith('svg') or f.endswith('svgz')]

bindings = {
    pyglet.window.key.W:'up',
    pyglet.window.key.S:'dn',
    pyglet.window.key.D:'right',
    pyglet.window.key.A:'left',
    pyglet.window.key.UP:'zoomin',
    pyglet.window.key.DOWN:'zoomout',
    pyglet.window.key.LEFT:'rotanticlockwise',
    pyglet.window.key.RIGHT:'rotclockwise',
    pyglet.window.key.SPACE:'next_file',
    }


class TestSVG(cocos.scene.Scene):
    def __init__(self):
        super(TestSVG,self).__init__()
        bg = cocos.layer.ColorLayer(255,255,255,255)
        self.add(bg)

        self.svg = None
        self.ifile = -1
        button = {}
        for e in bindings:
            button[bindings[e]] = False
        self.button = button
        self.cmd_repeat_time = 0.25
        self.allow_times = {
                             'next_file':time.time()
                            }
        self.svg_group = sqa.SVG_CacheNode()
        self.add(self.svg_group)
        self.schedule(self.update)

    def on_enter(self):
        for e in self.button:
            self.button[e] = False
        director.window.push_handlers(self.on_key_press,self.on_key_release)
        super(TestSVG, self).on_enter()
        if self.svg is None:
            self.cmd_next_file(0.1)

    def on_exit(self):
        super(TestSVG, self).on_exit()
        director.window.pop_handlers()

    def on_key_press(self, symbol, modifiers):
        if symbol not in bindings:
            return False
        cmd = bindings[symbol]
        self.button[cmd] = True
        return True

    def on_key_release(self,symbol,modifiers):
        if symbol not in bindings:
            return False
        cmd = bindings[symbol]
        self.button[cmd] = False
        return True

    def update(self,dt):
        for cmd in self.button:
            if self.button[cmd]:
                #print 'cmd:',cmd
                fn = getattr(self, 'cmd_'+cmd)
                fn(dt)

    def cmd_up(self,dt):
        self.svg.position += euclid.Vector2(0, 160)*dt
    def cmd_dn(self,dt):
        self.svg.position -= euclid.Vector2(0, 160)*dt
    def cmd_left(self,dt):
        self.svg.position -= euclid.Vector2(160, 0)*dt
    def cmd_right(self,dt):
        self.svg.position += euclid.Vector2(160, 0)*dt
    def cmd_zoomin(self,dt):
        self.svg.scale *= (1.0 + 5.0*dt)
    def cmd_zoomout(self,dt):
        self.svg.scale /= (1.0 + 5.0*dt)
    def cmd_rotclockwise(self,dt):
        self.svg.rotation += 160.0*dt
    def cmd_rotanticlockwise(self,dt):
        self.svg.rotation -= 160.0*dt
    def cmd_next_file(self,dt):
        if self.allow_times['next_file']>time.time():
            return
        self.allow_times['next_file'] = time.time() + self.cmd_repeat_time
        if self.svg is not None:
            self.svg_group.remove(self.svg)
        self.ifile = (self.ifile+1)%len(filelist)
        filename = os.path.join('svgs', filelist[self.ifile])
        print 'Showing file:', filename
        w,h = director.get_window_size()
        pos = (w/2.0,h/2.0)
        self.svg = sqa.SVGnode(filename,position=pos,anchor_hint='CC')
        self.svg_group.add(self.svg)
        pre_caption = 'Use WASD to move, arrows to zoom rotate, space to next svg'
        director.window.set_caption(pre_caption + ' - ' + filename)

print 'Use WASD to move, arrows to zoom rotate, space to next svg'
print 'WARN: you must patch cocos.euclid or get traceback. see \nhttp://code.google.com/p/los-cocos/issues/detail?id=119'

director.init( width=800, height=600, resizable=False )
director.show_FPS = True
scene = TestSVG()
director.run( scene )
