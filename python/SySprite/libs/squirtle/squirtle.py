"""
This adaptor offers the classic squirtle functionality.
Remember to provide a file named gl_backend.py with the lone line
from pyglet.gl import *


Squirtle mini-library for SVG rendering in Pyglet.

Example usage:
    import squirtle
    my_svg = squirtle.SVG('filename.svg')
    my_svg.draw(100, 200, angle=15)
    
"""


from squirtle_core import *
from pyglet.gl import *

class SVG(object):
    """Opaque SVG image object.
    
    Users should instantiate this object once for each SVG file they wish to 
    render.
    
    """
    
    _disp_list_cache = {}
    def __init__(self, filename, anchor_x=0, anchor_y=0, bezier_points=BEZIER_POINTS, circle_points=CIRCLE_POINTS):
        """Creates an SVG object from a .svg or .svgz file.
        
            `filename`: str
                The name of the file to be loaded.
            `anchor_x`: float
                The horizontal anchor position for scaling and rotations. Defaults to 0. The symbolic 
                values 'left', 'center' and 'right' are also accepted.
            `anchor_y`: float
                The vertical anchor position for scaling and rotations. Defaults to 0. The symbolic 
                values 'bottom', 'center' and 'top' are also accepted.
            `bezier_points`: int
                The number of line segments into which to subdivide Bezier splines. Defaults to 10.
            `circle_points`: int
                The number of line segments into which to subdivide circular and elliptic arcs. 
                Defaults to 10.
                
        """
        
        self.filename = filename
        self.bezier_points = bezier_points
        self.circle_points = circle_points
        self.generate_disp_list()
        self.anchor_x = anchor_x
        self.anchor_y = anchor_y

    def _set_anchor_x(self, anchor_x):
        self._anchor_x = anchor_x
        if self._anchor_x == 'left':
            self._a_x = 0
        elif self._anchor_x == 'center':
            self._a_x = self.width * .5
        elif self._anchor_x == 'right':
            self._a_x = self.width
        else:
            self._a_x = self._anchor_x
    
    def _get_anchor_x(self):
        return self._anchor_x
    
    anchor_x = property(_get_anchor_x, _set_anchor_x)
    
    def _set_anchor_y(self, anchor_y):
        self._anchor_y = anchor_y
        if self._anchor_y == 'bottom':
            self._a_y = 0
        elif self._anchor_y == 'center':
            self._a_y = self.height * .5
        elif self._anchor_y == 'top':
            self._a_y = self.height
        else:
            self._a_y = self.anchor_y

    def _get_anchor_y(self):
        return self._anchor_y
        
    anchor_y = property(_get_anchor_y, _set_anchor_y)
    
    def generate_disp_list(self):
        if (self.filename, self.bezier_points) in self._disp_list_cache:
            self.disp_list, self.width, self.height = self._disp_list_cache[self.filename, self.bezier_points]
        else:
            disp_list, width, height = SVG_pre_render(self.filename,self.bezier_points,self.circle_points).get_legacy_result()
            self._disp_list_cache[self.filename, self.bezier_points] = (disp_list, width, height)
            self.disp_list = disp_list
            self.width = width
            self.height = height

    def draw(self, x, y, z=0, angle=0, scale=1):
        """Draws the SVG to screen.
        
        :Parameters
            `x` : float
                The x-coordinate at which to draw.
            `y` : float
                The y-coordinate at which to draw.
            `z` : float
                The z-coordinate at which to draw. Defaults to 0. Note that z-ordering may not 
                give expected results when transparency is used.
            `angle` : float
                The angle by which the image should be rotated (in degrees). Defaults to 0.
            `scale` : float
                The amount by which the image should be scaled, either as a float, or a tuple 
                of two floats (xscale, yscale).
        
        """
        glPushMatrix()
        glTranslatef(x, y, z)
        if angle:
            glRotatef(angle, 0, 0, 1)
        if scale != 1:
            try:
                glScalef(scale[0], scale[1], 1)
            except TypeError:
                glScalef(scale, scale, 1)
        if self._a_x or self._a_y:  
            glTranslatef(-self._a_x, -self._a_y, 0)
        glCallList(self.disp_list)
        glPopMatrix()
