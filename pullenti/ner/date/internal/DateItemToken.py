﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import datetime
import typing
from enum import IntEnum
from pullenti.ntopy.Utils import Utils
from pullenti.ner.MetaToken import MetaToken

from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.date.DatePointerType import DatePointerType
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.core.NumberExType import NumberExType


class DateItemToken(MetaToken):
    """ Примитив, из которых состоит дата """
    
    class DateItemType(IntEnum):
        NUMBER = 0
        YEAR = 1
        MONTH = 2
        DELIM = 3
        HOUR = 4
        MINUTE = 5
        SECOND = 6
        HALFYEAR = 7
        QUARTAL = 8
        POINTER = 9
        CENTURY = 10
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        self.typ = DateItemToken.DateItemType.NUMBER
        self.string_value = None
        self.int_value = 0
        self.lang = None
        self.new_age = 0
        self.__m_year = -1
        self.__m_can_by_month = -1
        super().__init__(begin, end, None)
    
    def __str__(self) -> str:
        return "{0} {1}".format(Utils.enumToString(self.typ), (self.string_value if self.int_value == 0 else str(self.int_value)))
    
    @property
    def year(self) -> int:
        if (self.__m_year > 0): 
            return self.__m_year
        if (self.int_value == 0): 
            return 0
        if (self.new_age == 0): 
            if (self.int_value < 16): 
                return 2000 + self.int_value
            if (self.int_value <= ((datetime.datetime.today().year - 2000) + 5)): 
                return 2000 + self.int_value
            if (self.int_value < 100): 
                return 1900 + self.int_value
        return self.int_value
    
    @year.setter
    def year(self, value) -> int:
        self.__m_year = value
        return value
    
    @property
    def year0(self) -> int:
        if (self.new_age < 0): 
            return - self.year
        return self.year
    
    @property
    def can_be_year(self) -> bool:
        if (self.typ == DateItemToken.DateItemType.YEAR): 
            return True
        if (self.typ == DateItemToken.DateItemType.MONTH or self.typ == DateItemToken.DateItemType.QUARTAL or self.typ == DateItemToken.DateItemType.HALFYEAR): 
            return False
        if (self.int_value >= 50 and (self.int_value < 100)): 
            return True
        if ((self.int_value < 1000) or self.int_value > 2100): 
            return False
        return True
    
    @property
    def can_by_month(self) -> bool:
        if (self.__m_can_by_month >= 0): 
            return self.__m_can_by_month == 1
        if (self.typ == DateItemToken.DateItemType.MONTH): 
            return True
        if (self.typ == DateItemToken.DateItemType.QUARTAL or self.typ == DateItemToken.DateItemType.HALFYEAR or self.typ == DateItemToken.DateItemType.POINTER): 
            return False
        return self.int_value > 0 and self.int_value <= 12
    
    @can_by_month.setter
    def can_by_month(self, value) -> bool:
        self.__m_can_by_month = (1 if value else 0)
        return value
    
    @property
    def can_be_day(self) -> bool:
        if ((self.typ == DateItemToken.DateItemType.MONTH or self.typ == DateItemToken.DateItemType.QUARTAL or self.typ == DateItemToken.DateItemType.HALFYEAR) or self.typ == DateItemToken.DateItemType.POINTER): 
            return False
        return self.int_value > 0 and self.int_value <= 31
    
    @property
    def can_be_hour(self) -> bool:
        if (self.typ != DateItemToken.DateItemType.NUMBER): 
            return self.typ == DateItemToken.DateItemType.HOUR
        if (self.length_char != 2): 
            if (self.length_char == 1 and self.int_value == 0): 
                return True
            return False
        return self.int_value >= 0 and (self.int_value < 24)
    
    @property
    def can_be_minute(self) -> bool:
        if (self.typ != DateItemToken.DateItemType.NUMBER): 
            return self.typ == DateItemToken.DateItemType.MINUTE
        if (self.length_char != 2): 
            return False
        return self.int_value >= 0 and (self.int_value < 60)
    
    @property
    def is_zero_headed(self) -> bool:
        return self.kit.sofa.text[self.begin_char] == '0'
    
    @staticmethod
    def try_attach(t : 'Token', prev : typing.List['DateItemToken']) -> 'DateItemToken':
        """ Привязать с указанной позиции один примитив
        
        Args:
            cnt: 
            indFrom: 
        
        """
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.TextToken import TextToken
        if (t is None): 
            return None
        t0 = t
        if (t0.is_char('_')): 
            t = t.next0
            while t is not None: 
                if (t.is_newline_before): 
                    return None
                if (not t.is_char('_')): 
                    break
                t = t.next0
        elif (BracketHelper.can_be_start_of_sequence(t0, True, False)): 
            ok = False
            t = t.next0
            while t is not None: 
                if (BracketHelper.can_be_end_of_sequence(t, True, t0, False)): 
                    ok = True
                    break
                elif (not t.is_char('_')): 
                    break
                t = t.next0
            if (not ok): 
                t = t0
            else: 
                t = t.next0
                while t is not None: 
                    if (not t.is_char('_')): 
                        break
                    t = t.next0
        elif (isinstance(t0, TextToken) and t0.is_value("THE", None)): 
            res0 = DateItemToken.__try_attach(t.next0, prev)
            if (res0 is not None): 
                res0.begin_token = t
                return res0
        res = DateItemToken.__try_attach(t, prev)
        if (res is None): 
            return None
        res.begin_token = t0
        if (not res.is_whitespace_after and res.end_token.next0 is not None and res.end_token.next0.is_char('_')): 
            t = res.end_token.next0
            while t is not None: 
                if (not t.is_char('_')): 
                    break
                else: 
                    res.end_token = t
                t = t.next0
        if (res.typ == DateItemToken.DateItemType.YEAR or res.typ == DateItemToken.DateItemType.CENTURY or res.typ == DateItemToken.DateItemType.NUMBER): 
            tok = None
            ii = 0
            t = res.end_token.next0
            if (t is not None and t.is_value("ДО", None)): 
                tok = DateItemToken.__m_new_age.try_parse(t.next0, TerminParseAttr.NO)
                ii = -1
            elif (t is not None and t.is_value("ОТ", "ВІД")): 
                tok = DateItemToken.__m_new_age.try_parse(t.next0, TerminParseAttr.NO)
                ii = 1
            else: 
                tok = DateItemToken.__m_new_age.try_parse(t, TerminParseAttr.NO)
                ii = 1
            if (tok is not None): 
                res.new_age = (-1 if ii < 0 else 1)
                res.end_token = tok.end_token
                if (res.typ == DateItemToken.DateItemType.NUMBER): 
                    res.typ = DateItemToken.DateItemType.YEAR
        return res
    
    @staticmethod
    def __is_new_age(t : 'Token') -> bool:
        if (t is None): 
            return False
        if (t.is_value("ДО", None)): 
            return DateItemToken.__m_new_age.try_parse(t.next0, TerminParseAttr.NO) is not None
        elif (t.is_value("ОТ", "ВІД")): 
            return DateItemToken.__m_new_age.try_parse(t.next0, TerminParseAttr.NO) is not None
        return DateItemToken.__m_new_age.try_parse(t, TerminParseAttr.NO) is not None
    
    @staticmethod
    def __try_attach(t : 'Token', prev : typing.List['DateItemToken']) -> 'DateItemToken':
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.TextToken import TextToken
        from pullenti.morph.MorphLang import MorphLang
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.ner.date.DateRangeReferent import DateRangeReferent
        if (t is None): 
            return None
        nt = (t if isinstance(t, NumberToken) else None)
        begin = t
        end = t
        is_in_brack = False
        if ((BracketHelper.can_be_start_of_sequence(t, False, False) and t.next0 is not None and isinstance(t.next0, NumberToken)) and BracketHelper.can_be_end_of_sequence(t.next0.next0, False, None, False)): 
            nt = (t.next0 if isinstance(t.next0, NumberToken) else None)
            end = t.next0.next0
            is_in_brack = True
        if ((t.is_newline_before and BracketHelper.is_bracket(t, False) and isinstance(t.next0, NumberToken)) and BracketHelper.is_bracket(t.next0.next0, False)): 
            nt = (t.next0 if isinstance(t.next0, NumberToken) else None)
            end = t.next0.next0
            is_in_brack = True
        if (nt is not None): 
            if (nt.typ == NumberSpellingType.WORDS): 
                if (nt.morph.class0.is_noun and not nt.morph.class0.is_adjective): 
                    if (t.next0 is not None and ((t.next0.is_value("КВАРТАЛ", None) or t.next0.is_value("ПОЛУГОДИЕ", None) or t.next0.is_value("ПІВРІЧЧЯ", None)))): 
                        pass
                    else: 
                        return None
            if (NumberHelper.try_parse_age(nt) is not None): 
                return None
            res = DateItemToken._new629(begin, end, DateItemToken.DateItemType.NUMBER, nt.value, nt.morph)
            if ((res.int_value == 20 and isinstance(nt.next0, NumberToken) and nt.next0.length_char == 2) and prev is not None): 
                num = 2000 + (nt.next0 if isinstance(nt.next0, NumberToken) else None).value
                if ((num < 2030) and len(prev) > 0 and prev[len(prev) - 1].typ == DateItemToken.DateItemType.MONTH): 
                    ok = False
                    if (nt.whitespaces_after_count == 1): 
                        ok = True
                    elif (nt.is_newline_after and nt.is_newline_after): 
                        ok = True
                    if (ok): 
                        nt = (nt.next0 if isinstance(nt.next0, NumberToken) else None)
                        res.end_token = nt
                        res.int_value = num
            if (res.int_value == 20 or res.int_value == 201): 
                tt = t.next0
                if (tt is not None and tt.is_char('_')): 
                    while tt is not None: 
                        if (not tt.is_char('_')): 
                            break
                        tt = tt.next0
                    tt = DateItemToken.__test_year_rus_word(tt, False)
                    if (tt is not None): 
                        res.int_value = 0
                        res.end_token = tt
                        res.typ = DateItemToken.DateItemType.YEAR
                        return res
            if (res.int_value <= 12 and t.next0 is not None and (t.whitespaces_after_count < 3)): 
                tt = t.next0
                if (tt.is_value("ЧАС", None)): 
                    if ((isinstance(t.previous, TextToken) and not t.previous.chars.is_letter and not t.is_whitespace_before) and isinstance(t.previous.previous, NumberToken) and not t.previous.is_whitespace_before): 
                        pass
                    else: 
                        res.typ = DateItemToken.DateItemType.HOUR
                        res.end_token = tt
                        tt = tt.next0
                        if (tt is not None and tt.is_char('.')): 
                            res.end_token = tt
                            tt = tt.next0
                first_pass2611 = True
                while True:
                    if first_pass2611: first_pass2611 = False
                    else: tt = tt.next0
                    if (not (tt is not None)): break
                    if (tt.is_value("УТРО", "РАНОК")): 
                        res.end_token = tt
                        res.typ = DateItemToken.DateItemType.HOUR
                        return res
                    if (tt.is_value("ВЕЧЕР", "ВЕЧІР")): 
                        res.end_token = tt
                        res.int_value += 12
                        res.typ = DateItemToken.DateItemType.HOUR
                        return res
                    if (tt.is_value("ДЕНЬ", None)): 
                        res.end_token = tt
                        if (res.int_value < 10): 
                            res.int_value += 12
                        res.typ = DateItemToken.DateItemType.HOUR
                        return res
                    if (tt.is_value("НОЧЬ", "НІЧ")): 
                        res.end_token = tt
                        if (res.int_value == 12): 
                            res.int_value = 0
                        elif (res.int_value > 9): 
                            res.int_value += 12
                        res.typ = DateItemToken.DateItemType.HOUR
                        return res
                    if (tt.is_comma or tt.morph.class0.is_adverb): 
                        continue
                    break
                if (res.typ == DateItemToken.DateItemType.HOUR): 
                    return res
            can_be_year_ = True
            if (prev is not None and len(prev) > 0 and prev[len(prev) - 1].typ == DateItemToken.DateItemType.MONTH): 
                pass
            elif ((prev is not None and len(prev) >= 4 and prev[len(prev) - 1].typ == DateItemToken.DateItemType.DELIM) and prev[len(prev) - 2].can_by_month): 
                pass
            elif (nt.next0 is not None and ((nt.next0.is_value("ГОД", None) or nt.next0.is_value("РІК", None)))): 
                if (res.int_value < 1000): 
                    can_be_year_ = False
            tt = DateItemToken.__test_year_rus_word(nt.next0, False)
            if (tt is not None and DateItemToken.__is_new_age(tt.next0)): 
                res.typ = DateItemToken.DateItemType.YEAR
                res.end_token = tt
            elif (can_be_year_): 
                if (res.can_be_year): 
                    tt = DateItemToken.__test_year_rus_word(nt.next0, res.is_newline_before)
                    if ((tt) is not None): 
                        if ((tt.is_value("Г", None) and not tt.is_whitespace_before and t.previous is not None) and ((t.previous.is_value("КОРПУС", None) or t.previous.is_value("КОРП", None)))): 
                            pass
                        elif ((((nt.next0.is_value("Г", None) and (t.whitespaces_before_count < 3) and t.previous is not None) and t.previous.is_value("Я", None) and t.previous.previous is not None) and t.previous.previous.is_char_of("\\/") and t.previous.previous.previous is not None) and t.previous.previous.previous.is_value("А", None)): 
                            return None
                        else: 
                            res.end_token = tt
                            res.typ = DateItemToken.DateItemType.YEAR
                            res.lang = tt.morph.language
                elif (tt is not None and (nt.whitespaces_after_count < 2) and (nt.end_char - nt.begin_char) == 1): 
                    res.end_token = tt
                    res.typ = DateItemToken.DateItemType.YEAR
                    res.lang = tt.morph.language
            if (nt.previous is not None): 
                if (nt.previous.is_value("В", "У") or nt.previous.is_value("К", None) or nt.previous.is_value("ДО", None)): 
                    tt = DateItemToken.__test_year_rus_word(nt.next0, False)
                    if ((tt) is not None): 
                        if ((res.int_value < 100) and isinstance(tt, TextToken) and (((tt if isinstance(tt, TextToken) else None).term == "ГОДА" or (tt if isinstance(tt, TextToken) else None).term == "РОКИ"))): 
                            pass
                        else: 
                            res.end_token = tt
                            res.typ = DateItemToken.DateItemType.YEAR
                            res.lang = tt.morph.language
                            res.begin_token = nt.previous
                elif (((nt.previous.is_value("IN", None) or nt.previous.is_value("SINCE", None))) and res.can_be_year): 
                    res.typ = DateItemToken.DateItemType.YEAR
                    res.begin_token = nt.previous
                elif (nt.previous.is_value("NEL", None) or nt.previous.is_value("DEL", None)): 
                    if (res.can_be_year): 
                        res.typ = DateItemToken.DateItemType.YEAR
                        res.lang = MorphLang.IT
                        res.begin_token = nt.previous
                elif (nt.previous.is_value("IL", None) and res.can_be_day): 
                    res.lang = MorphLang.IT
                    res.begin_token = nt.previous
            t1 = res.end_token.next0
            if (t1 is not None): 
                if ((t1.is_value("ЧАС", None) or t1.is_value("ГОДИНА", None))): 
                    if ((((prev is not None and len(prev) == 2 and prev[0].can_be_hour) and prev[1].typ == DateItemToken.DateItemType.DELIM and not prev[1].is_whitespace_after) and not prev[1].is_whitespace_after and res.int_value >= 0) and (res.int_value < 59)): 
                        prev[0].typ = DateItemToken.DateItemType.HOUR
                        res.typ = DateItemToken.DateItemType.MINUTE
                        res.end_token = t1
                    elif (res.int_value < 24): 
                        if (t1.next0 is not None and t1.next0.is_char('.')): 
                            t1 = t1.next0
                        res.typ = DateItemToken.DateItemType.HOUR
                        res.end_token = t1
                elif ((res.int_value < 60) and ((t1.is_value("МИНУТА", None) or t1.is_value("МИН", None) or t.is_value("ХВИЛИНА", None)))): 
                    if (t1.next0 is not None and t1.next0.is_char('.')): 
                        t1 = t1.next0
                    res.typ = DateItemToken.DateItemType.MINUTE
                    res.end_token = t1
                elif ((res.int_value < 60) and ((t1.is_value("СЕКУНДА", None) or t1.is_value("СЕК", None)))): 
                    if (t1.next0 is not None and t1.next0.is_char('.')): 
                        t1 = t1.next0
                    res.typ = DateItemToken.DateItemType.SECOND
                    res.end_token = t1
                elif ((res.int_value < 30) and ((t1.is_value("ВЕК", "ВІК") or t1.is_value("СТОЛЕТИЕ", "СТОЛІТТЯ")))): 
                    res.typ = DateItemToken.DateItemType.CENTURY
                    res.end_token = t1
                elif (res.int_value <= 4 and t1.is_value("КВАРТАЛ", None)): 
                    res.typ = DateItemToken.DateItemType.QUARTAL
                    res.end_token = t1
                elif (res.int_value <= 2 and ((t1.is_value("ПОЛУГОДИЕ", None) or t1.is_value("ПІВРІЧЧЯ", None)))): 
                    res.typ = DateItemToken.DateItemType.HALFYEAR
                    res.end_token = t1
            return res
        t0 = (t if isinstance(t, TextToken) else None)
        if (t0 is None): 
            return None
        txt = t0.get_source_text()
        if ((txt[0] == 'I' or txt[0] == 'X' or txt[0] == 'Х') or txt[0] == 'V'): 
            lat = NumberHelper.try_parse_roman(t)
            if (lat is not None and lat.end_token.next0 is not None): 
                tt = lat.end_token.next0
                if (tt.is_value("КВАРТАЛ", None) and lat.value > 0 and lat.value <= 4): 
                    return DateItemToken._new630(t, tt, DateItemToken.DateItemType.QUARTAL, lat.value)
                if (tt.is_value("ПОЛУГОДИЕ", "ПІВРІЧЧЯ") and lat.value > 0 and lat.value <= 2): 
                    return DateItemToken._new630(t, lat.end_token.next0, DateItemToken.DateItemType.HALFYEAR, lat.value)
                if (tt.is_value("ВЕК", "ВІК") or tt.is_value("СТОЛЕТИЕ", "СТОЛІТТЯ")): 
                    return DateItemToken._new630(t, lat.end_token.next0, DateItemToken.DateItemType.CENTURY, lat.value)
                if (tt.is_value("В", None) and tt.next0 is not None and tt.next0.is_char('.')): 
                    if (prev is not None and len(prev) > 0 and prev[len(prev) - 1].typ == DateItemToken.DateItemType.POINTER): 
                        return DateItemToken._new630(t, tt.next0, DateItemToken.DateItemType.CENTURY, lat.value)
                    if (DateItemToken.__is_new_age(tt.next0.next0)): 
                        return DateItemToken._new630(t, tt.next0, DateItemToken.DateItemType.CENTURY, lat.value)
                if (tt.is_hiphen): 
                    lat2 = NumberHelper.try_parse_roman(tt.next0)
                    if (lat2 is not None and lat2.value > lat.value and lat2.end_token.next0 is not None): 
                        if (lat2.end_token.next0.is_value("ВЕК", "ВІК") or lat2.end_token.next0.is_value("СТОЛЕТИЕ", "СТОЛІТТЯ")): 
                            return DateItemToken._new630(t, lat.end_token, DateItemToken.DateItemType.CENTURY, lat.value)
        if (t is not None and t.is_value("НАПРИКІНЦІ", None)): 
            return DateItemToken._new636(t, t, DateItemToken.DateItemType.POINTER, "конец")
        if (t is not None and t.is_value("ДОНЕДАВНА", None)): 
            return DateItemToken._new636(t, t, DateItemToken.DateItemType.POINTER, "сегодня")
        tok = DateItemToken.__m_seasons.try_parse(t, TerminParseAttr.NO)
        if ((tok is not None and Utils.valToEnum(tok.termin.tag, DatePointerType) == DatePointerType.SUMMER and t.morph.language.is_ru) and isinstance(t, TextToken)): 
            str0 = (t if isinstance(t, TextToken) else None).term
            if (str0 != "ЛЕТОМ" and str0 != "ЛЕТА" and str0 != "ЛЕТО"): 
                tok = None
        if (tok is not None): 
            return DateItemToken._new630(t, tok.end_token, DateItemToken.DateItemType.POINTER, Utils.valToEnum(tok.termin.tag, DatePointerType))
        npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0)
        if (npt is not None): 
            tok = DateItemToken.__m_seasons.try_parse(npt.end_token, TerminParseAttr.NO)
            if ((tok is not None and Utils.valToEnum(tok.termin.tag, DatePointerType) == DatePointerType.SUMMER and t.morph.language.is_ru) and isinstance(t, TextToken)): 
                str0 = (t if isinstance(t, TextToken) else None).term
                if (str0 != "ЛЕТОМ" and str0 != "ЛЕТА" and str0 != "ЛЕТО"): 
                    tok = None
            if (tok is not None): 
                return DateItemToken._new630(t, tok.end_token, DateItemToken.DateItemType.POINTER, Utils.valToEnum(tok.termin.tag, DatePointerType))
            typ_ = DateItemToken.DateItemType.NUMBER
            if (npt.noun.is_value("КВАРТАЛ", None)): 
                typ_ = DateItemToken.DateItemType.QUARTAL
            elif (npt.end_token.is_value("ПОЛУГОДИЕ", None) or npt.end_token.is_value("ПІВРІЧЧЯ", None)): 
                typ_ = DateItemToken.DateItemType.HALFYEAR
            elif (npt.end_token.is_value("НАЧАЛО", None) or npt.end_token.is_value("ПОЧАТОК", None)): 
                return DateItemToken._new636(t, npt.end_token, DateItemToken.DateItemType.POINTER, "начало")
            elif (npt.end_token.is_value("СЕРЕДИНА", None)): 
                return DateItemToken._new636(t, npt.end_token, DateItemToken.DateItemType.POINTER, "середина")
            elif (npt.end_token.is_value("КОНЕЦ", None) or npt.end_token.is_value("КІНЕЦЬ", None) or npt.end_token.is_value("НАПРИКІНЕЦЬ", None)): 
                return DateItemToken._new636(t, npt.end_token, DateItemToken.DateItemType.POINTER, "конец")
            elif (npt.end_token.is_value("ВРЕМЯ", None) and len(npt.adjectives) > 0 and npt.end_token.previous.is_value("НАСТОЯЩЕЕ", None)): 
                return DateItemToken._new636(t, npt.end_token, DateItemToken.DateItemType.POINTER, "сегодня")
            elif (npt.end_token.is_value("ЧАС", None) and len(npt.adjectives) > 0 and npt.end_token.previous.is_value("ДАНИЙ", None)): 
                return DateItemToken._new636(t, npt.end_token, DateItemToken.DateItemType.POINTER, "сегодня")
            if (typ_ != DateItemToken.DateItemType.NUMBER): 
                delta = 0
                if (len(npt.adjectives) > 0): 
                    if (npt.adjectives[0].is_value("ПОСЛЕДНИЙ", None) or npt.adjectives[0].is_value("ОСТАННІЙ", None)): 
                        return DateItemToken._new630(t0, npt.end_token, typ_, (4 if typ_ == DateItemToken.DateItemType.QUARTAL else 2))
                    if (npt.adjectives[0].is_value("ПРЕДЫДУЩИЙ", None) or npt.adjectives[0].is_value("ПОПЕРЕДНІЙ", None)): 
                        delta = -1
                    elif (npt.adjectives[0].is_value("СЛЕДУЮЩИЙ", None) or npt.adjectives[0].is_value("ПОСЛЕДУЮЩИЙ", None) or npt.adjectives[0].is_value("НАСТУПНИЙ", None)): 
                        delta = 1
                    else: 
                        return None
                cou = 0
                tt = t.previous
                first_pass2612 = True
                while True:
                    if first_pass2612: first_pass2612 = False
                    else: tt = tt.previous
                    if (not (tt is not None)): break
                    if (cou > 200): 
                        break
                    dr = (tt.get_referent() if isinstance(tt.get_referent(), DateRangeReferent) else None)
                    if (dr is None): 
                        continue
                    if (typ_ == DateItemToken.DateItemType.QUARTAL): 
                        ii = dr.quarter_number
                        if (ii < 1): 
                            continue
                        ii += delta
                        if ((ii < 1) or ii > 4): 
                            continue
                        return DateItemToken._new630(t0, npt.end_token, typ_, ii)
                    if (typ_ == DateItemToken.DateItemType.HALFYEAR): 
                        ii = dr.halfyear_number
                        if (ii < 1): 
                            continue
                        ii += delta
                        if ((ii < 1) or ii > 2): 
                            continue
                        return DateItemToken._new630(t0, npt.end_token, typ_, ii)
        term = t0.term
        if (not term[0].isalnum()): 
            if (t0.is_char_of(".\\/:") or t0.is_hiphen): 
                return DateItemToken._new636(t0, t0, DateItemToken.DateItemType.DELIM, term)
            elif (t0.is_char(',')): 
                return DateItemToken._new636(t0, t0, DateItemToken.DateItemType.DELIM, term)
            else: 
                return None
        if (term == "O" or term == "О"): 
            if (isinstance(t.next0, NumberToken) and not t.is_whitespace_after and ((t.next0 if isinstance(t.next0, NumberToken) else None).value < 10)): 
                return DateItemToken._new630(t, t.next0, DateItemToken.DateItemType.NUMBER, (t.next0 if isinstance(t.next0, NumberToken) else None).value)
        if (term[0].isalpha()): 
            inf = DateItemToken.__m_monthes.try_parse(t, TerminParseAttr.NO)
            if (inf is not None and inf.termin.tag is None): 
                inf = DateItemToken.__m_monthes.try_parse(inf.end_token.next0, TerminParseAttr.NO)
            if (inf is not None and isinstance(inf.termin.tag, int)): 
                return DateItemToken._new651(inf.begin_token, inf.end_token, DateItemToken.DateItemType.MONTH, inf.termin.tag, inf.termin.lang)
        return None
    
    DAYS_OF_WEEK = None
    
    __m_new_age = None
    
    __m_monthes = None
    
    __m_seasons = None
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.core.TerminCollection import TerminCollection
        from pullenti.ner.core.Termin import Termin
        from pullenti.morph.MorphLang import MorphLang
        if (DateItemToken.__m_new_age is not None): 
            return
        DateItemToken.__m_new_age = TerminCollection()
        tt = Termin._new652("НОВАЯ ЭРА", MorphLang.RU, True, "НОВОЙ ЭРЫ")
        tt.add_variant("НАША ЭРА", True)
        tt.add_abridge("Н.Э.")
        DateItemToken.__m_new_age.add(tt)
        tt = Termin._new652("НОВА ЕРА", MorphLang.UA, True, "НОВОЇ ЕРИ")
        tt.add_variant("НАША ЕРА", True)
        tt.add_abridge("Н.Е.")
        DateItemToken.__m_new_age.add(tt)
        tt = Termin("РОЖДЕСТВО ХРИСТОВО", MorphLang.RU, True)
        tt.add_abridge("Р.Х.")
        DateItemToken.__m_new_age.add(tt)
        tt = Termin("РІЗДВА ХРИСТОВОГО", MorphLang.UA, True)
        tt.add_abridge("Р.Х.")
        DateItemToken.__m_new_age.add(tt)
        DateItemToken.__m_seasons = TerminCollection()
        DateItemToken.__m_seasons.add(Termin._new654("ЗИМА", MorphLang.RU, True, DatePointerType.WINTER))
        DateItemToken.__m_seasons.add(Termin._new654("WINTER", MorphLang.EN, True, DatePointerType.WINTER))
        t = Termin._new654("ВЕСНА", MorphLang.RU, True, DatePointerType.SPRING)
        t.add_variant("ПРОВЕСНА", True)
        DateItemToken.__m_seasons.add(t)
        DateItemToken.__m_seasons.add(Termin._new654("SPRING", MorphLang.EN, True, DatePointerType.SPRING))
        t = Termin._new654("ЛЕТО", MorphLang.RU, True, DatePointerType.SUMMER)
        DateItemToken.__m_seasons.add(t)
        t = Termin._new654("ЛІТО", MorphLang.UA, True, DatePointerType.SUMMER)
        DateItemToken.__m_seasons.add(t)
        t = Termin._new654("ОСЕНЬ", MorphLang.RU, True, DatePointerType.AUTUMN)
        DateItemToken.__m_seasons.add(t)
        t = Termin._new654("AUTUMN", MorphLang.EN, True, DatePointerType.AUTUMN)
        DateItemToken.__m_seasons.add(t)
        t = Termin._new654("ОСІНЬ", MorphLang.UA, True, DatePointerType.AUTUMN)
        DateItemToken.__m_seasons.add(t)
        DateItemToken.__m_monthes = TerminCollection()
        months = ["ЯНВАРЬ", "ФЕВРАЛЬ", "МАРТ", "АПРЕЛЬ", "МАЙ", "ИЮНЬ", "ИЮЛЬ", "АВГУСТ", "СЕНТЯБРЬ", "ОКТЯБРЬ", "НОЯБРЬ", "ДЕКАБРЬ"]
        i = 0
        while i < len(months): 
            t = Termin._new654(months[i], MorphLang.RU, True, i + 1)
            DateItemToken.__m_monthes.add(t)
            i += 1
        months = ["СІЧЕНЬ", "ЛЮТИЙ", "БЕРЕЗЕНЬ", "КВІТЕНЬ", "ТРАВЕНЬ", "ЧЕРВЕНЬ", "ЛИПЕНЬ", "СЕРПЕНЬ", "ВЕРЕСЕНЬ", "ЖОВТЕНЬ", "ЛИСТОПАД", "ГРУДЕНЬ"]
        i = 0
        while i < len(months): 
            t = Termin._new654(months[i], MorphLang.UA, True, i + 1)
            DateItemToken.__m_monthes.add(t)
            i += 1
        months = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"]
        i = 0
        while i < len(months): 
            t = Termin._new654(months[i], MorphLang.EN, True, i + 1)
            DateItemToken.__m_monthes.add(t)
            i += 1
        months = ["GENNAIO", "FEBBRAIO", "MARZO", "APRILE", "MAGGIO", "GUINGO", "LUGLIO", "AGOSTO", "SETTEMBRE", "OTTOBRE", "NOVEMBRE", "DICEMBRE"]
        i = 0
        while i < len(months): 
            t = Termin._new654(months[i], MorphLang.IT, True, i + 1)
            DateItemToken.__m_monthes.add(t)
            i += 1
        for m in ["ЯНВ", "ФЕВ", "ФЕВР", "МАР", "АПР", "ИЮН", "ИЮЛ", "АВГ", "СЕН", "СЕНТ", "ОКТ", "НОЯ", "НОЯБ", "ДЕК", "JAN", "FEB", "MAR", "APR", "JUN", "JUL", "AUG", "SEP", "SEPT", "OCT", "NOV", "DEC"]: 
            for ttt in DateItemToken.__m_monthes.termins: 
                if (ttt.terms[0].canonical_text.startswith(m)): 
                    ttt.add_abridge(m)
                    DateItemToken.__m_monthes.reindex(ttt)
                    break
        for m in ["OF"]: 
            DateItemToken.__m_monthes.add(Termin(m, MorphLang.EN, True))
        DateItemToken.__m_empty_words = dict()
        DateItemToken.__m_empty_words["IN"] = MorphLang.EN
        DateItemToken.__m_empty_words["SINCE"] = MorphLang.EN
        DateItemToken.__m_empty_words["THE"] = MorphLang.EN
        DateItemToken.__m_empty_words["NEL"] = MorphLang.IT
        DateItemToken.__m_empty_words["DEL"] = MorphLang.IT
        DateItemToken.__m_empty_words["IL"] = MorphLang.IT
        DateItemToken.DAYS_OF_WEEK = TerminCollection()
        te = Termin._new654("SUNDAY", MorphLang.EN, True, 7)
        te.add_abridge("SUN")
        te.add_variant("ВОСКРЕСЕНЬЕ", True)
        te.add_variant("ВОСКРЕСЕНИЕ", True)
        te.add_abridge("ВС")
        te.add_variant("НЕДІЛЯ", True)
        DateItemToken.DAYS_OF_WEEK.add(te)
        te = Termin._new654("MONDAY", MorphLang.EN, True, 1)
        te.add_abridge("MON")
        te.add_variant("ПОНЕДЕЛЬНИК", True)
        te.add_abridge("ПОН")
        te.add_variant("ПОНЕДІЛОК", True)
        DateItemToken.DAYS_OF_WEEK.add(te)
        te = Termin._new654("TUESDAY", MorphLang.EN, True, 2)
        te.add_abridge("TUE")
        te.add_variant("ВТОРНИК", True)
        te.add_abridge("ВТ")
        te.add_variant("ВІВТОРОК", True)
        DateItemToken.DAYS_OF_WEEK.add(te)
        te = Termin._new654("WEDNESDAY", MorphLang.EN, True, 3)
        te.add_abridge("WED")
        te.add_variant("СРЕДА", True)
        te.add_abridge("СР")
        te.add_variant("СЕРЕДА", True)
        DateItemToken.DAYS_OF_WEEK.add(te)
        te = Termin._new654("THURSDAY", MorphLang.EN, True, 4)
        te.add_abridge("THU")
        te.add_variant("ЧЕТВЕРГ", True)
        te.add_abridge("ЧТ")
        te.add_variant("ЧЕТВЕР", True)
        DateItemToken.DAYS_OF_WEEK.add(te)
        te = Termin._new654("FRIDAY", MorphLang.EN, True, 5)
        te.add_abridge("FRI")
        te.add_variant("ПЯТНИЦА", True)
        te.add_abridge("ПТ")
        te.add_variant("ПЯТНИЦЯ", True)
        DateItemToken.DAYS_OF_WEEK.add(te)
        te = Termin._new654("SATURDAY", MorphLang.EN, True, 6)
        te.add_abridge("SAT")
        te.add_variant("СУББОТА", True)
        te.add_abridge("СБ")
        te.add_variant("СУБОТА", True)
        DateItemToken.DAYS_OF_WEEK.add(te)
    
    __m_empty_words = None
    
    @staticmethod
    def __test_year_rus_word(t0 : 'Token', ignore_newline : bool=False) -> 'Token':
        tt = t0
        if (tt is None): 
            return None
        if (not ignore_newline and tt.previous is not None and tt.is_newline_before): 
            return None
        if (tt.is_value("ГОД", None) or tt.is_value("РІК", None)): 
            return tt
        if ((tt.is_value("Г", None) and tt.next0 is not None and tt.next0.is_char_of("\\/.")) and tt.next0.next0 is not None and tt.next0.next0.is_value("Б", None)): 
            return None
        if (((tt.morph.language.is_ru and ((tt.is_value("ГГ", None) or tt.is_value("Г", None))))) or ((tt.morph.language.is_ua and ((tt.is_value("Р", None) or tt.is_value("РР", None)))))): 
            if (tt.next0 is not None and tt.next0.is_char('.')): 
                tt = tt.next0
                if ((tt.next0 is not None and ((((tt.next0.is_value("Г", None) and tt.next0.morph.language.is_ru)) or ((tt.next0.morph.language.is_ua and tt.next0.is_value("Р", None))))) and tt.next0.next0 is not None) and tt.next0.next0.is_char('.')): 
                    tt = tt.next0.next0
                return tt
            else: 
                return tt
        return None
    
    @staticmethod
    def try_attach_list(t : 'Token', max_count : int=20) -> typing.List['DateItemToken']:
        """ Привязать примитивы в контейнере с указанной позиции
        
        Args:
            cnt: 
            indFrom: 
        
        Returns:
            typing.List[DateItemToken]: Список примитивов
        """
        from pullenti.ner.TextToken import TextToken
        from pullenti.morph.MorphClass import MorphClass
        from pullenti.ner.core.NumberExToken import NumberExToken
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        p = DateItemToken.try_attach(t, None)
        if (p is None): 
            return None
        if (p.typ == DateItemToken.DateItemType.DELIM): 
            return None
        res = list()
        res.append(p)
        tt = p.end_token.next0
        while tt is not None:
            if (isinstance(tt, TextToken)): 
                if ((tt if isinstance(tt, TextToken) else None).check_value(DateItemToken.__m_empty_words) is not None): 
                    tt = tt.next0
                    continue
            p0 = DateItemToken.try_attach(tt, res)
            if (p0 is None): 
                if (tt.is_newline_before): 
                    break
                if (tt.chars.is_latin_letter): 
                    break
                if (tt.morph is not None and tt.morph.check(MorphClass.ADJECTIVE | MorphClass.PRONOUN)): 
                    tt = tt.next0
                    continue
                break
            if (tt.is_newline_before): 
                if (p.typ == DateItemToken.DateItemType.MONTH and p0.can_be_year): 
                    pass
                elif (p.typ == DateItemToken.DateItemType.NUMBER and p.can_be_day and p0.typ == DateItemToken.DateItemType.MONTH): 
                    pass
                else: 
                    break
            if (p0.can_be_year and p0.typ == DateItemToken.DateItemType.NUMBER): 
                if (p.typ == DateItemToken.DateItemType.HALFYEAR or p.typ == DateItemToken.DateItemType.QUARTAL): 
                    p0.typ = DateItemToken.DateItemType.YEAR
                elif (p.typ == DateItemToken.DateItemType.POINTER and p0.int_value > 1990): 
                    p0.typ = DateItemToken.DateItemType.YEAR
            p = p0
            res.append(p)
            if (max_count > 0 and len(res) >= max_count): 
                break
            tt = p.end_token.next0
        for i in range(len(res) - 1, -1, -1):
            if (res[i].typ == DateItemToken.DateItemType.DELIM): 
                del res[i]
            else: 
                break
        if (len(res) > 0 and res[len(res) - 1].typ == DateItemToken.DateItemType.NUMBER): 
            nex = NumberExToken.try_parse_number_with_postfix(res[len(res) - 1].begin_token)
            if (nex is not None and nex.ex_typ != NumberExType.HOUR): 
                if (len(res) > 3 and res[len(res) - 2].typ == DateItemToken.DateItemType.DELIM and res[len(res) - 2].string_value == ":"): 
                    pass
                else: 
                    del res[len(res) - 1]
        if (len(res) == 0): 
            return None
        i = 1
        while i < (len(res) - 1): 
            if (res[i].typ == DateItemToken.DateItemType.DELIM and res[i].begin_token.is_comma): 
                if ((i == 1 and res[i - 1].typ == DateItemToken.DateItemType.MONTH and res[i + 1].can_be_year) and (i + 1) == (len(res) - 1)): 
                    del res[i]
            i += 1
        if (res[len(res) - 1].typ == DateItemToken.DateItemType.NUMBER): 
            rr = res[len(res) - 1]
            npt = NounPhraseHelper.try_parse(rr.begin_token, NounPhraseParseAttr.NO, 0)
            if (npt is not None and npt.end_char > rr.end_char): 
                del res[len(res) - 1]
                if (len(res) > 0 and res[len(res) - 1].typ == DateItemToken.DateItemType.DELIM): 
                    del res[len(res) - 1]
        if (len(res) == 0): 
            return None
        if (len(res) == 2 and not res[0].is_whitespace_after): 
            if (not res[0].is_whitespace_before and not res[1].is_whitespace_after): 
                return None
        return res

    
    @staticmethod
    def _new629(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'DateItemType', _arg4 : int, _arg5 : 'MorphCollection') -> 'DateItemToken':
        res = DateItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.int_value = _arg4
        res.morph = _arg5
        return res
    
    @staticmethod
    def _new630(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'DateItemType', _arg4 : int) -> 'DateItemToken':
        res = DateItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.int_value = _arg4
        return res
    
    @staticmethod
    def _new636(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'DateItemType', _arg4 : str) -> 'DateItemToken':
        res = DateItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.string_value = _arg4
        return res
    
    @staticmethod
    def _new651(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'DateItemType', _arg4 : int, _arg5 : 'MorphLang') -> 'DateItemToken':
        res = DateItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.int_value = _arg4
        res.lang = _arg5
        return res