# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.morph.LanguageHelper import LanguageHelper

class IntOntologyItem:
    # Элемент внутреннего онтологического словаря
    
    def __init__(self, r : 'Referent') -> None:
        self.termins = list()
        self.__m_canonic_text = None;
        self.typ = None;
        self.misc_attr = None;
        self.owner = None;
        self.referent = None;
        self.tag = None;
        self.referent = r
    
    @property
    def canonic_text(self) -> str:
        """ Каноноический текст """
        if (self.__m_canonic_text is None and len(self.termins) > 0): 
            self.__m_canonic_text = self.termins[0].canonic_text
        return Utils.ifNotNull(self.__m_canonic_text, "?")
    @canonic_text.setter
    def canonic_text(self, value) -> str:
        self.__m_canonic_text = value
        return value
    
    def set_shortest_canonical_text(self, ignore_termins_with_notnull_tags : bool=False) -> None:
        """ В качестве канонического текста установить самый короткий среди терминов
        
        Args:
            ignore_termins_with_notnull_tags(bool): 
        """
        self.__m_canonic_text = (None)
        for t in self.termins: 
            if (ignore_termins_with_notnull_tags and t.tag is not None): 
                continue
            if (len(t.terms) == 0): 
                continue
            s = t.canonic_text
            if (not LanguageHelper.is_cyrillic_char(s[0])): 
                continue
            if (self.__m_canonic_text is None): 
                self.__m_canonic_text = s
            elif (len(s) < len(self.__m_canonic_text)): 
                self.__m_canonic_text = s
    
    def __str__(self) -> str:
        res = io.StringIO()
        if (self.typ is not None): 
            print("{0}: ".format(self.typ), end="", file=res, flush=True)
        print(self.canonic_text, end="", file=res)
        for t in self.termins: 
            tt = str(t)
            if (tt == self.canonic_text): 
                continue
            print("; ", end="", file=res)
            print(tt, end="", file=res)
        if (self.referent is not None): 
            print(" [{0}]".format(self.referent), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)