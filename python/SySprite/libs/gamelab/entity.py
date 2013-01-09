# Component based game entities.
#
# Copyright (c) 2010 Nick Trout.
# See Gamelab-licence.txt for licence details.


################################################################################
# Entity

class Component(object):
    def on_create(self, level):
        """ Called when we want to add an entity to a level. Component initialisation
            and gathering of resources may happen before this point, but it won't appear
            in the level before here. """
        pass
    def on_destroy(self, level):
        """ Remove an entity component from a level. """
        pass


class Entity(object):
    """ Container for components. """
    def __init__(self, level):
        self._comps = []
        self._level = level

    def __iadd__(self, comp_list):
        """ Allow::
                entity += [ ..component list.. ]
        """
        # keep track of which components we've been given
        self._comps += comp_list
        
        # give component a chance to resolve dependencies to other components
        for comp in comp_list:
            comp.on_create(self._level)

################################################################################
# Factory

class EntityType(object):
    def __init__(self, name, comp_list):
        self.name = name
        self._comps = comp_list
        self._props = {}            # properties 


#class propset(object):
#    def __init__(self, set_fn):
#        print 'propset', self, set_fn
#        
#        def my_propset(self, *args):
#            print 'my_propset', self, args
#            self._add_props(set_fn.__name__, set_fn)
#            return set_fn(*args)
#            
#        print self, ent_type.__name__, args
#        
#    def _add_props(self, name, setter):
#        print self 
#        
#    def __call__(self, *args):
#        print 'call', self, args
#        self._etype()


class EntityFactory(object):
    def __init__(self):
        self._objs = {}
        
    def add_type(self, ent_type):
        self._objs[ent_type.name] = ent_type

