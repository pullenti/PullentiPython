# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.ntopy.Utils import Utils


class ResourceHelper:
    """ Это для поддержки получения встроенных ресурсов """
    
    @staticmethod
    def get_bytes(name : str) -> bytearray:
        """ Получить встроенный ресурс
        
        Args:
            name(str): имя, на который оканчивается ресурс
        
        """
        # ignored: assembly = ResourceHelper.
        names = Utils.getResourcesNames('pullenti.ner.person.internal.properties', '.dat;.png;.txt')
        for n in names: 
            if (n.upper().endswith(name.upper())): 
                try: 
                    inf = Utils.getResourceInfo('pullenti.ner.person.internal.properties', n)
                    if (inf is None): 
                        continue
                    with Utils.getResourceStream('pullenti.ner.person.internal.properties', n) as stream: 
                        buf = Utils.newArrayOfBytes(Utils.getLengthIO(stream), 0)
                        Utils.readIO(stream, buf, 0, len(buf))
                        return buf
                except Exception as ex: 
                    pass
        return None
    
    @staticmethod
    def get_string(name : str) -> str:
        arr = ResourceHelper.get_bytes(name)
        if (arr is None): 
            return None
        if ((len(arr) > 3 and arr[0] == 0xEF and arr[1] == 0xBB) and arr[2] == 0xBF): 
            return arr[3:3+len(arr) - 3].decode('utf-8', 'ignore')
        else: 
            return arr.decode('utf-8', 'ignore')