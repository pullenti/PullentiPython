# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

class PullentiNerGoodsInternalResourceHelper:
    """ Это для поддержки получения встроенных ресурсов """
    
    @staticmethod
    def get_bytes(name : str) -> bytearray:
        """ Получить встроенный ресурс
        
        Args:
            name(str): имя, на который оканчивается ресурс
        
        """
        # ignored: assembly = PullentiNerGoodsInternalResourceHelper.
        names = Utils.getResourcesNames('pullenti.ner.goods.properties', '.png')
        for n in names: 
            if (Utils.endsWithString(n, name, True)): 
                if (len(name) < len(n)): 
                    if (n[len(n) - len(name) - 1] != '.'): 
                        continue
                try: 
                    inf = Utils.getResourceInfo('pullenti.ner.goods.properties', n)
                    if (inf is None): 
                        continue
                    with Utils.getResourceStream('pullenti.ner.goods.properties', n) as stream: 
                        buf = Utils.newArrayOfBytes(Utils.getLengthIO(stream), 0)
                        Utils.readIO(stream, buf, 0, len(buf))
                        return buf
                except Exception as ex: 
                    pass
        return None
    
    @staticmethod
    def get_string(name : str) -> str:
        arr = PullentiNerGoodsInternalResourceHelper.get_bytes(name)
        if (arr is None): 
            return None
        if ((len(arr) > 3 and arr[0] == (0xEF) and arr[1] == (0xBB)) and arr[2] == (0xBF)): 
            return arr[3:3+len(arr) - 3].decode("UTF-8", 'ignore')
        else: 
            return arr.decode("UTF-8", 'ignore')