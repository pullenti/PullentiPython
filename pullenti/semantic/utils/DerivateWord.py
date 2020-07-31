# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
import xml.etree
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Xml import XmlWriter

from pullenti.morph.MorphTense import MorphTense
from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.MorphVoice import MorphVoice
from pullenti.semantic.utils.ExplanWordAttr import ExplanWordAttr
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
        self.next_words = None
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
    
    def serialize(self, xml0_ : XmlWriter, tag_ : str) -> None:
        xml0_.write_start_element(tag_)
        xml0_.write_attribute_string("s", self.spelling)
        if (self.class0_ is not None): 
            xml0_.write_attribute_string("c", str(self.class0_.value))
        if (self.aspect != MorphAspect.UNDEFINED): 
            xml0_.write_attribute_string("a", Utils.enumToString(self.aspect).lower())
        if (self.voice != MorphVoice.UNDEFINED): 
            xml0_.write_attribute_string("v", Utils.enumToString(self.voice).lower())
        if (self.tense != MorphTense.UNDEFINED): 
            xml0_.write_attribute_string("t", Utils.enumToString(self.tense).lower())
        if (self.reflexive): 
            xml0_.write_attribute_string("r", "true")
        if (self.attrs.value != (0)): 
            xml0_.write_attribute_string("attr", str(self.attrs.value))
        if (self.next_words is not None): 
            i = 0
            while i < len(self.next_words): 
                xml0_.write_attribute_string("next{0}".format(i + 1), self.next_words[i])
                i += 1
        xml0_.write_end_element()
    
    def deserialize(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        for a in xml0_.attrib.items(): 
            if (a[0] == "s"): 
                self.spelling = a[1]
            elif (a[0] == "c"): 
                self.class0_ = MorphClass._new72(int(a[1]))
            elif (a[0] == "a"): 
                try: 
                    self.aspect = (Utils.valToEnum(a[1], MorphAspect))
                except Exception as ex3048: 
                    pass
            elif (a[0] == "v"): 
                try: 
                    self.voice = (Utils.valToEnum(a[1], MorphVoice))
                except Exception as ex3049: 
                    pass
            elif (a[0] == "t"): 
                try: 
                    self.tense = (Utils.valToEnum(a[1], MorphTense))
                except Exception as ex3050: 
                    pass
            elif (a[0] == "r"): 
                self.reflexive = a[1] == "true"
            elif (a[0] == "attr"): 
                self.attrs.value = int(a[1])
            elif (a[0].startswith("next")): 
                if (self.next_words is None): 
                    self.next_words = list()
                self.next_words.append(a[1])
    
    @staticmethod
    def _new3046(_arg1 : 'DerivateGroup', _arg2 : str, _arg3 : 'MorphLang', _arg4 : 'MorphClass', _arg5 : 'MorphAspect', _arg6 : bool, _arg7 : 'MorphTense', _arg8 : 'MorphVoice', _arg9 : 'ExplanWordAttr') -> 'DerivateWord':
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