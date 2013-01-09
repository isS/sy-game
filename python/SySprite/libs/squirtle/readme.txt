squirtle_mod

Purpose:
The original squirtle by Martin O'Leary is a nice package that provides SVG
support to the pyglet library.
This mod is a squirtle refactor so that use with libraries other than pyglet
is facilitated, while compatibility with original squirtle is maintained.
Additionally, adds support for the cocos library.

In brief, the refactor puts the squirtle core functionality (conversion from
svg files to open gl display lists) into one file (squirtle_core).
Then classes used to feed the display lists to the engine are left for
specific adaptors.
At the moment I have two adaptors:
    squirtle : offers the classic squirtle interface, comes from the
               original squirtle
    squirtle_cocos_adaptor: defines a pair of CocosNodes subclasses to draw
               svg files

Typically you should add to the app source dir the files
  squirtle_core.py
  gl_backend.py # with the aproppiate content (see docstring squirtle_core.py)
  xxx_adaptor.py # squirtle_cocos_adaptor.py , squirtle.py or your own custom adaptor

then in your app import xxx_adaptor,probably with a shortname, like
import squirtle_cocos_adaptor as sqa

...

I want to use the cocos functionality in the coming pyweek and Im late,
so I will limit here the docs to the cocos usage. If you want to adapt to other
gl backends, or even for pyglet but not with the details in original squirtle,
then look at the docstring in squirtle core.

Cocos warn: ** Note: This has been fixed in pygamelab --NDT,13-Jan-10 **
to run the example test_suite_cocos.py
you must patch cocos.euclid or will get a traceback.
see http://code.google.com/p/los-cocos/issues/detail?id=119
Also, I would recommend to use cocos svn (but also apply the euclid fix)

Cocos usage:

example typical use:
import cocos
import squirtle_cocos_adaptor as sqa

scene = cocos.Scene.scene()
cache_group = sqa.SVG_CacheNode()
scene.add(cache_group)
ball = sqa.SVGnode("ball",position=123,123)
cache_group.add(ball)
flower1 = sqa.SVGnode('flower.png',position=(200,0),anchor_hint='S')
cache_group.add(flower1)
flower2 = sqa.SVGnode('flower.png',position=(300,0),anchor_hint='S')
cache_group.add(flower2)
...

remarks about the example:
A SVG_Cache_Node is needed even if only one SVGnode wiil be in use.
The anchor_hint defaults to 'CC' --> center
The values for anchor_hint come from a rosewind analogy, with the additional
value 'CC' meaning center.
The instances flower1, flower2 share the same vertex list.

cocos_adaptor entities:

class SVG_CacheNode:
    a cocosnode subclass that acts as a container for SVGnodes
    Responsabilities:
        display list provider: childs get the display list that represent
        the svg file through this node.

        vertex lists caching: childs that use the same svg with the same
        conversion parameters will share the vertext list ( and the file
        will be parsed and converted only once)

        Set and unset a fine open gl state to draw the SVG nodes.

    Additional notes:
    You can have more than one SVG_CacheCode, but caching would not apply
    across diferent cache nodes.
    Childs must be SVGnodes.

class SVGnode:
    A cocosnode subclass to display a svg file

    Responsabilities:
        handle the anchor_hint
        draw the object
        offer additional info:
            members min_x, max_x, min_y, max_y describes the bounding box for
            the vertexes in the display list

            members fwidth, fheight gives the width and size for that bounding box.

    Aditional notes:
    Any SVGnode instance must have an SVG_CacheNode ancestor. In practice,
    you probably will create one SVG_CacheNode instance, then add to him a bunch
    of SVGnode instances, and maybe add some more SVGnodes childs to the previus
    SVGnodes instances.
    If you want to add non SVG class instances as SVGnode childs, you must
    handle set/unset the proper gl state.

    The __init__ anchor_hint parameter dont translate to standart cocosnode
    anchors members until the SVGnode on_enter gets called.
    In particular, the anchor values are meaningless all along the __init__method.

    The additional info ( size, bounding box ) is not available until the
    SVGnode on_enter is called.

    Note that the bounding box and size related members are untransformed values,
    ie dont reflect any rotation or scale.

    The anchor_hint parameter values follow the rosewind analogy, with the
    additional value 'CC' meaning center. Examples: 'SW' refers to the bounding
    box lower left corner, 'N' (or 'CN' or 'NC') refers to the bb top segment
    center.

function f_rosewind_offset :
    this is a helper used internally to build the anchors from the anchor hint
    and the bounding box.
    It can be handy if you roll your own custom adaptor.

this is a preliminary design; after collecting some use cases things may change.
feel free to mail coments (with concrete use cases samples) to
ccanepacc@gmail.com
mention svg or squirtle in the subject, please
or, if fits the cocos-discuss list, mail there.

Limitations
-----------

Squirtle is at present quite limited in the SVG which it can render. Basic
geometric shapes, paths, polygons, etc work fine. Solid fills work, as do both
linear and radial gradients. Note that gradients may render slightly oddly due
to vertex colouring. Gaussian blur not works.

Significant aspects of the SVG specification which have not been implemented
include patterned fills, variable line widths, text and the symbol system.
Remember that you can convert text to paths in your svg editor.

Patches to improve on any of these limitations are greatly welcomed.


Changelog:
The user interface will not change until after pyweek.
Some bugfixes and svg-compatibility upgrades can be released.
I will repost any bugfix in the page
http://groups.google.com/group/cocos-discuss/files
look at a name in the form squirtle_mod_bugfixX.zip
Also will anounce in a followup in the pyweek thread.

release 0.2: squirtle_mod_bugfix2.zip
    fixes a glicth related to error reporting
    fixes a bug in arcs ( I missed some squirtle update )
    fixes another bug in arcs ( sol: clamp before acos in arc_to )
    fixes traceback when svg elements width and height includes units (cm, mm, etc)

    upgraded converter, now understands path opcodes 'm' and 'a'. this prevented
    some parts in za_xxx.svg files to show. Thanks Alia for the svgs.
    Also opcodes 'a', 'c', 'm' understand the 'repeat' use. (probably need to
    port to other opcodes)

    minor upgrade: now color expressed as svg color constants are accepted. You
    can see the know constants in svg_colors.py.

    WARN: There is something wrong with arcs, as seen in z_cubic02_no_css.svg.
    I will work on the problem, but the 1st comment in the related method tells:
        # This function is made out of magical fairy dust
    so it may take some time to nail that !
    workaround: convert arcs to paths in the editor.

    added some svg files which troubled the previous release, most render ok
    now but some quirks remains (see below)
    svg samples details:
        za_guy.svg : in windows raised ValueError: math domain error at arc_to
                     method. Was a numeric precision problem, fixed. ( later I
                     learned that this was fixed in squirtle 2.4 ).
        za_nomnom.svg : not showing an arc. fixed.
        z_one_elip_arc_b.svg : other math domain error, this time in arc_to's
        acos call. Fixed by clamping.
        z_guy_plano.svg : needed opcode 'm' and the repeat form for 'c'.fixed.
        z_arcs01.svg : needed 'a' opcode. partially fixed, needs more work
        Compare with the inkscape render or the sample in
        http://www.w3.org/TR/2003/REC-SVG11-20030114/images/paths/arcs01.png
        z_cubic02_no_css.svg :

release 0.1: squirtle_mod_bugfix1.zip
    fixes one windows style path in the examples for compatibility
    with *nix. (thanks Alia for bugreport and bugfix)

    fixes a traceback while leaving a scene

release 0.0: squirtle_mod.zip

--
claudio canepa
ccanepacc@gmail.com

See: http://groups.google.com/group/cocos-discuss/browse_thread/thread/e717b55a1859b6d
