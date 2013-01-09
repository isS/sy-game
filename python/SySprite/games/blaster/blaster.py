# Blaster game.

# Copyright (c) 2010 Nick Trout.
# See Gamelab-licence.txt for licence details.

import sys, random
from gamelab import gameapp, entity, components
import pyglet
from cocos import actions, layer, menu, sprite, scene, director


class PlayerControlComponent(components.InputBrainComponent):
    def __init__(self, controls=None):
        super(PlayerControlComponent,self).__init__()
        self._controls = controls       # what we control
    
    def on_create(self, level):
        super(PlayerControlComponent,self).on_create(level)

    def on_mouse_press(self, x,y, buttons, modifiers):
        self._controls.position = x,y
        self._controls.velocity = 0,0

################################################################################
# Game types        

class PlayerEntity(entity.EntityType):
    def __init__(self):
        c_spr = components.SpriteComponent(file='games/blaster/cross.png', position=(200,300))
        c_body = components.OrientablePhysicsBodyComponent(orients=c_spr).add_circle(radius=1)
        c_crtl = PlayerControlComponent(controls=c_body)
        super(PlayerEntity,self).__init__('player', [c_spr, c_body, c_crtl])

#    @entity.property
    def position(self, pos):
        print 'pos', pos
        self._pos = pos
       

def create_entity_factory():
    fact = entity.EntityFactory()

    ent = PlayerEntity()
    ent.position( (500,600) )
    fact.add_type(ent)
    

def create_level(level):
    # cross
    plyr = entity.Entity(level)
    c_spr = components.SpriteComponent(file='games/blaster/cross.png', position=(200,300))
    c_body = components.OrientablePhysicsBodyComponent(orients=c_spr).add_circle(radius=1)
    c_crtl = PlayerControlComponent(controls=c_body)
    plyr += [c_spr, c_body, c_crtl]


################################################################################
# Game

class BlasterGameLayer(gameapp.GameLayer):
    def __init__(self):
        super(BlasterGameLayer, self).__init__()
        self.init_physics()
        self._factory = create_entity_factory()
        create_level(self)


def main(args):
    app = gameapp.SimpleGame()
#    main_menu = gameapp.SimpleMainMenuLayer('Blaster', scene.Scene( BlasterGameLayer() ) )
    app.run('Blaster', BlasterGameLayer())

