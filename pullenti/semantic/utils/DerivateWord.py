# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphVoice import MorphVoice
from pullenti.morph.MorphTense import MorphTense
from pullenti.semantic.utils.ExplanWordAttr import ExplanWordAttr
from pullenti.morph.MorphAspect import MorphAspect

class DerivateWord:
    """ Слово дериватной группы DerivateWord
    
    """
    
    def __init__(self) -> None:
        self.spelling = None;
        self.class0_ = None;
        self.aspect = MorphAspect.UNDEFINED
        self.voice = MorphVoice.UNDEFINED
        self.tense = MorphTense.UNDEFINED
        self.reflexive = False
        self.lang = None;
        self.attrs = ExplanWordAttr()
        self.next_words = None
    
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
    def _new2965(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'MorphClass', _arg4 : 'MorphAspect', _arg5 : bool, _arg6 : 'MorphTense', _arg7 : 'MorphVoice', _arg8 : 'ExplanWordAttr') -> 'DerivateWord':
        res = DerivateWord()
        res.spelling = _arg1
        res.lang = _arg2
        res.class0_ = _arg3
        res.aspect = _arg4
        res.reflexive = _arg5
        res.tense = _arg6
        res.voice = _arg7
        res.attrs = _arg8
        return res