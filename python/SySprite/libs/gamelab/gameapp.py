"""
Application management. Reusable application object.
"""
# Copyright (c) 2010 Nick Trout.
# See Gamelab-licence.txt for licence details.

import sys
from cocos import director, menu, scene, layer
from squirtle import squirtle_cocos_adaptor as sqa
import pymunk
from gamelab import components

################################################################################
# Application helpers

class SimpleGame:
    def __init__(self):
        """Initialise our game application. """

        # initialise the director, which creates a window
        director.director.init()

    def run(self, app_name, game_layer):
        """ Kick off the game using the layer provided as the main layer. """
        game_scene = scene.Scene( game_layer )

        # create a cache group to assist in rendering SVG nodes using squirtle
        self._cache_group = sqa.SVG_CacheNode()
        game_scene.add(self._cache_group)

        # give user layer access to cache group
        game_layer.svg_cache_group = self._cache_group

        #main_menu = SimpleMainMenuLayer(app_name, game_scene)
        director.director.run( game_scene )


################################################################################
# Main menu

class SimpleMainMenuLayer(menu.Menu):
    """ Provide simple main game menu with default options. """

    def __init__(self, title, newGameScene):
        super(SimpleMainMenuLayer, self).__init__(title)
        assert isinstance(newGameScene, scene.Scene), 'newGameScene expecying Scene'
        self._newGameScene = newGameScene

        # create the options
        m = [
             menu.MenuItem('New Game', self.on_new_game ),
             menu.MenuItem('Quit', self.on_quit )
             ]
        self.create_menu( m )

    def on_new_game(self):
        """ Start a new game. """
        director.director.push( self._newGameScene )

    def on_quit(self):
        """ Quit the game (from the menu). """
        sys.exit(0)


################################################################################
# Game Management Layer

class GameLayer(layer.ColorLayer):
    """ Provides a simple game layer with basic management of game systems. """

    is_event_handler = True

    def __init__(self, back_col = (32,32,200,244)):
        super( GameLayer, self ).__init__(*back_col)

        self._updates = []      # things that need updating every tick
        self._input_listeners = []
        self._drawable = set()

        self.space = None       # No physics by default

        self.spr_mgr = components.SpriteManager(self)

        # ask for the layer update to be called at regular intervals
        self.schedule_interval(self._layer_update, 1.0/50.0)

    def init_physics(self, gravity_dir = (0.0, -900.0)):
        """ Call this to initialise physics for a game. """
        # Initialise the physics system for the application.
        pymunk.init_pymunk()
        self.space = pymunk.Space(iterations=10)
        self.space.gravity = gravity_dir

        #### Updateable ####

    def _layer_update(self, dt):
        # update the physics
        if self.space:
            self.space.step(dt)

        for u in self._updates:
            u.update(dt)

    def add_updateable(self, comp):
        """ Register a component that needs updating every tick. """
        self._updates.append(comp)

        #### Listeners ####

    def add_input_listener(self, IListener):
        """ Record an object that wants to receive input.

            See class InputListenerMixin. A listener should override the methods there.
        """
        self._input_listeners.append(IListener)

        #### Drawable ####

    def add_drawable(self, IDrawable):
        self._drawable.add(IDrawable)

    def remove_drawable(self, IDrawable):
        self._drawable.remove(IDrawable)

    def draw(self):
        """ Override Window event on_draw. """
        layer.ColorLayer.draw(self)
        for d in self._drawable:
            d.on_draw()

        #### Events ####

    def on_mouse_press (self, x,y, buttons, modifiers):
        """This function is called when any mouse button is pressed

            (x, y) are the physical coordinates of the mouse
            'buttons' is a bitwise or of pyglet.window.mouse constants LEFT, MIDDLE, RIGHT
            'modifiers' is a bitwise or of pyglet.window.key modifier constants
               (values like 'SHIFT', 'OPTION', 'ALT')
        """
        x,y = director.director.get_virtual_coordinates(x,y)
        for il in self._input_listeners:
            il.on_mouse_press(x,y, buttons, modifiers)

    def on_mouse_motion (self, x,y, dx,dy):
        """ The mouse moved. """
        x,y = director.director.get_virtual_coordinates(x,y)
        for il in self._input_listeners:
            il.on_mouse_motion(x,y, dx,dy)

    def on_mouse_drag(self, x,y, dx,dy, buttons, modifiers):
        """ The mouse is being dragged. """
        x,y = director.director.get_virtual_coordinates(x,y)
        for il in self._input_listeners:
            il.on_mouse_drag(x,y, dx,dy, buttons, modifiers)

    def on_mouse_release(self, x,y, buttons, modifiers):
        """This function is called when any mouse button is released. """
        x,y = director.director.get_virtual_coordinates(x,y)
        for il in self._input_listeners:
            il.on_mouse_release(x,y, buttons, modifiers)
