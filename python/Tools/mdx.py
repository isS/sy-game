#coding=utf-8
__author__ = 'icestar'

import struct



with open("HeroArchMage.mdx", "rb") as file:

    mdx = file.read()

    head = mdx[:4]  # MDLX
    mdx = mdx[4:]

    version_flag = mdx[:4]  # VERS
    mdx = mdx[4:]

    version_size = mdx[:4]
    version_size = struct.unpack("i", version_size)[0]
    mdx = mdx[4:]

    version_value = mdx[:version_size]
    version_value = struct.unpack("i", version_value)[0]
    mdx = mdx[version_size:]

    model_flag = mdx[:4]    # MODL
    mdx = mdx[4:]

    model_size = mdx[:4]
    model_size = struct.unpack("i", model_size)[0]
    mdx = mdx[4:]

    model_data = mdx[:model_size]
    mdx = mdx[model_size:]

    model_name = model_data[:80]
    model_data = model_data[80:]
    model_name2 = model_data[:260]
    model_data = model_data[260:]
    model_unknow1 = model_data[:4]
    model_data = model_data[4:]
    model_mins_x =  model_data[:4]
    model_mins_x = struct.unpack("f", model_mins_x)
    model_data = model_data[4:]
    model_mins_y = model_data[:4]
    model_mins_y = struct.unpack("f", model_mins_y)
    model_data = model_data[4:]
    model_mins_z = model_data[:4]
    model_mins_z = struct.unpack("f", model_mins_z)
    model_data = model_data[4:]
    model_max_x = model_data[:4]
    model_max_x = struct.unpack("f", model_max_x)
    model_data = model_data[4:]
    model_max_y =  model_data[:4]
    model_max_y = struct.unpack("f", model_max_y)
    model_data = model_data[4:]
    model_max_z =  model_data[:4]
    model_max_z = struct.unpack("f", model_max_z)
    model_data = model_data[4:]
    model_unknow2 = model_data[:4]


    print "model_name:", model_name
    print "min(%s, %s, %s)"%(model_mins_x, model_mins_y, model_mins_z)
    print "max(%s, %s, %s)"%(model_max_x, model_max_y, model_max_z)

    un = mdx[:4]

    print un