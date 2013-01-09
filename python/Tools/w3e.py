#coding=utf-8
__author__ = 'icestar'

import struct

from lxml import etree

root = etree.Element("root")

with open("war3map.w3e", "rb") as mapFile:


    mapContent = mapFile.read()

    #char[4]: 文件ID = "W3E!"
    #地图文件头
    head = mapContent[:4]
    mapContent = mapContent[4:]

    #int: w3e format version [0B 00 00 00]h = version 11
    #地图版本


    version = mapContent[:4]
    version = struct.unpack("i", version)[0]
    mapContent = mapContent[4:]
    xml_version = etree.SubElement(root, "version")
    xml_version.text = str(version)

    #main tileset [TS]
    #地图类型，如：洛丹伦的夏天
    tilesetType = mapContent[0]
    mapContent = mapContent[1:]
    xml_tilesets = etree.SubElement(root, "tilesets")
    xml_tilesets.text = str(tilesetType)

    #int  custom tilesets flag (1 = using cutom, 0 = not using custom tilesets)
    tilesetFlag = mapContent[:4]
    tilesetFlag = struct.unpack("i", tilesetFlag)[0]
    mapContent = mapContent[4:]
    xml_tilesetFlag = etree.SubElement(root, "tilesetFlag")
    xml_tilesetFlag.text = str(tilesetFlag)

    #int: tilesets组的编号 (高高低低原则) (注意: 不能大于16 ，因为tilesets 标注在tilepoints 的定义中)
    tilesetGroupId = mapContent[:4]
    tilesetGroupId = struct.unpack("i", tilesetGroupId)[0]
    mapContent = mapContent[4:]
    xml_tilesetGroupId = etree.SubElement(root, "tilesetGroupId")
    xml_tilesetGroupId.text = str(tilesetGroupId)

    #char[4][地表条目数]: 地表 tilesets IDs (tilesets目录)
    tilesetsIds = mapContent[:4 * tilesetGroupId]
    mapContent = mapContent[4 * tilesetGroupId:]
    xml_tilesetIds = etree.SubElement(root, "tilesetsIds")
    xml_tilesetIds.text = str(tilesetsIds)

    #int: cliff tilesets的编号(高高低低原则) (注意: 不能大于16，原因同上)
    cliffId = mapContent[:4]
    cliffId = struct.unpack("i", cliffId)[0]
    mapContent = mapContent[4:]
    xml_cliffId = etree.SubElement(root, "cliffId")
    xml_cliffId.text = str(cliffId)


    #char[4][悬崖地表数]: cliff tilesets IDs (悬崖tilesets 目录) 例如: "CLdi"代表了洛丹伦悬崖泥土 (想要了解更多，请参阅war3,mpq中"TerrainArt\CliffTypes.slk"文件)
    cliffPath = mapContent[:4 * cliffId]
    mapContent = mapContent[4 * cliffId:]
    xml_cliffPath = etree.SubElement(root, "cliffPath")
    xml_cliffPath.text = str(cliffPath)

    #int: 地图宽度+ 1 = Mx
    Mx = mapContent[:4]
    Mx = struct.unpack("i", Mx)[0]
    mapContent = mapContent[4:]
    xml_mx = etree.SubElement(root, "MX")
    xml_mx.text = str(Mx)

    #int: 地图高度 + 1 = My
    My = mapContent[:4]
    My = struct.unpack("i", My)[0]
    mapContent = mapContent[4:]
    xml_my = etree.SubElement(root, "MY")
    xml_my.text = str(My)

    #float: 地图X坐标中心偏移
    x_offset = mapContent[:4]
    x_offset = struct.unpack("f", x_offset)[0]
    mapContent = mapContent[4:]
    xml_xOffset = etree.SubElement(root, "x_offset")
    xml_xOffset.text = str(x_offset)

    #float: 地图Y坐标中心偏移
    y_offset = mapContent[:4]
    y_offset = struct.unpack("f", y_offset)[0]
    mapContent = mapContent[4:]
    xml_yOffset = etree.SubElement(root, "y_offset")
    xml_yOffset.text = str(y_offset)

    xml_tiles = etree.SubElement(root, "tiles")

    print len(mapContent), Mx, My, Mx * My * 7

    #
    #    原始坐标（0，0）位于地图左下角，比传统在地图正中间做（0，0）更易于使用。
    #
    #    下面是偏移的算法：
    #
    #    -1*(Mx-1)*128/2 and -1*(My-1)*128/2
    #
    #    在这里
    #
    #    (Mx-1) 和 (My-1) 是地图的宽度和高度
    #
    #    128是地图里tile的大小
    #
    #   /2 是取长度的中间值
    #
    #   -1* 因为我们是"translating" 地图区域，而不是定义新坐标

    #数据


    #一个 tilepoint 用一个7bytes的块来定义。

    #block的数量= Mx*My.
    #short: 地面高度
    #C000h: 最低高度(-16384)
    #2000h: 正常高度(零地水准平面)
    #3FFFh: 最高高度(+16383)
    while len(mapContent) > 0:

        terrainHeight = mapContent[0:2]
        terrainHeight = struct.unpack("h", terrainHeight)[0]
        mapContent = mapContent[2:]

        #short: 水面 + 标记*（地图边缘的阴影范围）
        flag = mapContent[0:2]
        flag = struct.unpack("h", flag)[0]
        mapContent = mapContent[2:]

        #
        unknow = mapContent[0]
        unknow = struct.unpack("b", unknow)[0]
        mapContent = mapContent[1:]
        mask = 0xF0
        water_flag = (unknow&mask)>>4
        mask = 0x0F
        terrainType = unknow&mask

        #细节纹理
        texture = mapContent[0]
        texture = struct.unpack("b", texture)[0]
        mapContent = mapContent[1:]



        #悬崖 层次
        height = mapContent[0]
        height = struct.unpack("b", height)[0]
        mapContent = mapContent[1:]

        mask = 0xF0
        xuanya =  (height&mask)>>4
        mask = 0x0F
        cengci = height&mask

        tile = etree.SubElement(xml_tiles, "tile")
        xml_terrainHeight = etree.SubElement(tile, "terrainHeight")
        xml_terrainHeight.text = str(terrainHeight)
        xml_flag = etree.SubElement(tile, "flag")
        xml_flag.text = str(flag)

        xml_waterFlag = etree.SubElement(tile, "waterFlag")
        xml_waterFlag.text = str(water_flag)
        xml_terrainType =  etree.SubElement(tile, "terrainType")
        xml_terrainType.text = str(terrainType)

        xml_texture = etree.SubElement(tile, "texture")
        xml_texture.text = str(texture)
        xml_cliffType =etree.SubElement(tile, "cliffType")
        xml_cliffType.text = str(xuanya)
        xml_height = etree.SubElement(tile, "layoutHeight")
        xml_height.text = str(cengci)





file = open("map.xml", "w")
file.write(etree.tostring(root, pretty_print=True))
file.close()
print "end"