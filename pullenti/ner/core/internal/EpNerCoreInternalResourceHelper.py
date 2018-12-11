# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
from pullenti.unisharp.Utils import Utils

class EpNerCoreInternalResourceHelper:
    """ Это для поддержки получения встроенных ресурсов """
    
    @staticmethod
    def getBytes(name : str) -> bytearray:
        """ Получить встроенный ресурс
        
        Args:
            name(str): имя, на который оканчивается ресурс
        
        """
        # ignored: assembly = EpNerCoreInternalResourceHelper.
        names = Utils.getResourcesNames('pullenti.ner.core.properties', '.csv;.png')
        for n in names: 
            if (Utils.endsWithString(n, name, True)): 
                try: 
                    inf = Utils.getResourceInfo('pullenti.ner.core.properties', n)
                    if (inf is None): 
                        continue
                    with Utils.getResourceStream('pullenti.ner.core.properties', n) as stream: 
                        buf = Utils.newArrayOfBytes(Utils.getLengthIO(stream), 0)
                        Utils.readIO(stream, buf, 0, len(buf))
                        return buf
                except Exception as ex: 
                    pass
        return None
    
    @staticmethod
    def getString(name : str) -> str:
        arr = EpNerCoreInternalResourceHelper.getBytes(name)
        if (arr is None): 
            return None
        if ((len(arr) > 3 and arr[0] == (0xEF) and arr[1] == (0xBB)) and arr[2] == (0xBF)): 
            return arr[3:3+len(arr) - 3].decode("UTF-8", 'ignore')
        else: 
            return arr.decode("UTF-8", 'ignore')