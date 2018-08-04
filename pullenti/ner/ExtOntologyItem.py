# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.ntopy.Utils import Utils


class ExtOntologyItem:
    """ Элемент внешней онтологии """
    
    def __init__(self, caption : str=None) -> None:
        self.ext_id = None
        self.type_name = None
        self.referent = None
        self.__m_caption = None
        self.__m_caption = caption
    
    def __str__(self) -> str:
        if (self.__m_caption is not None): 
            return self.__m_caption
        elif (self.referent is None): 
            return "{0}: ?".format(Utils.ifNotNull(self.type_name, "?"))
        else: 
            res = str(self.referent)
            if (self.referent.parent_referent is not None): 
                str1 = str(self.referent.parent_referent)
                if (not str1 in res): 
                    res = (res + "; " + str1)
            return res

    
    @staticmethod
    def _new2605(_arg1 : object, _arg2 : 'Referent', _arg3 : str) -> 'ExtOntologyItem':
        res = ExtOntologyItem()
        res.ext_id = _arg1
        res.referent = _arg2
        res.type_name = _arg3
        return res