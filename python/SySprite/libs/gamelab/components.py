#
# Stock components for use with entities.
#
# Copyright (c) 2010 Nick Trout.
# See Gamelab-licence.txt for licence details.

import math
from cocos import cocosnode, sprite
from gamelab import entity
import pymunk
from squirtle import squirtle_cocos_adaptor as sqa
from pyglet.gl import *


class InputListenerMixin:
    def on_mouse_press(self, x,y, buttons, modifiers):
        pass
    def on_mouse_motion(self, x, y, dx, dy):
        pass
    def on_mouse_drag(self, x,y, dx,dy, buttons, modifiers):
        pass
    def on_mouse_release(self, x,y, buttons, modifiers):
        pass

class IOrientable:
    # Properties:
    position = None     # get, set
    rotation = None     # get, set (radians)



################################################################################
# Sprite

class SpriteComponent(entity.Component, IOrientable):
    """ This component manages a single sprite. It is orientable by other components.
    """
    def __init__(self, file='no_filename', position=(100,100), z=1):

        self.sprite = sprite.Sprite(file)
        self.sprite.position = position
        self.z = z

    def resolve(self, layer):
        layer.spr_mgr.add(self)

    def _set_position(self, pos):
        self.sprite.position = pos

    position = property(lambda self: self.sprite.position, _set_position)


class SpriteManager:
    """ Container/manager for all sprites in a level. """
    def __init__(self, layer):
        self._layer = layer
        self._sprite_comps = []

    def add(self, comp):
        """ Add a sprite component. """
        self._sprite_comps.append(comp)
        self._layer.add(comp.sprite, z=comp.z)

################################################################################
# SVG / Vector graphics

class SVGComponent(entity.Component, IOrientable):
    """ This component manages an SVG defined graphical object. It is orientable
        by other components.
    """
    def __init__(self, file='no_filename', position=(100,100), z=1, scale=1.0):
        # create parent node to control SVG node
        self._pnode = cocosnode.CocosNode()
        self._set_position(position)
        self._pnode.scale = scale

        # create the SVG node
        self._svg = sqa.SVGnode(file, anchor_hint='CC')
        self._pnode.add(self._svg)
        self.z = z

    def on_create(self, layer):
        # add the SVG node the cache group that will render it
        layer.svg_cache_group.add(self._svg)
        layer.add(self._pnode)

    def _set_position(self, pos):
        self._pnode.x, self._pnode.y = pos

    def _set_rotation(self, angle):
        self._pnode.rotation = angle

    position = property(lambda self: self._pnode.position, _set_position)
    rotation = property(lambda self: self._pnode.rotation, _set_rotation)


class LineComponent(entity.Component, IOrientable, cocosnode.CocosNode):
    """ Draw a line. """
    def __init__(self, position=(100,100), points=[]):
        cocosnode.CocosNode.__init__(self)
        self.position = position
        self.points = points

    def on_create(self, layer):
        # add the SVG node the cache group that will render it
        layer.add(self)

    def draw(self):
        glPushMatrix() # preserve
        self.transform() #prepare
        glBegin(GL_LINE_STRIP)
        for x,y in self.points:
            glVertex2f ((x),(y))
        glEnd()
        glPopMatrix() # restore


################################################################################
# Physics

class OrientablePhysicsBodyComponent(entity.Component):
    """ Add simple physics to an IOrientable object. The object is manipulated
        using the orientable interface. The object will act as though it is attached
        to the physics body.
    """
    def __init__(self, orients=None):
        self._body = None
        self._orient_comp = orients     # the component to set

    def add_circle(self, position=(100,100), mass=1.0, radius=1.0, offset=(0,0)):
        """ Add a circle collision shape to the rigid body. """

        inertia = pymunk.moment_for_circle(mass, 0, radius, (0,0))
        self._body = pymunk.Body(mass, inertia)
        self._body.position = position
        self._body.angle = 0

        self._shape = pymunk.Circle(self._body, radius, offset)
        self._shape.elasticity = 0.2
        self._shape.friction = 0.3
        return self

    def add_poly(self, points, position=(100,100), mass=1.0):
        """ Add a closed polygon collision shape. """

        moment = pymunk.moment_for_poly(mass, points, (0,0))
        self._body = pymunk.Body(mass, moment)
        self._body.position = position
        self._body.angle = 47.0

        self._shape = pymunk.Poly(self._body, points, (0,0))
        return self

    def on_create(self, level):
        assert level.space, 'Physics not initialised'
        level.space.add(self._body, self._shape)
        self._update_orient()
        level.add_updateable(self)

    def _set_position(self, pos):
        self._body.position = pos
        if self._orient_comp:
            self._orient_comp.position = self._body.position

    def _set_rotation(self, angle):
        self._body.angle = angle
        if self._orient_comp:
            self._orient_comp.rotation = self._body.angle

    def _set_velocity(self, vel):
        self._body.velocity = vel

    def _update_orient(self):
        if self._orient_comp:
            self._orient_comp.position = self._body.position
            self._orient_comp.rotation = self._body.angle * (-180.0/math.pi)

    def update(self, dt):
        self._update_orient()

    position = property(lambda self: self._body.position, _set_position)
    velocity = property(lambda self: self._body.velocity, _set_velocity)


################################################################################
# Brain

class BrainComponent(entity.Component):
    """ A component that provides decision making. """
    pass


class InputBrainComponent(BrainComponent, InputListenerMixin):
    """ A Brain component that receives input. """
    def __init__(self):
        super(InputBrainComponent,self).__init__()

    def on_create(self, level):
        super(BrainComponent,self).on_create(level)
        level.add_input_listener(self)

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_press(self, x,y, buttons, modifiers):
        pass

