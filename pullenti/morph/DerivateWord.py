# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphVoice import MorphVoice
from pullenti.morph.MorphTense import MorphTense
from pullenti.morph.ExplanWordAttr import ExplanWordAttr
from pullenti.morph.MorphAspect import MorphAspect

class DerivateWord:
    """ Слово толкового словаря """
    
    def __init__(self, gr : 'DerivateGroup') -> None:
        self.group = None;
        self.spelling = None;
        self.class0_ = None;
        self.aspect = MorphAspect.UNDEFINED
        self.voice = MorphVoice.UNDEFINED
        self.tense = MorphTense.UNDEFINED
        self.reflexive = False
        self.lang = None;
        self.attrs = ExplanWordAttr()
        self.tag = None;
        self.group = gr
    
    def __str__(self) -> str:
        tmp = io.StringIO()
        print(self.spelling, end="", file=tmp)
        if (self.class0_ is not None and not self.class0_.is_undefined): 
            print(", {0}".format(str(self.class0_)), end="", file=tmp, flush=True)
        if (self.aspect != MorphAspect.UNDEFINED): 
            print(", {0}".format(("соверш." if self.aspect == MorphAspect.PERFECTIVE else "несоверш.")), end="", file=tmp, flush=True)
        if (self.voice != MorphVoice.UNDEFINED): 
            print(", {0}".format(("действ." if self.voice == MorphVoice.ACTIVE else ("страдат." if self.voice == MorphVoice.PASSIVE else "средн."))), end="", file=tmp, flush=True)
        if (self.tense != MorphTense.UNDEFINED): 
            print(", {0}".format(("прош." if self.tense == MorphTense.PAST else ("настоящ." if self.tense == MorphTense.PRESENT else "будущ."))), end="", file=tmp, flush=True)
        if (self.reflexive): 
            print(", возвр.", end="", file=tmp)
        if (self.attrs.value != (0)): 
            print(", {0}".format(str(self.attrs)), end="", file=tmp, flush=True)
        return Utils.toStringStringIO(tmp)
    
    @staticmethod
    def _new42(_arg1 : 'DerivateGroup', _arg2 : str, _arg3 : 'MorphLang', _arg4 : 'MorphClass', _arg5 : 'MorphAspect', _arg6 : bool, _arg7 : 'MorphTense', _arg8 : 'MorphVoice', _arg9 : 'ExplanWordAttr') -> 'DerivateWord':
        res = DerivateWord(_arg1)
        res.spelling = _arg2
        res.lang = _arg3
        res.class0_ = _arg4
        res.aspect = _arg5
        res.reflexive = _arg6
        res.tense = _arg7
        res.voice = _arg8
        res.attrs = _arg9
        return res