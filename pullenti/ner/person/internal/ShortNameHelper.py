# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import typing
from pullenti.ntopy.Utils import Utils
from pullenti.ntopy.Misc import RefOutArgWrapper
from pullenti.morph.MorphGender import MorphGender

from pullenti.ner.person.internal.ResourceHelper import ResourceHelper
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis


class ShortNameHelper:
    
    class ShortnameVar:
        
        def __init__(self) -> None:
            self.name = None
            self.gender = MorphGender.UNDEFINED
        
        def __str__(self) -> str:
            return self.name
    
        
        @staticmethod
        def _new2412(_arg1 : str, _arg2 : 'MorphGender') -> 'ShortnameVar':
            res = ShortNameHelper.ShortnameVar()
            res.name = _arg1
            res.gender = _arg2
            return res
    
    __m_shorts_names = None
    
    @staticmethod
    def get_shortnames_for_name(name : str) -> typing.List[str]:
        res = list()
        for kp in ShortNameHelper.__m_shorts_names.items(): 
            for v in kp[1]: 
                if (v.name == name): 
                    if (not kp[0] in res): 
                        res.append(kp[0])
        return res
    
    @staticmethod
    def get_names_for_shortname(shortname : str) -> typing.List['ShortnameVar']:
        res = [ ]
        inoutarg2410 = RefOutArgWrapper(None)
        inoutres2411 = Utils.tryGetValue(ShortNameHelper.__m_shorts_names, shortname, inoutarg2410)
        res = inoutarg2410.value
        if (not inoutres2411): 
            return None
        else: 
            return res
    
    __m_inited = False
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.core.AnalysisKit import AnalysisKit
        from pullenti.ner.TextToken import TextToken
        if (ShortNameHelper.__m_inited): 
            return
        ShortNameHelper.__m_inited = True
        obj = ResourceHelper.get_string("ShortNames.txt")
        if (obj is not None): 
            kit = AnalysisKit(SourceOfAnalysis(obj))
            t = kit.first_token
            while t is not None: 
                if (t.is_newline_before): 
                    g = (MorphGender.FEMINIE if t.is_value("F", None) else MorphGender.MASCULINE)
                    t = t.next0_
                    nam = (t if isinstance(t, TextToken) else None).term
                    shos = list()
                    t = t.next0_
                    while t is not None: 
                        if (t.is_newline_before): 
                            break
                        else: 
                            shos.append((t if isinstance(t, TextToken) else None).term)
                        t = t.next0_
                    for s in shos: 
                        li = None
                        inoutarg2413 = RefOutArgWrapper(None)
                        inoutres2414 = Utils.tryGetValue(ShortNameHelper.__m_shorts_names, s, inoutarg2413)
                        li = inoutarg2413.value
                        if (not inoutres2414): 
                            li = list()
                            ShortNameHelper.__m_shorts_names[s] = li
                        li.append(ShortNameHelper.ShortnameVar._new2412(nam, g))
                    if (t is None): 
                        break
                    t = t.previous
                t = t.next0_
    
    # static constructor for class ShortNameHelper
    @staticmethod
    def _static_ctor():
        ShortNameHelper.__m_shorts_names = dict()

ShortNameHelper._static_ctor()