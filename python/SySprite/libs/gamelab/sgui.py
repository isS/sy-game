#
# Helper for using simplui (http://code.google.com/p/simplui/)
#
# Copyright (c) 2010 Nick Trout.
# See Gamelab-licence.txt for licence details.

import os
import simplui

SIMPLUI_THEMES = os.path.join(os.path.dirname(simplui.__file__), 'themes').replace('\\', '/')


class GUI:
    """ Top level GUI helper.

            mygui = GUI(pyglet_window)
    """

    def __init__(self, window, theme='pywidget'):
        self._theme = simplui.Theme('%s/%s' % (SIMPLUI_THEMES, theme))

        w,h = window.width, window.height
        self._frame = simplui.Frame(self._theme, w=w,h=h)
        window.push_handlers(self._frame)

    def on_draw(self):
        """ We can respond to drawable events here. """
        self._frame.draw()

    def _content(self, **kws):
        """ Create content of a container.

                vertical -- lay out content using vertical layout.
                horiz -- layout will be horizontal
        """
        content = None
        if 'vertical' in kws:
            content = simplui.VLayout(children=kws['vertical'])
            del kws['vertical']
        if 'horiz' in kws:
            content = simplui.HLayout(children=kws['horiz'])
            del kws['horiz']
        return content

    def get_widget(self, name):
        return self._frame.get_element_by_name(name)

    def create_dialog(self, title='PyGameLab', x=100,y=300, **kws):
        """ Add a dialog to the screen.

                x,y -- position of dialog
                w,h -- width and height of dialog
                title -- title of box
                see _content for child layout details
        """
        dlg = simplui.Dialogue(title, x=x, y=y,
                               content=self._content(**kws))
        self._frame.add(dlg)
        return dlg

    def folding_box(self, title='box', content=[], collapsed=False, **kws):
        """ FoldingBox - vertically collapsible box, resizes to fit contents.

                title -- title of box
                collapsed -- if true, container folded initially
                see _content for child layout details
        """
        return simplui.FoldingBox(title, collapsed=collapsed, content=self._content(**kws))

    def label(self, title='label', **kws):
        """ Text label.

                title -- text in label
        """
        return simplui.Label(title, **kws)

    def button(self, title='button', name=None, action=None):
        """ Clickable button.

        		action -- callback to be invoked when the button is clicked
        """
        return simplui.Button(title, name=name, action=action)

    def checkbox(self, title='checkbox', action=None):
        """ Clickable button.

        		action -- callback to be invoked when the button is clicked
        """
        return simplui.Checkbox(title, action=action)






