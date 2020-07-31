# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import xml.etree
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Xml import XmlWriter

from pullenti.morph.MorphCase import MorphCase
from pullenti.semantic.core.SemanticRole import SemanticRole
from pullenti.semantic.utils.QuestionType import QuestionType

class ControlModelLink:
    
    def __str__(self) -> str:
        if (self.role == SemanticRole.COMMON): 
            return self.spelling
        return "{0} ({1})".format(self.spelling, Utils.enumToString(self.role))
    
    def __init__(self, prep : str, cas : 'MorphCase', spel : str=None, typ : 'QuestionType'=QuestionType.UNDEFINED) -> None:
        self.question = QuestionType.UNDEFINED
        self.preposition = None;
        self.case_ = None;
        self.role = SemanticRole.COMMON
        self.spelling = None;
        self.preposition = prep
        self.case_ = cas
        self.spelling = spel
        self.question = typ
        if (spel is not None): 
            return
        if (not Utils.isNullOrEmpty(prep)): 
            if (cas.is_genitive): 
                spel = "{0} чего".format(prep.lower())
            elif (cas.is_dative): 
                spel = "{0} чему".format(prep.lower())
            elif (cas.is_accusative): 
                spel = "{0} что".format(prep.lower())
            elif (cas.is_instrumental): 
                spel = "{0} чем".format(prep.lower())
            elif (cas.is_prepositional): 
                spel = "{0} чём".format(prep.lower())
        else: 
            self.preposition = (None)
            if (cas is not None): 
                if (cas.is_nominative): 
                    spel = "кто"
                elif (cas.is_genitive): 
                    spel = "чего"
                elif (cas.is_dative): 
                    spel = "чему"
                elif (cas.is_accusative): 
                    spel = "что"
                elif (cas.is_instrumental): 
                    spel = "чем"
                elif (cas.is_prepositional): 
                    spel = "чём"
        self.spelling = spel
    
    def is_equals(self, li : 'ControlModelLink') -> bool:
        if (li.preposition != self.preposition or li.case_ != self.case_): 
            return False
        if (li.preposition is None and ((li.case_ is None or li.case_.is_undefined))): 
            return self.question == li.question
        return True
    
    def serialize_xml(self, xml0_ : XmlWriter) -> None:
        xml0_.write_start_element("li")
        if (self.spelling is not None): 
            xml0_.write_attribute_string("s", self.spelling)
        if (self.preposition is not None): 
            xml0_.write_attribute_string("p", self.preposition)
        if (self.case_ is not None and not self.case_.is_undefined): 
            xml0_.write_attribute_string("c", str(self.case_))
        if (self.question != QuestionType.UNDEFINED): 
            xml0_.write_attribute_string("q", Utils.enumToString(self.question).upper())
        if (self.role != SemanticRole.COMMON): 
            xml0_.write_attribute_string("r", Utils.enumToString(self.role).upper())
        xml0_.write_end_element()
    
    def deserialize_xml(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        for a in xml0_.attrib.items(): 
            if (a[0] == "p"): 
                self.preposition = a[1]
            elif (a[0] == "c"): 
                self.case_ = MorphCase.parse(a[1])
            elif (a[0] == "s"): 
                self.spelling = a[1]
            elif (a[0] == "q"): 
                try: 
                    self.question = (Utils.valToEnum(a[1], QuestionType))
                except Exception as ex3030: 
                    pass
            elif (a[0] == "r"): 
                if (a[1] == "AGENTORINSTRUMENT"): 
                    self.role = SemanticRole.AGENT
                elif (a[1] == "INSTRUMENT"): 
                    self.role = SemanticRole.STRONG
                else: 
                    try: 
                        self.role = (Utils.valToEnum(a[1], SemanticRole))
                    except Exception as ex3031: 
                        pass