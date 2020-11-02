# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.TextToken import TextToken
from pullenti.semantic.internal.DelimType import DelimType
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper

class DelimToken(MetaToken):
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        super().__init__(b, e0_, None)
        self.typ = DelimType.UNDEFINED
        self.doublt = False
    
    def __str__(self) -> str:
        return "{0}{1}: {2}".format(Utils.enumToString(self.typ), ("?" if self.doublt else ""), super().__str__())
    
    @staticmethod
    def try_parse(t : 'Token') -> 'DelimToken':
        if (not (isinstance(t, TextToken))): 
            return None
        if (t.is_comma_and): 
            res0 = DelimToken.try_parse(t.next0_)
            if (res0 is not None): 
                res0.begin_token = t
                return res0
            return None
        tok = DelimToken.__m_onto.try_parse(t, TerminParseAttr.NO)
        if (tok is not None): 
            res = DelimToken(t, tok.end_token)
            res.typ = (Utils.valToEnum(tok.termin.tag, DelimType))
            res.doublt = tok.termin.tag2 is not None
            res2 = DelimToken.try_parse(res.end_token.next0_)
            if (res2 is not None): 
                if (res2.typ == res.typ): 
                    res.end_token = res2.end_token
                    res.doublt = False
            if (t.morph.class0_.is_pronoun): 
                npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.PARSEADVERBS, 0, None)
                if (npt is not None and npt.end_char > res.end_char): 
                    return None
            return res
        return None
    
    __m_onto = None
    
    @staticmethod
    def initialize() -> None:
        DelimToken.__m_onto = TerminCollection()
        t = Termin._new100("НО", DelimType.BUT)
        t.add_variant("А", False)
        t.add_variant("ОДНАКО", False)
        t.add_variant("ХОТЯ", False)
        DelimToken.__m_onto.add(t)
        t = Termin._new100("ЕСЛИ", DelimType.IF)
        t.add_variant("В СЛУЧАЕ ЕСЛИ", False)
        DelimToken.__m_onto.add(t)
        t = Termin._new102("КОГДА", DelimType.IF, DelimToken.__m_onto)
        DelimToken.__m_onto.add(t)
        t = Termin._new100("ТО", DelimType.THEN)
        t.add_variant("ТОГДА", False)
        DelimToken.__m_onto.add(t)
        t = Termin._new100("ИНАЧЕ", DelimType.ELSE)
        t.add_variant("В ПРОТИВНОМ СЛУЧАЕ", False)
        DelimToken.__m_onto.add(t)
        t = Termin._new100("ТАК КАК", DelimType.BECAUSE)
        t.add_variant("ПОТОМУ ЧТО", False)
        t.add_variant("ПО ПРИЧИНЕ ТОГО ЧТО", False)
        t.add_variant("ИЗ ЗА ТОГО ЧТО", False)
        t.add_variant("ИЗЗА ТОГО ЧТО", False)
        t.add_variant("ИЗ-ЗА ТОГО ЧТО", False)
        t.add_variant("ТО ЕСТЬ", False)
        DelimToken.__m_onto.add(t)
        t = Termin._new100("ЧТОБЫ", DelimType.FOR)
        t.add_variant("ДЛЯ ТОГО ЧТОБЫ", False)
        DelimToken.__m_onto.add(t)
        t = Termin._new100("ЧТО", DelimType.WHAT)
        DelimToken.__m_onto.add(t)