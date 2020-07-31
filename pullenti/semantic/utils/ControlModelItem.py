# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
import xml.etree
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Xml import XmlWriter

from pullenti.semantic.utils.ControlModelQuestion import ControlModelQuestion
from pullenti.semantic.core.SemanticRole import SemanticRole
from pullenti.semantic.utils.ControlModelItemType import ControlModelItemType

class ControlModelItem:
    
    def __init__(self) -> None:
        self.typ = ControlModelItemType.WORD
        self.word = None;
        self.links = dict()
        self.nominative_can_be_agent_and_pacient = False
        self.ignorable = False
    
    def __str__(self) -> str:
        res = io.StringIO()
        if (self.ignorable): 
            print("IGNORE ", end="", file=res)
        if (self.typ != ControlModelItemType.WORD): 
            print("{0}: ".format(Utils.enumToString(self.typ)), end="", file=res, flush=True)
        else: 
            print("{0}: ".format(Utils.ifNotNull(self.word, "?")), end="", file=res, flush=True)
        for l_ in self.links.items(): 
            if (l_[1] == SemanticRole.AGENT): 
                print("аг:", end="", file=res)
            elif (l_[1] == SemanticRole.PACIENT): 
                print("пац:", end="", file=res)
            elif (l_[1] == SemanticRole.STRONG): 
                print("сильн:", end="", file=res)
            print("{0}? ".format(l_[0].spelling), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    def check(self, w : 'DerivateWord') -> bool:
        if (self.typ == ControlModelItemType.WORD): 
            return w.class0_.is_noun and w.spelling == self.word
        if (w.class0_.is_verb): 
            if (self.typ == ControlModelItemType.REFLEXIVE): 
                return w.reflexive
            if (self.typ == ControlModelItemType.VERB): 
                return not w.reflexive
        return False
    
    def serialize_xml(self, xml0_ : XmlWriter) -> None:
        xml0_.write_start_element("item")
        xml0_.write_attribute_string("typ", Utils.enumToString(self.typ).upper())
        if (self.nominative_can_be_agent_and_pacient): 
            xml0_.write_attribute_string("agpac", "true")
        if (self.word is not None): 
            xml0_.write_attribute_string("word", self.word)
        for li in self.links.items(): 
            xml0_.write_start_element("li")
            xml0_.write_attribute_string("q", li[0].spelling)
            if (li[1] != SemanticRole.COMMON): 
                xml0_.write_attribute_string("r", Utils.enumToString(li[1]))
            xml0_.write_end_element()
        xml0_.write_end_element()
    
    def deserialize_xml(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        for a in xml0_.attrib.items(): 
            if (a[0] == "word"): 
                self.word = a[1]
            elif (a[0] == "agpac"): 
                self.nominative_can_be_agent_and_pacient = True
            elif (a[0] == "typ"): 
                try: 
                    self.typ = (Utils.valToEnum(a[1], ControlModelItemType))
                except Exception as ex3028: 
                    pass
        for x in xml0_: 
            if (x.tag == "li"): 
                r = SemanticRole.COMMON
                q = None
                for a in x.attrib.items(): 
                    if (a[0] == "q"): 
                        q = ControlModelQuestion.find_by_spel(a[1])
                    elif (a[0] == "r"): 
                        if (a[1] == "AgentOrInstrument"): 
                            r = SemanticRole.AGENT
                        elif (a[1] == "Instrument"): 
                            r = SemanticRole.STRONG
                        else: 
                            try: 
                                r = (Utils.valToEnum(a[1], SemanticRole))
                            except Exception as ex3029: 
                                pass
                if (q is not None and not q in self.links): 
                    self.links[q] = r