"""
Check our run-time environment is correct and working.
"""
# Copyright (c) 2010 Nick Trout.
# See Gamelab-licence.txt for licence details.

import os

PYGLET_NOTE = """
NOTE: To use Pyglet on OSX 10.6 (Snow Leopard) using the system Python 2.6
    you'll need to run Python in 32 bit mode. It is in 64 bit mode by default.
    This is because Pyglet depends on Carbon (which is 32-bit).

    See: http://code.google.com/p/pyglet/issues/detail?id=438
         http://groups.google.com/group/pyglet-users/browse_thread/thread/1cf9b8cff2d27d8b/e44be0c01a0d25bf?#e44be0c01a0d25bf

    A workaround for this is to type the following in a terminal:
    >> defaults write com.apple.versioner.python Prefer-32-Bit -bool yes

"""

import sys, os

# Expected minimum versions:
PYTHON_VER = (2, 5)
COCOS_VER = (0, 3)


def check_env():
    print "Checking the run-time environment for Gamelab..."

    print 'Python version:', sys.version
    if sys.version_info[:2] < PYTHON_VER:
        print 'Warning, may not work correctly with this version of Python. Expects at least: %d.%d' % PYTHON_VER

    if sys.platform=='darwin' and sys.maxint==9223372036854775807:
        print >>sys.stderr, """
You are running python in 64 bit mode. Currently this is a problem for
pyglet as it uses Carbon (32-bit) and not Cocoa (64-bit). We'll put Python in
32-bit mode (read "man python") and you can try again.

Do:
    export VERSIONER_PYTHON_PREFER_32_BIT=yes
"""
        # TODO: Come up with better solution than export 32 bit...
        sys.exit(1)

    try:
        import pyglet
    except ImportError:
        print 'Problem importing Pyglet.'
        sys.exit(1)
    print 'Pyglet version:', pyglet.version

    try:
        import cocos
    except OSError:
        print 'Cocos has problems starting.'
        print PYGLET_NOTE
        sys.exit(1)
    print 'Cocos version:', cocos.version

    ver = tuple(cocos.version.split('.')[:2])
    if ver < COCOS_VER:
        print 'Warning, this may not work with the version of Cocos2d you have. Expecting at least %d.%d' % COCOS_VER

    import pymunk
    print 'pymunk version:', pymunk.version
