# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import typing
from enum import IntEnum
from pullenti.ntopy.Utils import Utils
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.Termin import Termin

from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.NumberSpellingType import NumberSpellingType


class DocStructItem(MetaToken):
    
    class Typs(IntEnum):
        INDEX = 0
        INDEXITEM = 1
        INTRO = 2
        LITERATURE = 3
        APPENDIX = 4
        CONCLUSION = 5
        OTHER = 6
        CHAPTER = 7
    
    class DocTermin(Termin):
        
        def __init__(self, source : str, add_lemma_variant : bool=False) -> None:
            from pullenti.morph.MorphLang import MorphLang
            self.typ = DocStructItem.Typs.INDEX
            super().__init__(source, MorphLang(), False)
    
        
        @staticmethod
        def _new1472(_arg1 : str, _arg2 : 'Typs') -> 'DocTermin':
            res = DocStructItem.DocTermin(_arg1)
            res.typ = _arg2
            return res
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        
        self.typ = DocStructItem.Typs.INDEX
        self.value = None
        self.content_items = None
        self.attached_item = None
        super().__init__(begin, end, None)
    
    def __str__(self) -> str:
        return "{0} {1} {2}".format(Utils.enumToString(self.typ), Utils.ifNotNull(self.value, ""), ("" if self.attached_item is None else "(attached)"))
    
    @staticmethod
    def try_attach(t : 'Token', items : typing.List['DocStructItem'], is_content_item : bool=False) -> 'DocStructItem':
        
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.NumberToken import NumberToken
        if (t is None): 
            return None
        if (not t.is_newline_before): 
            return None
        tt = t
        first_pass2807 = True
        while True:
            if first_pass2807: first_pass2807 = False
            else: tt = tt.next0
            if (not (tt is not None)): break
            if (tt.is_newline_before and tt != t): 
                return None
            if (not tt.chars.is_letter): 
                continue
            if (tt.chars.is_all_lower): 
                return None
            toks = DocStructItem.__m_ontology.try_attach(tt, None, False)
            if (toks is None): 
                break
            dt = (toks[0].termin if isinstance(toks[0].termin, DocStructItem.DocTermin) else None)
            t1 = toks[0].end_token
            if ((dt.typ == DocStructItem.Typs.INDEX and t1.next0 is not None and not t1.is_newline_after) and t1.next0.chars.is_letter): 
                if (not t1.next0.morph.case.is_genitive): 
                    return None
                else: 
                    t1 = t1.next0
            nam = MiscHelper.get_text_value(tt, t1, GetTextAttr.NO)
            ok = True
            ttt = t1.next0
            while ttt is not None: 
                if (ttt.is_newline_before): 
                    break
                if (ttt.chars.is_letter): 
                    ok = False
                    break
                t1 = ttt
                ttt = ttt.next0
            if (ok): 
                res = DocStructItem._new1468(t, t1, dt.typ, nam)
                if (res.typ == DocStructItem.Typs.INDEX): 
                    DocStructItem.__analyze_content(res)
                elif (items is not None): 
                    for it in items: 
                        if (it.value == nam): 
                            res.attached_item = it
                            break
                return res
            break
        t1 = tt
        while t1 is not None: 
            if (t1.is_newline_after and MiscHelper.can_be_start_of_sentence(t1.next0)): 
                break
            t1 = t1.next0
        if (t1 is None): 
            return None
        if ((t1.end_char - tt.begin_char) > DocStructItem.__max_name_length): 
            return None
        name = MiscHelper.get_text_value(tt, t1, GetTextAttr.NO)
        if (len(name) > DocStructItem.__max_name_length): 
            return None
        name2 = None
        t2 = None
        if (t1.next0 is not None and t1.next0.chars.is_letter): 
            t2 = t1.next0
            while t2 is not None: 
                if (t2.is_newline_after): 
                    break
                t2 = t2.next0
            if (t2 is not None and ((t2.end_char - tt.begin_char) < DocStructItem.__max_name_length)): 
                name2 = MiscHelper.get_text_value(tt, t2, GetTextAttr.NO)
        if (items is not None): 
            for it in items: 
                if (it.value == name or it.value == name2): 
                    res = DocStructItem._new1469(t, t1, DocStructItem.Typs.CHAPTER, it, name)
                    if (it.value == name2): 
                        res.value = name2
                        res.end_token = t2
                    return res
        if (is_content_item): 
            ok = False
            if (tt.is_value("ГЛАВА", None) or tt.is_char('§') or tt.is_value("РАЗДЕЛ", None)): 
                ok = True
            elif (isinstance(tt, NumberToken) and tt.next0 is not None and tt.next0.is_char('.')): 
                ok = True
            if (ok): 
                res = DocStructItem._new1468(t, t1, DocStructItem.Typs.INDEXITEM, name)
                return res
        return None
    
    __max_name_length = 300
    
    @staticmethod
    def __analyze_content(res : 'DocStructItem') -> None:
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.core.MiscHelper import MiscHelper
        t = res.end_token.next0
        if (t is None or not t.is_newline_before): 
            return
        numbers = list()
        first_pass2808 = True
        while True:
            if first_pass2808: first_pass2808 = False
            else: t = t.next0
            if (not (t is not None)): break
            if (t.is_value("СТР", None)): 
                continue
            if (not t.is_newline_before): 
                if (t.chars.is_letter): 
                    break
                else: 
                    continue
            dsi = DocStructItem.try_attach(t, res.content_items, True)
            if (dsi is not None): 
                if (dsi.attached_item is not None): 
                    return
                if (dsi.typ == DocStructItem.Typs.INDEX): 
                    return
                if (res.content_items is None): 
                    res.content_items = list()
                res.content_items.append(dsi)
                t = dsi.end_token
                res.end_token = t
                if (isinstance(t, NumberToken) and (t if isinstance(t, NumberToken) else None).typ == NumberSpellingType.DIGIT): 
                    numbers.append((t if isinstance(t, NumberToken) else None).value)
                continue
            t1 = t
            ok = False
            while t1 is not None: 
                if (t1.chars.is_letter): 
                    ok = True
                    break
                elif (t1.is_newline_after): 
                    break
                t1 = t1.next0
            if (t1.chars.is_all_lower): 
                ok = False
            if (not ok): 
                break
            t2 = t1
            while t2 is not None: 
                if (t2.is_newline_after): 
                    break
                t2 = t2.next0
            if (t2 is None): 
                break
            tt = t2
            while tt != t1: 
                if (isinstance(tt, NumberToken) and (tt if isinstance(tt, NumberToken) else None).typ == NumberSpellingType.DIGIT): 
                    if (tt == t2): 
                        numbers.append((tt if isinstance(tt, NumberToken) else None).value)
                elif (tt.chars.is_letter and not tt.is_value("СТР", None) and not tt.is_value("С", None)): 
                    break
                tt = tt.previous
            item = DocStructItem._new1471(t, t2, DocStructItem.Typs.INDEXITEM)
            item.value = MiscHelper.get_text_value(t1, tt, GetTextAttr.NO)
            if (len(item.value) > DocStructItem.__max_name_length): 
                break
            if (res.content_items is None): 
                res.content_items = list()
            res.content_items.append(item)
            t = item.end_token
            res.end_token = t
    
    __m_ontology = None

    
    @staticmethod
    def _new1468(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Typs', _arg4 : str) -> 'DocStructItem':
        res = DocStructItem(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        return res
    
    @staticmethod
    def _new1469(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Typs', _arg4 : 'DocStructItem', _arg5 : str) -> 'DocStructItem':
        res = DocStructItem(_arg1, _arg2)
        res.typ = _arg3
        res.attached_item = _arg4
        res.value = _arg5
        return res
    
    @staticmethod
    def _new1471(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Typs') -> 'DocStructItem':
        res = DocStructItem(_arg1, _arg2)
        res.typ = _arg3
        return res
    
    # static constructor for class DocStructItem
    @staticmethod
    def _static_ctor():
        from pullenti.ner.core.IntOntologyCollection import IntOntologyCollection
        
        DocStructItem.__m_ontology = IntOntologyCollection()
        for s in ["СОДЕРЖАНИЕ", "СОДЕРЖИМОЕ", "ОГЛАВЛЕНИЕ", "ПЛАН", "PLAN"]: 
            DocStructItem.__m_ontology.add(DocStructItem.DocTermin._new1472(s, DocStructItem.Typs.INDEX))
        for s in ["ВВЕДЕНИЕ", "ВСТУПЛЕНИЕ", "ПРЕДИСЛОВИЕ", "INTRODUCTION"]: 
            DocStructItem.__m_ontology.add(DocStructItem.DocTermin._new1472(s, DocStructItem.Typs.INTRO))
        for s in ["ВЫВОДЫ", "ВЫВОД", "ЗАКЛЮЧЕНИЕ", "CONCLUSION"]: 
            DocStructItem.__m_ontology.add(DocStructItem.DocTermin._new1472(s, DocStructItem.Typs.CONCLUSION))
        for s in ["ЛИТЕРАТУРА", "СПИСОК ЛИТЕРАТУРЫ", "СПИСОК ИСТОЧНИКОВ", "СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ", "СПИСОК ИСПОЛЬЗУЕМЫХ ИСТОЧНИКОВ", "СПЕЦИАЛЬНАЯ ЛИТЕРАТУРА", "СПИСОК ИСПОЛЬЗОВАННОЙ ЛИТЕРАТУРЫ", "СПИСОК ИСПОЛЬЗУЕМОЙ ЛИТЕРАТУРЫ", "ИСПОЛЬЗОВАННЫЕ ИСТОЧНИКИ", "ИСПОЛЬЗУЕМАЯ ЛИТЕРАТУРА", "БИБЛИОГРАФИЯ", "BIBLIOGRAPHY"]: 
            DocStructItem.__m_ontology.add(DocStructItem.DocTermin._new1472(s, DocStructItem.Typs.LITERATURE))
        for s in ["ПРИЛОЖЕНИЕ", "СПИСОК СОКРАЩЕНИЙ", "СПИСОК УСЛОВНЫХ СОКРАЩЕНИЙ", "УСЛОВНЫЕ СОКРАЩЕНИЯ", "ОБЗОР ЛИТЕРАТУРЫ", "АННОТАЦИЯ", "БЛАГОДАРНОСТИ", "ПРИЛОЖЕНИЕ", "SUPPLEMENT"]: 
            DocStructItem.__m_ontology.add(DocStructItem.DocTermin._new1472(s, DocStructItem.Typs.OTHER))

DocStructItem._static_ctor()