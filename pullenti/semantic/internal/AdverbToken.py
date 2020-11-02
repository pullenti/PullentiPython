# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.ner.TextToken import TextToken
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.semantic.SemAttributeType import SemAttributeType
from pullenti.ner.core.MiscHelper import MiscHelper

class AdverbToken(MetaToken):
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        super().__init__(b, e0_, None)
        self.typ = SemAttributeType.UNDEFINED
        self.not0_ = False
        self.__m_spelling = None;
    
    @property
    def spelling(self) -> str:
        if (self.__m_spelling is not None): 
            return self.__m_spelling
        return MiscHelper.get_text_value_of_meta_token(self, GetTextAttr.NO)
    @spelling.setter
    def spelling(self, value) -> str:
        self.__m_spelling = value
        return value
    
    def __str__(self) -> str:
        if (self.typ == SemAttributeType.UNDEFINED): 
            return self.spelling
        return "{0}: {1}{2}".format(Utils.enumToString(self.typ), ("НЕ " if self.not0_ else ""), self.spelling)
    
    @staticmethod
    def try_parse(t : 'Token') -> 'AdverbToken':
        if (t is None): 
            return None
        if ((isinstance(t, TextToken)) and t.term == "НЕ"): 
            nn = AdverbToken.try_parse(t.next0_)
            if (nn is not None): 
                nn.not0_ = True
                nn.begin_token = t
                return nn
        t0 = t
        if (t.next0_ is not None and t.morph.class0_.is_preposition): 
            t = t.next0_
        if (t.is_value("ДРУГ", None) or t.is_value("САМ", None)): 
            t1 = t.next0_
            if (t1 is not None and t1.morph.class0_.is_preposition): 
                t1 = t1.next0_
            if (t1 is not None): 
                if (t1.is_value("ДРУГ", None) and t.is_value("ДРУГ", None)): 
                    return AdverbToken._new2882(t0, t1, SemAttributeType.EACHOTHER)
                if (t1.is_value("СЕБЯ", None) and t.is_value("САМ", None)): 
                    return AdverbToken._new2882(t0, t1, SemAttributeType.HIMELF)
        tok = AdverbToken.__m_termins.try_parse(t, TerminParseAttr.NO)
        if (tok is not None): 
            res = AdverbToken._new2882(t0, tok.end_token, Utils.valToEnum(tok.termin.tag, SemAttributeType))
            t = res.end_token.next0_
            if (t is not None and t.is_comma): 
                t = t.next0_
            if (res.typ == SemAttributeType.LESS or res.typ == SemAttributeType.GREAT): 
                if (t is not None and t.is_value("ЧЕМ", None)): 
                    res.end_token = t
            return res
        mc = t.get_morph_class_in_dictionary()
        if (mc.is_adverb): 
            return AdverbToken(t, t)
        if (t.is_value("ВСТРЕЧА", None) and t.previous is not None and t.previous.is_value("НА", None)): 
            ne = AdverbToken.try_parse(t.next0_)
            if (ne is not None and ne.typ == SemAttributeType.EACHOTHER): 
                return AdverbToken(t.previous, t)
        return None
    
    __m_termins = None
    
    @staticmethod
    def initialize() -> None:
        if (AdverbToken.__m_termins is not None): 
            return
        AdverbToken.__m_termins = TerminCollection()
        t = Termin._new100("ЕЩЕ", SemAttributeType.STILL)
        AdverbToken.__m_termins.add(t)
        t = Termin._new100("УЖЕ", SemAttributeType.ALREADY)
        AdverbToken.__m_termins.add(t)
        t = Termin._new100("ВСЕ", SemAttributeType.ALL)
        AdverbToken.__m_termins.add(t)
        t = Termin._new100("ЛЮБОЙ", SemAttributeType.ANY)
        t.add_variant("ЛЮБОЙ", False)
        t.add_variant("КАЖДЫЙ", False)
        t.add_variant("ЧТО УГОДНО", False)
        t.add_variant("ВСЯКИЙ", False)
        AdverbToken.__m_termins.add(t)
        t = Termin._new100("НЕКОТОРЫЙ", SemAttributeType.SOME)
        t.add_variant("НЕКИЙ", False)
        AdverbToken.__m_termins.add(t)
        t = Termin._new100("ДРУГОЙ", SemAttributeType.OTHER)
        t.add_variant("ИНОЙ", False)
        AdverbToken.__m_termins.add(t)
        t = Termin._new100("ВЕСЬ", SemAttributeType.WHOLE)
        t.add_variant("ЦЕЛИКОМ", False)
        t.add_variant("ПОЛНОСТЬЮ", False)
        AdverbToken.__m_termins.add(t)
        t = Termin._new100("ОЧЕНЬ", SemAttributeType.VERY)
        AdverbToken.__m_termins.add(t)
        t = Termin._new100("МЕНЬШЕ", SemAttributeType.LESS)
        t.add_variant("МЕНЕЕ", False)
        t.add_variant("МЕНЕЕ", False)
        t.add_variant("МЕНЬШЕ", False)
        AdverbToken.__m_termins.add(t)
        t = Termin._new100("БОЛЬШЕ", SemAttributeType.GREAT)
        t.add_variant("БОЛЕЕ", False)
        t.add_variant("СВЫШЕ", False)
        AdverbToken.__m_termins.add(t)
    
    @staticmethod
    def _new2882(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'SemAttributeType') -> 'AdverbToken':
        res = AdverbToken(_arg1, _arg2)
        res.typ = _arg3
        return res