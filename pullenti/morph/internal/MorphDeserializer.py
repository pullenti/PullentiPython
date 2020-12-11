# Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project.
# The latest version of the code is available on the site www.pullenti.ru

import gzip
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Streams import Stream

class MorphDeserializer:
    
    @staticmethod
    def deflate_gzip(str0_ : Stream, res : Stream) -> None:
        with Stream(gzip.GzipFile(fileobj=str0_.getstream(), mode='r')) as deflate: 
            buf = Utils.newArrayOfBytes(100000, 0)
            len0_ = len(buf)
            while True:
                i = -1
                try: 
                    ii = 0
                    while ii < len0_: 
                        buf[ii] = (0)
                        ii += 1
                    i = deflate.read(buf, 0, len0_)
                except Exception as ex: 
                    for i in range(len0_ - 1, -1, -1):
                        if (buf[i] != (0)): 
                            res.write(buf, 0, i + 1)
                            break
                    else: i = -1
                    break
                if (i < 1): 
                    break
                res.write(buf, 0, i)