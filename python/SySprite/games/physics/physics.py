# Physics example
#
# Copyright (c) 2010 Nick Trout.
# See Gamelab-licence.txt for licence details.

import sys, random
from gamelab import gameapp, entity, components, sgui
from cocos import scene, director
import pymunk
from pyglet.gl import *


class ObjectSpawnComponent(components.InputBrainComponent):
    def __init__(self):
        pass

    def on_create(self, level):
        super(ObjectSpawnComponent,self).on_create(level)
        self._level = level

    def on_mouse_press(self, x,y, buttons, modifiers):
        # start drawing a line
        self._points = []
        self._level.add_drawable(self)

    def on_mouse_drag(self, x,y, dx,dy, buttons, modifiers):
        # record points on a line made by the mouse
        self._points.append((x,y))

    def on_draw(self):
        # draw the line
        glLineWidth (15.0)
        glColor4f(1.0, 1.0, 1.0, 0.2)
        glBegin(GL_LINE_STRIP)
        for x,y in self._points:
            glVertex2f ((x),(y))
        glEnd()
        glLineWidth (1.0);

    def on_mouse_release(self, x,y, buttons, modifiers):

        if self._mode=='stars':
            for p in self._points:
                ent = entity.Entity(self._level)
                c_gfx = components.SVGComponent(file='games/physics/star7.svgz', scale=.1)
                c_phys = components.OrientablePhysicsBodyComponent(orients=c_gfx)
                c_phys.add_circle(position=p, radius=10)
                ent += [c_gfx, c_phys]

        elif self._mode=='solid':
            if len(self._points) > 0:
                # recalc points relative to their centre
                mx = sum([i[0] for i in self._points])/len(self._points)
                my = sum([i[1] for i in self._points])/len(self._points)
                pts = [(-(x-mx),-(y-my)) for x,y in self._points]

                ent = entity.Entity(self._level)
                c_gfx = components.LineComponent(position=(mx,my), points=pts)
                c_phys = components.OrientablePhysicsBodyComponent(orients=c_gfx)
                c_phys.add_poly(position=(mx,my), points=pts)
                ent += [c_gfx, c_phys]

        # stop drawing the line
        self._points = None
        self._level.remove_drawable(self)

    def mode(self, mode):
        self._mode = mode


################################################################################
# Game

class PhysicsGameLayer(gameapp.GameLayer):
    def __init__(self):
        super(PhysicsGameLayer, self).__init__()

        self.init_physics()     # use physics

        ent = entity.Entity(self)
        osc = ObjectSpawnComponent()
        ent += [ osc ]

        static_body = pymunk.Body(pymunk.inf, pymunk.inf)
        static_lines = [ pymunk.Segment(static_body, (0, 30), (800, 30), 10.0), # bottom
                         pymunk.Segment(static_body, (10, 0), (10, 600), 10.0), # left
                         pymunk.Segment(static_body,(790, 0),(790, 600), 10.0)  # right
                         ]
        for line in static_lines:
            line.elasticity = 0.95
        self.space.add_static(static_lines)

        self._gui = g = sgui.GUI(director.director.window)

        def set_mode(wdg):
            mode = wdg.text
            #print 'mode', mode
            osc.mode(mode.lower())
            g.get_widget('mode').text = mode.upper()

        g.create_dialog('Physics', x=100,y=300, vertical=[
                g.folding_box('Mode', horiz=[
                    g.label('??????????', name='mode', halign='center'),
                    g.button('Stars', action=set_mode, name='stars'),
                    g.button('Solid', action=set_mode),
                ])
            ])
        self.add_drawable(self._gui)

        set_mode(g.get_widget('stars'))   # default mode


def main(args):
    app = gameapp.SimpleGame()
    app.run('Physics', PhysicsGameLayer())
