# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru


from pullenti.ner.MetaToken import MetaToken
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.morph.MorphClass import MorphClass
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper

class ParenthesisToken(MetaToken):
    # Анализ вводных слов и словосочетаний
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        super().__init__(b, e0_, None)
        self.ref = None;
    
    @staticmethod
    def try_attach(t : 'Token') -> 'ParenthesisToken':
        if (t is None): 
            return None
        tok = ParenthesisToken.__m_termins.try_parse(t, TerminParseAttr.NO)
        if (tok is not None): 
            res = ParenthesisToken(t, tok.end_token)
            return res
        if (not (isinstance(t, TextToken))): 
            return None
        mc = t.get_morph_class_in_dictionary()
        ok = False
        if (mc.is_adverb): 
            ok = True
        elif (mc.is_adjective): 
            if (t.morph.contains_attr("сравн.", None) and t.morph.contains_attr("кач.прил.", None)): 
                ok = True
        if (ok and t.next0_ is not None): 
            if (t.next0_.is_char(',')): 
                return ParenthesisToken(t, t)
            t1 = t.next0_
            if (t1.get_morph_class_in_dictionary() == MorphClass.VERB): 
                if (t1.morph.contains_attr("н.вр.", None) and t1.morph.contains_attr("нес.в.", None) and t1.morph.contains_attr("дейст.з.", None)): 
                    return ParenthesisToken(t, t1)
        t1 = (None)
        if ((t.is_value("В", None) and t.next0_ is not None and t.next0_.is_value("СООТВЕТСТВИЕ", None)) and t.next0_.next0_ is not None and t.next0_.next0_.morph.class0_.is_preposition): 
            t1 = t.next0_.next0_.next0_
        elif (t.is_value("СОГЛАСНО", None)): 
            t1 = t.next0_
        elif (t.is_value("В", None) and t.next0_ is not None): 
            if (t.next0_.is_value("СИЛА", None)): 
                t1 = t.next0_.next0_
            elif (t.next0_.morph.class0_.is_adjective or t.next0_.morph.class0_.is_pronoun): 
                npt = NounPhraseHelper.try_parse(t.next0_, NounPhraseParseAttr.NO, 0, None)
                if (npt is not None): 
                    if (npt.noun.is_value("ВИД", None) or npt.noun.is_value("СЛУЧАЙ", None) or npt.noun.is_value("СФЕРА", None)): 
                        return ParenthesisToken(t, npt.end_token)
        if (t1 is not None): 
            if (t1.next0_ is not None): 
                npt1 = NounPhraseHelper.try_parse(t1, NounPhraseParseAttr.NO, 0, None)
                if (npt1 is not None): 
                    if (npt1.noun.is_value("НОРМА", None) or npt1.noun.is_value("ПОЛОЖЕНИЕ", None) or npt1.noun.is_value("УКАЗАНИЕ", None)): 
                        t1 = npt1.end_token.next0_
            r = t1.get_referent()
            if (r is not None): 
                res = ParenthesisToken._new1115(t, t1, r)
                if (t1.next0_ is not None and t1.next0_.is_comma): 
                    sila = False
                    ttt = t1.next0_.next0_
                    first_pass3626 = True
                    while True:
                        if first_pass3626: first_pass3626 = False
                        else: ttt = ttt.next0_
                        if (not (ttt is not None)): break
                        if (ttt.is_value("СИЛА", None) or ttt.is_value("ДЕЙСТВИЕ", None)): 
                            sila = True
                            continue
                        if (ttt.is_comma): 
                            if (sila): 
                                res.end_token = ttt.previous
                            break
                        if (BracketHelper.can_be_start_of_sequence(ttt, False, False)): 
                            break
                return res
            npt = NounPhraseHelper.try_parse(t1, NounPhraseParseAttr.NO, 0, None)
            if (npt is not None): 
                return ParenthesisToken(t, npt.end_token)
        tt = t
        if (tt.is_value("НЕ", None) and t is not None): 
            tt = tt.next0_
        if (tt.morph.class0_.is_preposition and tt is not None): 
            tt = tt.next0_
            npt1 = NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.NO, 0, None)
            if (npt1 is not None): 
                tt = npt1.end_token
                if (tt.next0_ is not None and tt.next0_.is_comma): 
                    return ParenthesisToken(t, tt.next0_)
                if (npt1.noun.is_value("ОЧЕРЕДЬ", None)): 
                    return ParenthesisToken(t, tt)
        if (t.is_value("ВЕДЬ", None)): 
            return ParenthesisToken(t, t)
        return None
    
    @staticmethod
    def initialize() -> None:
        if (ParenthesisToken.__m_termins is not None): 
            return
        ParenthesisToken.__m_termins = TerminCollection()
        for s in ["ИТАК", "СЛЕДОВАТЕЛЬНО", "ТАКИМ ОБРАЗОМ"]: 
            ParenthesisToken.__m_termins.add(Termin(s, MorphLang.RU, True))
    
    __m_termins = None
    
    @staticmethod
    def _new1115(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Referent') -> 'ParenthesisToken':
        res = ParenthesisToken(_arg1, _arg2)
        res.ref = _arg3
        return res