#-*- coding:UTF-8 -*-
__author__ = 'icestar'

import struct

msg = "test".encode('utf-8')
size = len(msg)

buf = struct.pack("!is",size, msg )

print(buf)
