import random, math

import cocos
import cocos.scene
from cocos.director import director
from cocos.actions import AccelDeccel, MoveTo, Place, RotateBy, Repeat
import squirtle_cocos_adaptor as sqa

class SkyComposition( sqa.SVG_CacheNode ):
    is_event_handler = True # for actions to work
    def __init__(self):
        sqa.SVG_CacheNode.__init__(self)
        self.time_elapsed = 0
        self.sky = sqa.SVGnode("svgs/sky.svg",position=(800/2-20,600/2-20))#,anchor=(0,0))
        self.add(self.sky)
        self.sun = sqa.SVGnode("svgs/sun.svg",position=(600,500))
        self.add(self.sun)
        self.cloud = []
        for n in xrange(10):
            x = random.uniform(0, 928)
            y = random.uniform(0, 728)
            z = random.uniform(1, 2)
            self.cloud.append(sqa.SVGnode("svgs/cloud.svg",position=(x,y),scale=z))
            self.add(self.cloud[n], z)

    def on_enter(self):
        sqa.SVG_CacheNode.on_enter(self)

    def _step(self, dt):
        self.time_elapsed += dt
        for e in self.cloud:
            x,y = e.position
            x = (x+256 + 50*dt)%1200-256
            e.position = (x,y)
        self.sun.rotation = 10 * math.sin(self.time_elapsed)


director.init( width=800, height=600, resizable=False )
scene = cocos.scene.Scene()
cache_node = SkyComposition()
scene.add(cache_node)
director.run( scene )
