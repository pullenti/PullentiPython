# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import datetime
import typing
from enum import IntEnum
from pullenti.unisharp.Utils import Utils
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
        YEAR = 0 + 1
        MONTH = (0 + 1) + 1
        DELIM = ((0 + 1) + 1) + 1
        HOUR = (((0 + 1) + 1) + 1) + 1
        MINUTE = ((((0 + 1) + 1) + 1) + 1) + 1
        SECOND = (((((0 + 1) + 1) + 1) + 1) + 1) + 1
        HALFYEAR = ((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1
        QUARTAL = (((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        POINTER = ((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        CENTURY = (((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        
        @classmethod
        def has_value(cls, value):
            return any(value == item.value for item in cls)
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
        self.typ = DateItemToken.DateItemType.NUMBER
        self.string_value = None;
        self.int_value = 0
        self.lang = None;
        self.new_age = 0
        self.__m_year = -1
        self.__m_can_by_month = -1
    
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
            if (self.int_value <= ((Utils.getDate(datetime.datetime.today()).year - 2000) + 5)): 
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
    def tryAttach(t : 'Token', prev : typing.List['DateItemToken']) -> 'DateItemToken':
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
        if (t0.isChar('_')): 
            t = t.next0_
            while t is not None: 
                if (t.is_newline_before): 
                    return None
                if (not t.isChar('_')): 
                    break
                t = t.next0_
        elif (BracketHelper.canBeStartOfSequence(t0, True, False)): 
            ok = False
            t = t.next0_
            while t is not None: 
                if (BracketHelper.canBeEndOfSequence(t, True, t0, False)): 
                    ok = True
                    break
                elif (not t.isChar('_')): 
                    break
                t = t.next0_
            if (not ok): 
                t = t0
            else: 
                t = t.next0_
                while t is not None: 
                    if (not t.isChar('_')): 
                        break
                    t = t.next0_
        elif ((isinstance(t0, TextToken)) and t0.isValue("THE", None)): 
            res0 = DateItemToken.__TryAttach(t.next0_, prev)
            if (res0 is not None): 
                res0.begin_token = t
                return res0
        res = DateItemToken.__TryAttach(t, prev)
        if (res is None): 
            return None
        res.begin_token = t0
        if (not res.is_whitespace_after and res.end_token.next0_ is not None and res.end_token.next0_.isChar('_')): 
            t = res.end_token.next0_
            while t is not None: 
                if (not t.isChar('_')): 
                    break
                else: 
                    res.end_token = t
                t = t.next0_
        if (res.typ == DateItemToken.DateItemType.YEAR or res.typ == DateItemToken.DateItemType.CENTURY or res.typ == DateItemToken.DateItemType.NUMBER): 
            tok = None
            ii = 0
            t = res.end_token.next0_
            if (t is not None and t.isValue("ДО", None)): 
                tok = DateItemToken.M_NEW_AGE.tryParse(t.next0_, TerminParseAttr.NO)
                ii = -1
            elif (t is not None and t.isValue("ОТ", "ВІД")): 
                tok = DateItemToken.M_NEW_AGE.tryParse(t.next0_, TerminParseAttr.NO)
                ii = 1
            else: 
                tok = DateItemToken.M_NEW_AGE.tryParse(t, TerminParseAttr.NO)
                ii = 1
            if (tok is not None): 
                res.new_age = (-1 if ii < 0 else 1)
                res.end_token = tok.end_token
                if (res.typ == DateItemToken.DateItemType.NUMBER): 
                    res.typ = DateItemToken.DateItemType.YEAR
        return res
    
    @staticmethod
    def __isNewAge(t : 'Token') -> bool:
        if (t is None): 
            return False
        if (t.isValue("ДО", None)): 
            return DateItemToken.M_NEW_AGE.tryParse(t.next0_, TerminParseAttr.NO) is not None
        elif (t.isValue("ОТ", "ВІД")): 
            return DateItemToken.M_NEW_AGE.tryParse(t.next0_, TerminParseAttr.NO) is not None
        return DateItemToken.M_NEW_AGE.tryParse(t, TerminParseAttr.NO) is not None
    
    @staticmethod
    def __TryAttach(t : 'Token', prev : typing.List['DateItemToken']) -> 'DateItemToken':
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.TextToken import TextToken
        from pullenti.morph.MorphLang import MorphLang
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.ner.date.DateRangeReferent import DateRangeReferent
        if (t is None): 
            return None
        nt = Utils.asObjectOrNull(t, NumberToken)
        begin = t
        end = t
        is_in_brack = False
        if ((BracketHelper.canBeStartOfSequence(t, False, False) and t.next0_ is not None and (isinstance(t.next0_, NumberToken))) and BracketHelper.canBeEndOfSequence(t.next0_.next0_, False, None, False)): 
            nt = (Utils.asObjectOrNull(t.next0_, NumberToken))
            end = t.next0_.next0_
            is_in_brack = True
        if ((t.is_newline_before and BracketHelper.isBracket(t, False) and (isinstance(t.next0_, NumberToken))) and BracketHelper.isBracket(t.next0_.next0_, False)): 
            nt = (Utils.asObjectOrNull(t.next0_, NumberToken))
            end = t.next0_.next0_
            is_in_brack = True
        if (nt is not None): 
            if (nt.typ == NumberSpellingType.WORDS): 
                if (nt.morph.class0_.is_noun and not nt.morph.class0_.is_adjective): 
                    if (t.next0_ is not None and ((t.next0_.isValue("КВАРТАЛ", None) or t.next0_.isValue("ПОЛУГОДИЕ", None) or t.next0_.isValue("ПІВРІЧЧЯ", None)))): 
                        pass
                    else: 
                        return None
            if (NumberHelper.tryParseAge(nt) is not None): 
                return None
            res = DateItemToken._new680(begin, end, DateItemToken.DateItemType.NUMBER, nt.value, nt.morph)
            if ((res.int_value == 20 and (isinstance(nt.next0_, NumberToken)) and nt.next0_.length_char == 2) and prev is not None): 
                num = 2000 + ((Utils.asObjectOrNull(nt.next0_, NumberToken)).value)
                if ((num < 2030) and len(prev) > 0 and prev[len(prev) - 1].typ == DateItemToken.DateItemType.MONTH): 
                    ok = False
                    if (nt.whitespaces_after_count == 1): 
                        ok = True
                    elif (nt.is_newline_after and nt.is_newline_after): 
                        ok = True
                    if (ok): 
                        nt = (Utils.asObjectOrNull(nt.next0_, NumberToken))
                        res.end_token = nt
                        res.int_value = num
            if (res.int_value == 20 or res.int_value == 201): 
                tt = t.next0_
                if (tt is not None and tt.isChar('_')): 
                    while tt is not None: 
                        if (not tt.isChar('_')): 
                            break
                        tt = tt.next0_
                    tt = DateItemToken.__testYearRusWord(tt, False)
                    if (tt is not None): 
                        res.int_value = 0
                        res.end_token = tt
                        res.typ = DateItemToken.DateItemType.YEAR
                        return res
            if (res.int_value <= 12 and t.next0_ is not None and (t.whitespaces_after_count < 3)): 
                tt = t.next0_
                if (tt.isValue("ЧАС", None)): 
                    if (((isinstance(t.previous, TextToken)) and not t.previous.chars.is_letter and not t.is_whitespace_before) and (isinstance(t.previous.previous, NumberToken)) and not t.previous.is_whitespace_before): 
                        pass
                    else: 
                        res.typ = DateItemToken.DateItemType.HOUR
                        res.end_token = tt
                        tt = tt.next0_
                        if (tt is not None and tt.isChar('.')): 
                            res.end_token = tt
                            tt = tt.next0_
                first_pass2829 = True
                while True:
                    if first_pass2829: first_pass2829 = False
                    else: tt = tt.next0_
                    if (not (tt is not None)): break
                    if (tt.isValue("УТРО", "РАНОК")): 
                        res.end_token = tt
                        res.typ = DateItemToken.DateItemType.HOUR
                        return res
                    if (tt.isValue("ВЕЧЕР", "ВЕЧІР")): 
                        res.end_token = tt
                        res.int_value += 12
                        res.typ = DateItemToken.DateItemType.HOUR
                        return res
                    if (tt.isValue("ДЕНЬ", None)): 
                        res.end_token = tt
                        if (res.int_value < 10): 
                            res.int_value += 12
                        res.typ = DateItemToken.DateItemType.HOUR
                        return res
                    if (tt.isValue("НОЧЬ", "НІЧ")): 
                        res.end_token = tt
                        if (res.int_value == 12): 
                            res.int_value = 0
                        elif (res.int_value > 9): 
                            res.int_value += 12
                        res.typ = DateItemToken.DateItemType.HOUR
                        return res
                    if (tt.is_comma or tt.morph.class0_.is_adverb): 
                        continue
                    break
                if (res.typ == DateItemToken.DateItemType.HOUR): 
                    return res
            can_be_year_ = True
            if (prev is not None and len(prev) > 0 and prev[len(prev) - 1].typ == DateItemToken.DateItemType.MONTH): 
                pass
            elif ((prev is not None and len(prev) >= 4 and prev[len(prev) - 1].typ == DateItemToken.DateItemType.DELIM) and prev[len(prev) - 2].can_by_month): 
                pass
            elif (nt.next0_ is not None and ((nt.next0_.isValue("ГОД", None) or nt.next0_.isValue("РІК", None)))): 
                if (res.int_value < 1000): 
                    can_be_year_ = False
            tt = DateItemToken.__testYearRusWord(nt.next0_, False)
            if (tt is not None and DateItemToken.__isNewAge(tt.next0_)): 
                res.typ = DateItemToken.DateItemType.YEAR
                res.end_token = tt
            elif (can_be_year_): 
                if (res.can_be_year): 
                    tt = DateItemToken.__testYearRusWord(nt.next0_, res.is_newline_before)
                    if ((tt) is not None): 
                        if ((tt.isValue("Г", None) and not tt.is_whitespace_before and t.previous is not None) and ((t.previous.isValue("КОРПУС", None) or t.previous.isValue("КОРП", None)))): 
                            pass
                        elif ((((nt.next0_.isValue("Г", None) and (t.whitespaces_before_count < 3) and t.previous is not None) and t.previous.isValue("Я", None) and t.previous.previous is not None) and t.previous.previous.isCharOf("\\/") and t.previous.previous.previous is not None) and t.previous.previous.previous.isValue("А", None)): 
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
                if (nt.previous.isValue("В", "У") or nt.previous.isValue("К", None) or nt.previous.isValue("ДО", None)): 
                    tt = DateItemToken.__testYearRusWord(nt.next0_, False)
                    if ((tt) is not None): 
                        if ((res.int_value < 100) and (isinstance(tt, TextToken)) and (((Utils.asObjectOrNull(tt, TextToken)).term == "ГОДА" or (Utils.asObjectOrNull(tt, TextToken)).term == "РОКИ"))): 
                            pass
                        else: 
                            res.end_token = tt
                            res.typ = DateItemToken.DateItemType.YEAR
                            res.lang = tt.morph.language
                            res.begin_token = nt.previous
                elif (((nt.previous.isValue("IN", None) or nt.previous.isValue("SINCE", None))) and res.can_be_year): 
                    res.typ = DateItemToken.DateItemType.YEAR
                    res.begin_token = nt.previous
                elif (nt.previous.isValue("NEL", None) or nt.previous.isValue("DEL", None)): 
                    if (res.can_be_year): 
                        res.typ = DateItemToken.DateItemType.YEAR
                        res.lang = MorphLang.IT
                        res.begin_token = nt.previous
                elif (nt.previous.isValue("IL", None) and res.can_be_day): 
                    res.lang = MorphLang.IT
                    res.begin_token = nt.previous
            t1 = res.end_token.next0_
            if (t1 is not None): 
                if ((t1.isValue("ЧАС", None) or t1.isValue("ГОДИНА", None))): 
                    if ((((prev is not None and len(prev) == 2 and prev[0].can_be_hour) and prev[1].typ == DateItemToken.DateItemType.DELIM and not prev[1].is_whitespace_after) and not prev[1].is_whitespace_after and res.int_value >= 0) and (res.int_value < 59)): 
                        prev[0].typ = DateItemToken.DateItemType.HOUR
                        res.typ = DateItemToken.DateItemType.MINUTE
                        res.end_token = t1
                    elif (res.int_value < 24): 
                        if (t1.next0_ is not None and t1.next0_.isChar('.')): 
                            t1 = t1.next0_
                        res.typ = DateItemToken.DateItemType.HOUR
                        res.end_token = t1
                elif ((res.int_value < 60) and ((t1.isValue("МИНУТА", None) or t1.isValue("МИН", None) or t.isValue("ХВИЛИНА", None)))): 
                    if (t1.next0_ is not None and t1.next0_.isChar('.')): 
                        t1 = t1.next0_
                    res.typ = DateItemToken.DateItemType.MINUTE
                    res.end_token = t1
                elif ((res.int_value < 60) and ((t1.isValue("СЕКУНДА", None) or t1.isValue("СЕК", None)))): 
                    if (t1.next0_ is not None and t1.next0_.isChar('.')): 
                        t1 = t1.next0_
                    res.typ = DateItemToken.DateItemType.SECOND
                    res.end_token = t1
                elif ((res.int_value < 30) and ((t1.isValue("ВЕК", "ВІК") or t1.isValue("СТОЛЕТИЕ", "СТОЛІТТЯ")))): 
                    res.typ = DateItemToken.DateItemType.CENTURY
                    res.end_token = t1
                elif (res.int_value <= 4 and t1.isValue("КВАРТАЛ", None)): 
                    res.typ = DateItemToken.DateItemType.QUARTAL
                    res.end_token = t1
                elif (res.int_value <= 2 and ((t1.isValue("ПОЛУГОДИЕ", None) or t1.isValue("ПІВРІЧЧЯ", None)))): 
                    res.typ = DateItemToken.DateItemType.HALFYEAR
                    res.end_token = t1
            return res
        t0 = Utils.asObjectOrNull(t, TextToken)
        if (t0 is None): 
            return None
        txt = t0.getSourceText()
        if ((txt[0] == 'I' or txt[0] == 'X' or txt[0] == 'Х') or txt[0] == 'V'): 
            lat = NumberHelper.tryParseRoman(t)
            if (lat is not None and lat.end_token.next0_ is not None): 
                tt = lat.end_token.next0_
                if (tt.isValue("КВАРТАЛ", None) and lat.value > (0) and lat.value <= (4)): 
                    return DateItemToken._new681(t, tt, DateItemToken.DateItemType.QUARTAL, lat.value)
                if (tt.isValue("ПОЛУГОДИЕ", "ПІВРІЧЧЯ") and lat.value > (0) and lat.value <= (2)): 
                    return DateItemToken._new681(t, lat.end_token.next0_, DateItemToken.DateItemType.HALFYEAR, lat.value)
                if (tt.isValue("ВЕК", "ВІК") or tt.isValue("СТОЛЕТИЕ", "СТОЛІТТЯ")): 
                    return DateItemToken._new681(t, lat.end_token.next0_, DateItemToken.DateItemType.CENTURY, lat.value)
                if (tt.isValue("В", None) and tt.next0_ is not None and tt.next0_.isChar('.')): 
                    if (prev is not None and len(prev) > 0 and prev[len(prev) - 1].typ == DateItemToken.DateItemType.POINTER): 
                        return DateItemToken._new681(t, tt.next0_, DateItemToken.DateItemType.CENTURY, lat.value)
                    if (DateItemToken.__isNewAge(tt.next0_.next0_)): 
                        return DateItemToken._new681(t, tt.next0_, DateItemToken.DateItemType.CENTURY, lat.value)
                if (tt.is_hiphen): 
                    lat2 = NumberHelper.tryParseRoman(tt.next0_)
                    if (lat2 is not None and lat2.value > lat.value and lat2.end_token.next0_ is not None): 
                        if (lat2.end_token.next0_.isValue("ВЕК", "ВІК") or lat2.end_token.next0_.isValue("СТОЛЕТИЕ", "СТОЛІТТЯ")): 
                            return DateItemToken._new681(t, lat.end_token, DateItemToken.DateItemType.CENTURY, lat.value)
        if (t is not None and t.isValue("НАПРИКІНЦІ", None)): 
            return DateItemToken._new687(t, t, DateItemToken.DateItemType.POINTER, "конец")
        if (t is not None and t.isValue("ДОНЕДАВНА", None)): 
            return DateItemToken._new687(t, t, DateItemToken.DateItemType.POINTER, "сегодня")
        tok = DateItemToken.M_SEASONS.tryParse(t, TerminParseAttr.NO)
        if ((tok is not None and (Utils.valToEnum(tok.termin.tag, DatePointerType)) == DatePointerType.SUMMER and t.morph.language.is_ru) and (isinstance(t, TextToken))): 
            str0_ = (Utils.asObjectOrNull(t, TextToken)).term
            if (str0_ != "ЛЕТОМ" and str0_ != "ЛЕТА" and str0_ != "ЛЕТО"): 
                tok = (None)
        if (tok is not None): 
            return DateItemToken._new681(t, tok.end_token, DateItemToken.DateItemType.POINTER, Utils.valToEnum(tok.termin.tag, DatePointerType))
        npt = NounPhraseHelper.tryParse(t, NounPhraseParseAttr.NO, 0)
        if (npt is not None): 
            tok = DateItemToken.M_SEASONS.tryParse(npt.end_token, TerminParseAttr.NO)
            if ((tok is not None and (Utils.valToEnum(tok.termin.tag, DatePointerType)) == DatePointerType.SUMMER and t.morph.language.is_ru) and (isinstance(t, TextToken))): 
                str0_ = (Utils.asObjectOrNull(t, TextToken)).term
                if (str0_ != "ЛЕТОМ" and str0_ != "ЛЕТА" and str0_ != "ЛЕТО"): 
                    tok = (None)
            if (tok is not None): 
                return DateItemToken._new681(t, tok.end_token, DateItemToken.DateItemType.POINTER, Utils.valToEnum(tok.termin.tag, DatePointerType))
            typ_ = DateItemToken.DateItemType.NUMBER
            if (npt.noun.isValue("КВАРТАЛ", None)): 
                typ_ = DateItemToken.DateItemType.QUARTAL
            elif (npt.end_token.isValue("ПОЛУГОДИЕ", None) or npt.end_token.isValue("ПІВРІЧЧЯ", None)): 
                typ_ = DateItemToken.DateItemType.HALFYEAR
            elif (npt.end_token.isValue("НАЧАЛО", None) or npt.end_token.isValue("ПОЧАТОК", None)): 
                return DateItemToken._new687(t, npt.end_token, DateItemToken.DateItemType.POINTER, "начало")
            elif (npt.end_token.isValue("СЕРЕДИНА", None)): 
                return DateItemToken._new687(t, npt.end_token, DateItemToken.DateItemType.POINTER, "середина")
            elif (npt.end_token.isValue("КОНЕЦ", None) or npt.end_token.isValue("КІНЕЦЬ", None) or npt.end_token.isValue("НАПРИКІНЕЦЬ", None)): 
                return DateItemToken._new687(t, npt.end_token, DateItemToken.DateItemType.POINTER, "конец")
            elif (npt.end_token.isValue("ВРЕМЯ", None) and len(npt.adjectives) > 0 and npt.end_token.previous.isValue("НАСТОЯЩЕЕ", None)): 
                return DateItemToken._new687(t, npt.end_token, DateItemToken.DateItemType.POINTER, "сегодня")
            elif (npt.end_token.isValue("ЧАС", None) and len(npt.adjectives) > 0 and npt.end_token.previous.isValue("ДАНИЙ", None)): 
                return DateItemToken._new687(t, npt.end_token, DateItemToken.DateItemType.POINTER, "сегодня")
            if (typ_ != DateItemToken.DateItemType.NUMBER): 
                delta = 0
                if (len(npt.adjectives) > 0): 
                    if (npt.adjectives[0].isValue("ПОСЛЕДНИЙ", None) or npt.adjectives[0].isValue("ОСТАННІЙ", None)): 
                        return DateItemToken._new681(t0, npt.end_token, typ_, (4 if typ_ == DateItemToken.DateItemType.QUARTAL else 2))
                    if (npt.adjectives[0].isValue("ПРЕДЫДУЩИЙ", None) or npt.adjectives[0].isValue("ПОПЕРЕДНІЙ", None)): 
                        delta = -1
                    elif (npt.adjectives[0].isValue("СЛЕДУЮЩИЙ", None) or npt.adjectives[0].isValue("ПОСЛЕДУЮЩИЙ", None) or npt.adjectives[0].isValue("НАСТУПНИЙ", None)): 
                        delta = 1
                    else: 
                        return None
                cou = 0
                tt = t.previous
                first_pass2830 = True
                while True:
                    if first_pass2830: first_pass2830 = False
                    else: tt = tt.previous
                    if (not (tt is not None)): break
                    if (cou > 200): 
                        break
                    dr = Utils.asObjectOrNull(tt.getReferent(), DateRangeReferent)
                    if (dr is None): 
                        continue
                    if (typ_ == DateItemToken.DateItemType.QUARTAL): 
                        ii = dr.quarter_number
                        if (ii < 1): 
                            continue
                        ii += delta
                        if ((ii < 1) or ii > 4): 
                            continue
                        return DateItemToken._new681(t0, npt.end_token, typ_, ii)
                    if (typ_ == DateItemToken.DateItemType.HALFYEAR): 
                        ii = dr.halfyear_number
                        if (ii < 1): 
                            continue
                        ii += delta
                        if ((ii < 1) or ii > 2): 
                            continue
                        return DateItemToken._new681(t0, npt.end_token, typ_, ii)
        term = t0.term
        if (not str.isalnum(term[0])): 
            if (t0.isCharOf(".\\/:") or t0.is_hiphen): 
                return DateItemToken._new687(t0, t0, DateItemToken.DateItemType.DELIM, term)
            elif (t0.isChar(',')): 
                return DateItemToken._new687(t0, t0, DateItemToken.DateItemType.DELIM, term)
            else: 
                return None
        if (term == "O" or term == "О"): 
            if ((isinstance(t.next0_, NumberToken)) and not t.is_whitespace_after and ((Utils.asObjectOrNull(t.next0_, NumberToken)).value < (10))): 
                return DateItemToken._new681(t, t.next0_, DateItemToken.DateItemType.NUMBER, (Utils.asObjectOrNull(t.next0_, NumberToken)).value)
        if (str.isalpha(term[0])): 
            inf = DateItemToken.M_MONTHES.tryParse(t, TerminParseAttr.NO)
            if (inf is not None and inf.termin.tag is None): 
                inf = DateItemToken.M_MONTHES.tryParse(inf.end_token.next0_, TerminParseAttr.NO)
            if (inf is not None and (isinstance(inf.termin.tag, int))): 
                return DateItemToken._new702(inf.begin_token, inf.end_token, DateItemToken.DateItemType.MONTH, inf.termin.tag, inf.termin.lang)
        return None
    
    DAYS_OF_WEEK = None
    
    M_NEW_AGE = None
    
    M_MONTHES = None
    
    M_SEASONS = None
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.core.TerminCollection import TerminCollection
        from pullenti.ner.core.Termin import Termin
        from pullenti.morph.MorphLang import MorphLang
        if (DateItemToken.M_NEW_AGE is not None): 
            return
        DateItemToken.M_NEW_AGE = TerminCollection()
        tt = Termin._new703("НОВАЯ ЭРА", MorphLang.RU, True, "НОВОЙ ЭРЫ")
        tt.addVariant("НАША ЭРА", True)
        tt.addAbridge("Н.Э.")
        DateItemToken.M_NEW_AGE.add(tt)
        tt = Termin._new703("НОВА ЕРА", MorphLang.UA, True, "НОВОЇ ЕРИ")
        tt.addVariant("НАША ЕРА", True)
        tt.addAbridge("Н.Е.")
        DateItemToken.M_NEW_AGE.add(tt)
        tt = Termin("РОЖДЕСТВО ХРИСТОВО", MorphLang.RU, True)
        tt.addAbridge("Р.Х.")
        DateItemToken.M_NEW_AGE.add(tt)
        tt = Termin("РІЗДВА ХРИСТОВОГО", MorphLang.UA, True)
        tt.addAbridge("Р.Х.")
        DateItemToken.M_NEW_AGE.add(tt)
        DateItemToken.M_SEASONS = TerminCollection()
        DateItemToken.M_SEASONS.add(Termin._new705("ЗИМА", MorphLang.RU, True, DatePointerType.WINTER))
        DateItemToken.M_SEASONS.add(Termin._new705("WINTER", MorphLang.EN, True, DatePointerType.WINTER))
        t = Termin._new705("ВЕСНА", MorphLang.RU, True, DatePointerType.SPRING)
        t.addVariant("ПРОВЕСНА", True)
        DateItemToken.M_SEASONS.add(t)
        DateItemToken.M_SEASONS.add(Termin._new705("SPRING", MorphLang.EN, True, DatePointerType.SPRING))
        t = Termin._new705("ЛЕТО", MorphLang.RU, True, DatePointerType.SUMMER)
        DateItemToken.M_SEASONS.add(t)
        t = Termin._new705("ЛІТО", MorphLang.UA, True, DatePointerType.SUMMER)
        DateItemToken.M_SEASONS.add(t)
        t = Termin._new705("ОСЕНЬ", MorphLang.RU, True, DatePointerType.AUTUMN)
        DateItemToken.M_SEASONS.add(t)
        t = Termin._new705("AUTUMN", MorphLang.EN, True, DatePointerType.AUTUMN)
        DateItemToken.M_SEASONS.add(t)
        t = Termin._new705("ОСІНЬ", MorphLang.UA, True, DatePointerType.AUTUMN)
        DateItemToken.M_SEASONS.add(t)
        DateItemToken.M_MONTHES = TerminCollection()
        months = ["ЯНВАРЬ", "ФЕВРАЛЬ", "МАРТ", "АПРЕЛЬ", "МАЙ", "ИЮНЬ", "ИЮЛЬ", "АВГУСТ", "СЕНТЯБРЬ", "ОКТЯБРЬ", "НОЯБРЬ", "ДЕКАБРЬ"]
        i = 0
        while i < len(months): 
            t = Termin._new705(months[i], MorphLang.RU, True, i + 1)
            DateItemToken.M_MONTHES.add(t)
            i += 1
        months = ["СІЧЕНЬ", "ЛЮТИЙ", "БЕРЕЗЕНЬ", "КВІТЕНЬ", "ТРАВЕНЬ", "ЧЕРВЕНЬ", "ЛИПЕНЬ", "СЕРПЕНЬ", "ВЕРЕСЕНЬ", "ЖОВТЕНЬ", "ЛИСТОПАД", "ГРУДЕНЬ"]
        i = 0
        while i < len(months): 
            t = Termin._new705(months[i], MorphLang.UA, True, i + 1)
            DateItemToken.M_MONTHES.add(t)
            i += 1
        months = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"]
        i = 0
        while i < len(months): 
            t = Termin._new705(months[i], MorphLang.EN, True, i + 1)
            DateItemToken.M_MONTHES.add(t)
            i += 1
        months = ["GENNAIO", "FEBBRAIO", "MARZO", "APRILE", "MAGGIO", "GUINGO", "LUGLIO", "AGOSTO", "SETTEMBRE", "OTTOBRE", "NOVEMBRE", "DICEMBRE"]
        i = 0
        while i < len(months): 
            t = Termin._new705(months[i], MorphLang.IT, True, i + 1)
            DateItemToken.M_MONTHES.add(t)
            i += 1
        for m in ["ЯНВ", "ФЕВ", "ФЕВР", "МАР", "АПР", "ИЮН", "ИЮЛ", "АВГ", "СЕН", "СЕНТ", "ОКТ", "НОЯ", "НОЯБ", "ДЕК", "JAN", "FEB", "MAR", "APR", "JUN", "JUL", "AUG", "SEP", "SEPT", "OCT", "NOV", "DEC"]: 
            for ttt in DateItemToken.M_MONTHES.termins: 
                if (ttt.terms[0].canonical_text.startswith(m)): 
                    ttt.addAbridge(m)
                    DateItemToken.M_MONTHES.reindex(ttt)
                    break
        for m in ["OF"]: 
            DateItemToken.M_MONTHES.add(Termin(m, MorphLang.EN, True))
        DateItemToken.M_EMPTY_WORDS = dict()
        DateItemToken.M_EMPTY_WORDS["IN"] = MorphLang.EN
        DateItemToken.M_EMPTY_WORDS["SINCE"] = MorphLang.EN
        DateItemToken.M_EMPTY_WORDS["THE"] = MorphLang.EN
        DateItemToken.M_EMPTY_WORDS["NEL"] = MorphLang.IT
        DateItemToken.M_EMPTY_WORDS["DEL"] = MorphLang.IT
        DateItemToken.M_EMPTY_WORDS["IL"] = MorphLang.IT
        DateItemToken.DAYS_OF_WEEK = TerminCollection()
        te = Termin._new705("SUNDAY", MorphLang.EN, True, 7)
        te.addAbridge("SUN")
        te.addVariant("ВОСКРЕСЕНЬЕ", True)
        te.addVariant("ВОСКРЕСЕНИЕ", True)
        te.addAbridge("ВС")
        te.addVariant("НЕДІЛЯ", True)
        DateItemToken.DAYS_OF_WEEK.add(te)
        te = Termin._new705("MONDAY", MorphLang.EN, True, 1)
        te.addAbridge("MON")
        te.addVariant("ПОНЕДЕЛЬНИК", True)
        te.addAbridge("ПОН")
        te.addVariant("ПОНЕДІЛОК", True)
        DateItemToken.DAYS_OF_WEEK.add(te)
        te = Termin._new705("TUESDAY", MorphLang.EN, True, 2)
        te.addAbridge("TUE")
        te.addVariant("ВТОРНИК", True)
        te.addAbridge("ВТ")
        te.addVariant("ВІВТОРОК", True)
        DateItemToken.DAYS_OF_WEEK.add(te)
        te = Termin._new705("WEDNESDAY", MorphLang.EN, True, 3)
        te.addAbridge("WED")
        te.addVariant("СРЕДА", True)
        te.addAbridge("СР")
        te.addVariant("СЕРЕДА", True)
        DateItemToken.DAYS_OF_WEEK.add(te)
        te = Termin._new705("THURSDAY", MorphLang.EN, True, 4)
        te.addAbridge("THU")
        te.addVariant("ЧЕТВЕРГ", True)
        te.addAbridge("ЧТ")
        te.addVariant("ЧЕТВЕР", True)
        DateItemToken.DAYS_OF_WEEK.add(te)
        te = Termin._new705("FRIDAY", MorphLang.EN, True, 5)
        te.addAbridge("FRI")
        te.addVariant("ПЯТНИЦА", True)
        te.addAbridge("ПТ")
        te.addVariant("ПЯТНИЦЯ", True)
        DateItemToken.DAYS_OF_WEEK.add(te)
        te = Termin._new705("SATURDAY", MorphLang.EN, True, 6)
        te.addAbridge("SAT")
        te.addVariant("СУББОТА", True)
        te.addAbridge("СБ")
        te.addVariant("СУБОТА", True)
        DateItemToken.DAYS_OF_WEEK.add(te)
    
    M_EMPTY_WORDS = None
    
    @staticmethod
    def __testYearRusWord(t0 : 'Token', ignore_newline : bool=False) -> 'Token':
        tt = t0
        if (tt is None): 
            return None
        if (not ignore_newline and tt.previous is not None and tt.is_newline_before): 
            return None
        if (tt.isValue("ГОД", None) or tt.isValue("РІК", None)): 
            return tt
        if ((tt.isValue("Г", None) and tt.next0_ is not None and tt.next0_.isCharOf("\\/.")) and tt.next0_.next0_ is not None and tt.next0_.next0_.isValue("Б", None)): 
            return None
        if (((tt.morph.language.is_ru and ((tt.isValue("ГГ", None) or tt.isValue("Г", None))))) or ((tt.morph.language.is_ua and ((tt.isValue("Р", None) or tt.isValue("РР", None)))))): 
            if (tt.next0_ is not None and tt.next0_.isChar('.')): 
                tt = tt.next0_
                if ((tt.next0_ is not None and (tt.whitespaces_after_count < 4) and ((((tt.next0_.isValue("Г", None) and tt.next0_.morph.language.is_ru)) or ((tt.next0_.morph.language.is_ua and tt.next0_.isValue("Р", None)))))) and tt.next0_.next0_ is not None and tt.next0_.next0_.isChar('.')): 
                    tt = tt.next0_.next0_
                return tt
            else: 
                return tt
        return None
    
    @staticmethod
    def tryAttachList(t : 'Token', max_count : int=20) -> typing.List['DateItemToken']:
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
        p = DateItemToken.tryAttach(t, None)
        if (p is None): 
            return None
        if (p.typ == DateItemToken.DateItemType.DELIM): 
            return None
        res = list()
        res.append(p)
        tt = p.end_token.next0_
        while tt is not None:
            if (isinstance(tt, TextToken)): 
                if ((Utils.asObjectOrNull(tt, TextToken)).checkValue(DateItemToken.M_EMPTY_WORDS) is not None): 
                    tt = tt.next0_
                    continue
            p0 = DateItemToken.tryAttach(tt, res)
            if (p0 is None): 
                if (tt.is_newline_before): 
                    break
                if (tt.chars.is_latin_letter): 
                    break
                if (tt.morph is not None and tt.morph.check((MorphClass.ADJECTIVE) | MorphClass.PRONOUN)): 
                    tt = tt.next0_
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
            tt = p.end_token.next0_
        for i in range(len(res) - 1, -1, -1):
            if (res[i].typ == DateItemToken.DateItemType.DELIM): 
                del res[i]
            else: 
                break
        if (len(res) > 0 and res[len(res) - 1].typ == DateItemToken.DateItemType.NUMBER): 
            nex = NumberExToken.tryParseNumberWithPostfix(res[len(res) - 1].begin_token)
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
            npt = NounPhraseHelper.tryParse(rr.begin_token, NounPhraseParseAttr.NO, 0)
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
    def _new680(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'DateItemType', _arg4 : int, _arg5 : 'MorphCollection') -> 'DateItemToken':
        res = DateItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.int_value = _arg4
        res.morph = _arg5
        return res
    
    @staticmethod
    def _new681(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'DateItemType', _arg4 : int) -> 'DateItemToken':
        res = DateItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.int_value = _arg4
        return res
    
    @staticmethod
    def _new687(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'DateItemType', _arg4 : str) -> 'DateItemToken':
        res = DateItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.string_value = _arg4
        return res
    
    @staticmethod
    def _new702(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'DateItemType', _arg4 : int, _arg5 : 'MorphLang') -> 'DateItemToken':
        res = DateItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.int_value = _arg4
        res.lang = _arg5
        return res