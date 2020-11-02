# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import math
from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.core.Termin import Termin
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.internal.BlkTyps import BlkTyps
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper

class BlockLine(MetaToken):
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        super().__init__(b, e0_, None)
        self.is_all_upper = False
        self.has_verb = False
        self.is_exist_name = False
        self.has_content_item_tail = False
        self.words = 0
        self.not_words = 0
        self.number_end = None;
        self.typ = BlkTyps.UNDEFINED
    
    @staticmethod
    def create(t : 'Token', names : 'TerminCollection') -> 'BlockLine':
        if (t is None): 
            return None
        res = BlockLine(t, t)
        tt = t
        while tt is not None: 
            if (tt != t and tt.is_newline_before): 
                break
            else: 
                res.end_token = tt
            tt = tt.next0_
        nums = 0
        while t is not None and t.next0_ is not None and t.end_char <= res.end_char:
            if (isinstance(t, NumberToken)): 
                pass
            else: 
                rom = NumberHelper.try_parse_roman(t)
                if (rom is not None and rom.end_token.next0_ is not None): 
                    t = rom.end_token
                else: 
                    break
            if (t.next0_.is_char('.')): 
                pass
            elif ((isinstance(t.next0_, TextToken)) and not t.next0_.chars.is_all_lower): 
                pass
            else: 
                break
            res.number_end = t
            t = t.next0_
            if (t.is_char('.') and t.next0_ is not None): 
                res.number_end = t
                t = t.next0_
            if (t.is_newline_before): 
                return res
            nums += 1
        tok = BlockLine.__m_ontology.try_parse(t, TerminParseAttr.NO)
        if (tok is None): 
            npt1 = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0, None)
            if (npt1 is not None and npt1.end_token != npt1.begin_token): 
                tok = BlockLine.__m_ontology.try_parse(npt1.noun.begin_token, TerminParseAttr.NO)
        if (tok is not None): 
            if (t.previous is not None and t.previous.is_char(':')): 
                tok = (None)
        if (tok is not None): 
            typ_ = Utils.valToEnum(tok.termin.tag, BlkTyps)
            if (typ_ == BlkTyps.CONSLUSION): 
                if (t.is_newline_after): 
                    pass
                elif (t.next0_ is not None and t.next0_.morph.class0_.is_preposition and t.next0_.next0_ is not None): 
                    tok2 = BlockLine.__m_ontology.try_parse(t.next0_.next0_, TerminParseAttr.NO)
                    if (tok2 is not None and (Utils.valToEnum(tok2.termin.tag, BlkTyps)) == BlkTyps.CHAPTER): 
                        pass
                    else: 
                        tok = (None)
                else: 
                    tok = (None)
            if (t.kit.base_language != t.morph.language): 
                tok = (None)
            if (typ_ == BlkTyps.INDEX and not t.is_value("ОГЛАВЛЕНИЕ", None)): 
                if (not t.is_newline_after and t.next0_ is not None): 
                    npt = NounPhraseHelper.try_parse(t.next0_, NounPhraseParseAttr.NO, 0, None)
                    if (npt is not None and npt.is_newline_after and npt.morph.case_.is_genitive): 
                        tok = (None)
                    elif (npt is None): 
                        tok = (None)
            if ((typ_ == BlkTyps.INTRO and tok is not None and not tok.is_newline_after) and t.is_value("ВВЕДЕНИЕ", None)): 
                npt = NounPhraseHelper.try_parse(t.next0_, NounPhraseParseAttr.NO, 0, None)
                if (npt is not None and npt.morph.case_.is_genitive): 
                    tok = (None)
            if (tok is not None): 
                if (res.number_end is None): 
                    res.number_end = tok.end_token
                    if (res.number_end.end_char > res.end_char): 
                        res.end_token = res.number_end
                res.typ = typ_
                t = tok.end_token
                if (t.next0_ is not None and t.next0_.is_char_of(":.")): 
                    t = t.next0_
                    res.end_token = t
                if (t.is_newline_after or t.next0_ is None): 
                    return res
                t = t.next0_
        if (t.is_char('§') and (isinstance(t.next0_, NumberToken))): 
            res.typ = BlkTyps.CHAPTER
            res.number_end = t
            t = t.next0_
        if (names is not None): 
            tok2 = names.try_parse(t, TerminParseAttr.NO)
            if (tok2 is not None and tok2.end_token.is_newline_after): 
                res.end_token = tok2.end_token
                res.is_exist_name = True
                if (res.typ == BlkTyps.UNDEFINED): 
                    li2 = BlockLine.create((None if res.number_end is None else res.number_end.next0_), None)
                    if (li2 is not None and ((li2.typ == BlkTyps.LITERATURE or li2.typ == BlkTyps.INTRO or li2.typ == BlkTyps.CONSLUSION))): 
                        res.typ = li2.typ
                    else: 
                        res.typ = BlkTyps.CHAPTER
                return res
        t1 = res.end_token
        if ((((isinstance(t1, NumberToken)) or t1.is_char('.'))) and t1.previous is not None): 
            t1 = t1.previous
            if (t1.is_char('.')): 
                res.has_content_item_tail = True
                while t1 is not None and t1.begin_char > res.begin_char: 
                    if (not t1.is_char('.')): 
                        break
                    t1 = t1.previous
        res.is_all_upper = True
        while t is not None and t.end_char <= t1.end_char: 
            if (not (isinstance(t, TextToken)) or not t.chars.is_letter): 
                res.not_words += 1
            else: 
                mc = t.get_morph_class_in_dictionary()
                if (mc.is_undefined): 
                    res.not_words += 1
                elif (t.length_char > 2): 
                    res.words += 1
                if (not t.chars.is_all_upper): 
                    res.is_all_upper = False
                if (t.is_pure_verb): 
                    if (not t.term.endswith("ING")): 
                        res.has_verb = True
            t = t.next0_
        if (res.typ == BlkTyps.UNDEFINED): 
            npt = NounPhraseHelper.try_parse((res.begin_token if res.number_end is None else res.number_end.next0_), NounPhraseParseAttr.NO, 0, None)
            if (npt is not None): 
                if (npt.noun.is_value("ХАРАКТЕРИСТИКА", None) or npt.noun.is_value("СОДЕРЖАНИЕ", "ЗМІСТ")): 
                    ok = True
                    tt = npt.end_token.next0_
                    first_pass3525 = True
                    while True:
                        if first_pass3525: first_pass3525 = False
                        else: tt = tt.next0_
                        if (not (tt is not None and tt.end_char <= res.end_char)): break
                        if (tt.is_char('.')): 
                            continue
                        npt2 = NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.NO, 0, None)
                        if (npt2 is None or not npt2.morph.case_.is_genitive): 
                            ok = False
                            break
                        tt = npt2.end_token
                        if (tt.end_char > res.end_char): 
                            res.end_token = tt
                            if (not tt.is_newline_after): 
                                while res.end_token.next0_ is not None: 
                                    if (res.end_token.is_newline_after): 
                                        break
                                    res.end_token = res.end_token.next0_
                    if (ok): 
                        res.typ = BlkTyps.INTRO
                        res.is_exist_name = True
                elif (npt.noun.is_value("ВЫВОД", "ВИСНОВОК") or npt.noun.is_value("РЕЗУЛЬТАТ", "ДОСЛІДЖЕННЯ")): 
                    ok = True
                    tt = npt.end_token.next0_
                    first_pass3526 = True
                    while True:
                        if first_pass3526: first_pass3526 = False
                        else: tt = tt.next0_
                        if (not (tt is not None and tt.end_char <= res.end_char)): break
                        if (tt.is_char_of(",.") or tt.is_and): 
                            continue
                        npt1 = NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.NO, 0, None)
                        if (npt1 is not None): 
                            if (npt1.noun.is_value("РЕЗУЛЬТАТ", "ДОСЛІДЖЕННЯ") or npt1.noun.is_value("РЕКОМЕНДАЦИЯ", "РЕКОМЕНДАЦІЯ") or npt1.noun.is_value("ИССЛЕДОВАНИЕ", "ДОСЛІДЖЕННЯ")): 
                                tt = npt1.end_token
                                if (tt.end_char > res.end_char): 
                                    res.end_token = tt
                                    if (not tt.is_newline_after): 
                                        while res.end_token.next0_ is not None: 
                                            if (res.end_token.is_newline_after): 
                                                break
                                            res.end_token = res.end_token.next0_
                                continue
                        ok = False
                        break
                    if (ok): 
                        res.typ = BlkTyps.CONSLUSION
                        res.is_exist_name = True
                if (res.typ == BlkTyps.UNDEFINED and npt is not None and npt.end_char <= res.end_char): 
                    ok = False
                    publ = 0
                    if (BlockLine.__is_pub(npt)): 
                        ok = True
                        publ = 1
                    elif ((npt.noun.is_value("СПИСОК", None) or npt.noun.is_value("УКАЗАТЕЛЬ", "ПОКАЖЧИК") or npt.noun.is_value("ПОЛОЖЕНИЕ", "ПОЛОЖЕННЯ")) or npt.noun.is_value("ВЫВОД", "ВИСНОВОК") or npt.noun.is_value("РЕЗУЛЬТАТ", "ДОСЛІДЖЕННЯ")): 
                        if (npt.end_char == res.end_char): 
                            return None
                        ok = True
                    if (ok): 
                        if (npt.begin_token == npt.end_token and npt.noun.is_value("СПИСОК", None) and npt.end_char == res.end_char): 
                            ok = False
                        tt = npt.end_token.next0_
                        first_pass3527 = True
                        while True:
                            if first_pass3527: first_pass3527 = False
                            else: tt = tt.next0_
                            if (not (tt is not None and tt.end_char <= res.end_char)): break
                            if (tt.is_char_of(",.:") or tt.is_and or tt.morph.class0_.is_preposition): 
                                continue
                            if (tt.is_value("ОТРАЖЕНЫ", "ВІДОБРАЖЕНІ")): 
                                continue
                            npt = NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.NO, 0, None)
                            if (npt is None): 
                                ok = False
                                break
                            if (((BlockLine.__is_pub(npt) or npt.noun.is_value("РАБОТА", "РОБОТА") or npt.noun.is_value("ИССЛЕДОВАНИЕ", "ДОСЛІДЖЕННЯ")) or npt.noun.is_value("АВТОР", None) or npt.noun.is_value("ТРУД", "ПРАЦЯ")) or npt.noun.is_value("ТЕМА", None) or npt.noun.is_value("ДИССЕРТАЦИЯ", "ДИСЕРТАЦІЯ")): 
                                tt = npt.end_token
                                if (BlockLine.__is_pub(npt)): 
                                    publ += 1
                                if (tt.end_char > res.end_char): 
                                    res.end_token = tt
                                    if (not tt.is_newline_after): 
                                        while res.end_token.next0_ is not None: 
                                            if (res.end_token.is_newline_after): 
                                                break
                                            res.end_token = res.end_token.next0_
                                continue
                            ok = False
                            break
                        if (ok): 
                            res.typ = BlkTyps.LITERATURE
                            res.is_exist_name = True
                            if (publ == 0 and (res.end_char < ((math.floor((len(res.kit.sofa.text) * 2) / 3))))): 
                                if (res.number_end is not None): 
                                    res.typ = BlkTyps.MISC
                                else: 
                                    res.typ = BlkTyps.UNDEFINED
        return res
    
    @staticmethod
    def __is_pub(t : 'NounPhraseToken') -> bool:
        if (t is None): 
            return False
        if (((t.noun.is_value("ПУБЛИКАЦИЯ", "ПУБЛІКАЦІЯ") or t.noun.is_value("REFERENCE", None) or t.noun.is_value("ЛИТЕРАТУРА", "ЛІТЕРАТУРА")) or t.noun.is_value("ИСТОЧНИК", "ДЖЕРЕЛО") or t.noun.is_value("БИБЛИОГРАФИЯ", "БІБЛІОГРАФІЯ")) or t.noun.is_value("ДОКУМЕНТ", None)): 
            return True
        for a in t.adjectives: 
            if (a.is_value("БИБЛИОГРАФИЧЕСКИЙ", None)): 
                return True
        return False
    
    __m_ontology = None
    
    @staticmethod
    def initialize() -> None:
        if (BlockLine.__m_ontology is not None): 
            return
        BlockLine.__m_ontology = TerminCollection()
        for s in ["СОДЕРЖАНИЕ", "СОДЕРЖИМОЕ", "ОГЛАВЛЕНИЕ", "ПЛАН", "PLAN", "ЗМІСТ", "CONTENTS", "INDEX"]: 
            BlockLine.__m_ontology.add(Termin._new100(s, BlkTyps.INDEX))
        for s in ["ГЛАВА", "CHAPTER", "РАЗДЕЛ", "ПАРАГРАФ", "VOLUME", "SECTION", "РОЗДІЛ"]: 
            BlockLine.__m_ontology.add(Termin._new100(s, BlkTyps.CHAPTER))
        for s in ["ВВЕДЕНИЕ", "ВСТУПЛЕНИЕ", "ПРЕДИСЛОВИЕ", "INTRODUCTION"]: 
            BlockLine.__m_ontology.add(Termin._new100(s, BlkTyps.INTRO))
        for s in ["ВСТУП", "ПЕРЕДМОВА"]: 
            BlockLine.__m_ontology.add(Termin._new388(s, MorphLang.UA, BlkTyps.INTRO))
        for s in ["ВЫВОДЫ", "ВЫВОД", "ЗАКЛЮЧЕНИЕ", "CONCLUSION", "ВИСНОВОК", "ВИСНОВКИ"]: 
            BlockLine.__m_ontology.add(Termin._new100(s, BlkTyps.CONSLUSION))
        for s in ["ПРИЛОЖЕНИЕ", "APPENDIX", "ДОДАТОК"]: 
            BlockLine.__m_ontology.add(Termin._new100(s, BlkTyps.APPENDIX))
        for s in ["СПИСОК СОКРАЩЕНИЙ", "СПИСОК УСЛОВНЫХ СОКРАЩЕНИЙ", "СПИСОК ИСПОЛЬЗУЕМЫХ СОКРАЩЕНИЙ", "УСЛОВНЫЕ СОКРАЩЕНИЯ", "ОБЗОР ЛИТЕРАТУРЫ", "АННОТАЦИЯ", "ANNOTATION", "БЛАГОДАРНОСТИ", "SUPPLEMENT", "ABSTRACT", "СПИСОК СКОРОЧЕНЬ", "ПЕРЕЛІК УМОВНИХ СКОРОЧЕНЬ", "СПИСОК ВИКОРИСТОВУВАНИХ СКОРОЧЕНЬ", "УМОВНІ СКОРОЧЕННЯ", "ОГЛЯД ЛІТЕРАТУРИ", "АНОТАЦІЯ", "ПОДЯКИ"]: 
            BlockLine.__m_ontology.add(Termin._new100(s, BlkTyps.MISC))