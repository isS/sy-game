# Experimental Movie/Media Player
#
# Copyright (c) 2010 Nick Trout.
# See Gamelab-licence.txt for licence details.
#
# Portions of this code came from the pyglet examples, kytten demo.
#

import pyglet
from pyglet.window import key

# disable error checking for increased performance
#pyglet.options['debug_gl'] = False
#from pyglet import gl

from cocos.rect import Rect
import kytten
import mdata

THEME = kytten.Theme('libs/kytten/theme', override={
    #"gui_color": [64, 128, 255, 255],
    "font_size": 9
})

################################################################################
# Media Player

def on_escape(dialog):
    dialog.teardown()


class MarkupMode:
    def __init__(self, app, data):
        self._app = app
        self._data = data

    def init(self):

        self._batch = pyglet.graphics.Batch()

        # Media selection dialog
        self._dialog = kytten.Dialog(
            kytten.Frame(
                kytten.VerticalLayout([
                    kytten.Label("Untagged media:"),
                    kytten.Dropdown(self._data.file_paths,
                            on_select=self._on_select_media),
                    kytten.Label("Tagged media:"),
                    kytten.Dropdown(['']),
                ]),
            ),
            window=self._app, batch=self._batch,
            anchor=kytten.ANCHOR_TOP_LEFT, theme=THEME
        )

        # Timeline dialog
        self._timeline = kytten.Dialog(
            kytten.Frame(
                kytten.HorizontalLayout([
                        kytten.Label('Playing'),
                        kytten.Spacer(width=100, height=75)
                    ]),
                ),
            window=self._app, batch=self._batch,
            anchor=kytten.ANCHOR_BOTTOM, theme=THEME
        )

        self._player = pyglet.media.Player()
        self._vid_rect = Rect(0,0,0,0)
        self._vid_dlg = None
        self._player.volume = 0.2
        self._source = None

        # we want first pop at any input as the top layer
        self._app.push_handlers(self)

    def close(self):
        self._dialog.teardown()
        self._timeline.teardown()
        self._player.pause()
        if self._vid_dlg:
            self._vid_dlg.teardown()

        self._app.pop_handlers()

    def draw(self):
        # draw video if have a valid source
        if self._player.source and self._player.source.video_format:
            self._vid_dlg.draw()

            w = self._vid_space
            self._player.get_texture().blit(w.x, w.y,
                                            width=w.width,
                                            height=w.height)
            #self._player.get_texture().blit(self._vid_rect.left,
            #                                self._vid_rect.bottom,
            #                                width=self._vid_rect.width,
            #                                height=self._vid_rect.height, z=0)

        self._batch.draw()

    def _on_select_media(self, media_file):
        """ Media item was chosen from the list. """

        # load media and skip to it
        source = pyglet.media.load(media_file)
        self._player.queue(source)

        pct = 0.6
        wid, hei = self._app.width*pct, self._app.height*pct
        wid *= source.video_format.sample_aspect

        #self._vid_rect = Rect(0.5*(self._app.width - wid),
        #                      0.5*(self._app.height - hei),
        #                      wid, hei)

        if self._vid_dlg:
            self._vid_dlg.teardown()

        # video dialog
        self._vid_space = kytten.Spacer(width=wid, height=hei)
        self._vid_time_slide = kytten.Slider(0, 0, 1.0, steps=10000, on_set=self.on_set_video_slider)
        self._vid_dlg = kytten.Dialog(
            kytten.Frame(
                kytten.VerticalLayout([
                        self._vid_space,
                        self._vid_time_slide
                    ]),
                ),
            window=self._app, #batch=self._batch,
            anchor=kytten.ANCHOR_CENTER, theme=THEME
        )

        if not self._player.playing:
            self._player.play()
        else:
            self._player.next()

    def on_set_video_slider(self, value):
        print value
        self._player.seek(self._player.source.duration * value)
        self._player.play()

    def on_mouse_press(self, x, y, button, modifiers):
        """ Mouse was clicked in the window. """

        # if we're in the video player, work out time offset from position across
        if self._vid_dlg:
            w = self._vid_space
            if Rect(w.x,w.y,w.width,w.height).contains(x,y):
                pct = (x - self._vid_rect.left) / self._vid_rect.width

                # jump to the correct spot and continue playing
                toff = self._player.seek(self._player.source.duration * pct)
                self._player.play()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.SPACE:
            if self._player.playing:
                self._player.pause()
            else:
                self._player.play()
        elif symbol == key.ESCAPE:
            self._app.dispatch_event('on_close')


################################################################################
# Application

class FlicksApp(pyglet.window.Window):

    is_event_handler = True

    def __init__(self, w,h, args):
        super(FlicksApp,self).__init__(width=w, height=h, caption='Flicks') #, vsync=False)
        self._init_gui()

        # directories to read
        mdir = 'games/flicks'
        if len(args)>0:
            mdir = args[0]

        self._media_data = mdata.MediaData()
        self._media_data.scan_for_files(mdir)

        self._mode = MarkupMode(self, self._media_data)
        self._mode.init()

    def _init_gui(self):

        # force update, *NOTE* kytten *requires* this - not documented well
        self.register_event_type('on_update')
        def update(dt):
        	self.dispatch_event('on_update', dt)
        pyglet.clock.schedule(update)

        # change the background colour
        pyglet.gl.glClearColor(0.8, 0.8, 1.0, 1.0)

    def on_draw(self):
        self.clear()
        self._mode.draw()

    def on_close(self):
        self._mode.close()
        self.close()



def main(args):
    app = FlicksApp(1200,800, args)
    pyglet.app.run()

