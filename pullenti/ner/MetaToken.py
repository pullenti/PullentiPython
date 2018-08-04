# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import typing
from pullenti.ntopy.Utils import Utils
from pullenti.ner.Token import Token
from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.core.GetTextAttr import GetTextAttr


class MetaToken(Token):
    """ Токен - надстройка над диапазоном других токенов """
    
    def __init__(self, begin : 'Token', end : 'Token', kit_ : 'AnalysisKit'=None) -> None:
        self._m_begin_token = None
        self._m_end_token = None
        super().__init__(Utils.ifNotNull(kit_, begin.kit), (0 if begin is None else begin.begin_char), (0 if end is None else end.end_char))
        if (begin == self or end == self): 
            pass
        self._m_begin_token = begin
        self._m_end_token = end
        if (begin is None or end is None): 
            return
        self.chars = begin.chars
        if (begin != end): 
            t = begin.next0_
            while t is not None: 
                if (t.chars.is_letter): 
                    if (self.chars.is_capital_upper and t.chars.is_all_lower): 
                        pass
                    else: 
                        self.chars &= t.chars
                if (t == end): 
                    break
                t = t.next0_
    
    def __refresh_chars_info(self) -> None:
        if (self._m_begin_token is None): 
            return
        self.chars = self._m_begin_token.chars
        cou = 0
        if (self._m_begin_token != self._m_end_token and self._m_end_token is not None): 
            t = self._m_begin_token.next0_
            while t is not None: 
                cou += 1
                if ((cou) > 100): 
                    break
                if (t.end_char > self._m_end_token.end_char): 
                    break
                if (t.chars.is_letter): 
                    self.chars &= t.chars
                if (t == self._m_end_token): 
                    break
                t = t.next0_
    
    @property
    def begin_token(self) -> 'Token':
        """ Начальный токен диапазона """
        return self._m_begin_token
    
    @begin_token.setter
    def begin_token(self, value) -> 'Token':
        if (self._m_begin_token != value): 
            if (self._m_begin_token == self): 
                pass
            else: 
                self._m_begin_token = value
                if (value is not None): 
                    self.begin_char = self._m_begin_token.begin_char
                self.__refresh_chars_info()
        return value
    
    @property
    def end_token(self) -> 'Token':
        """ Конечный токен диапазона """
        return self._m_end_token
    
    @end_token.setter
    def end_token(self, value) -> 'Token':
        if (self._m_end_token != value): 
            if (self._m_end_token == self): 
                pass
            else: 
                self._m_end_token = value
                if (value is not None): 
                    self.end_char = self._m_end_token.end_char
                self.__refresh_chars_info()
        return value
    
    @property
    def tokens_count(self) -> int:
        """ Количество токенов в диапазоне """
        count = 1
        t = self._m_begin_token
        while t != self._m_end_token and t is not None: 
            if (count > 1 and t == self._m_begin_token): 
                break
            count += 1
            t = t.next0_
        return count
    
    @property
    def is_whitespace_before(self) -> bool:
        return self._m_begin_token.is_whitespace_before
    
    @property
    def is_whitespace_after(self) -> bool:
        return self._m_end_token.is_whitespace_after
    
    @property
    def is_newline_before(self) -> bool:
        return self._m_begin_token.is_newline_before
    
    @property
    def is_newline_after(self) -> bool:
        return self._m_end_token.is_newline_after
    
    @property
    def whitespaces_before_count(self) -> int:
        return self._m_begin_token.whitespaces_before_count
    
    @property
    def whitespaces_after_count(self) -> int:
        return self._m_end_token.whitespaces_after_count
    
    def __str__(self) -> str:
        res = Utils.newStringIO(None)
        t = self._m_begin_token
        while t is not None: 
            if (res.tell() > 0 and t.is_whitespace_before): 
                print(' ', end="", file=res)
            print(t.get_source_text(), end="", file=res)
            if (t == self._m_end_token): 
                break
            t = t.next0_
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def check(li : typing.List['ReferentToken']) -> bool:
        if (li is None or (len(li) < 1)): 
            return False
        i = 0
        while i < (len(li) - 1): 
            if (li[i].begin_char > li[i].end_char): 
                return False
            if (li[i].end_char >= li[i + 1].begin_char): 
                return False
            i += 1
        if (li[i].begin_char > li[i].end_char): 
            return False
        return True
    
    def get_normal_case_text(self, mc : 'MorphClass'=MorphClass(), single_number : bool=False, gender : 'MorphGender'=MorphGender.UNDEFINED, keep_chars : bool=False) -> str:
        from pullenti.ner.core.MiscHelper import MiscHelper
        attr = GetTextAttr.NO
        if (single_number): 
            attr = Utils.valToEnum(attr | GetTextAttr.FIRSTNOUNGROUPTONOMINATIVESINGLE, GetTextAttr)
        else: 
            attr = Utils.valToEnum(attr | GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE, GetTextAttr)
        if (keep_chars): 
            attr = Utils.valToEnum(attr | GetTextAttr.KEEPREGISTER, GetTextAttr)
        if (self.begin_token == self.end_token): 
            return self.begin_token.get_normal_case_text(mc, single_number, gender, keep_chars)
        else: 
            return MiscHelper.get_text_value(self.begin_token, self.end_token, attr)

    
    @staticmethod
    def _new590(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'MorphCollection') -> 'MetaToken':
        res = MetaToken(_arg1, _arg2)
        res.morph = _arg3
        return res
    
    @staticmethod
    def _new825(_arg1 : 'Token', _arg2 : 'Token', _arg3 : object) -> 'MetaToken':
        res = MetaToken(_arg1, _arg2)
        res.tag = _arg3
        return res
    
    @staticmethod
    def _new2174(_arg1 : 'Token', _arg2 : 'Token', _arg3 : object, _arg4 : 'MorphCollection') -> 'MetaToken':
        res = MetaToken(_arg1, _arg2)
        res.tag = _arg3
        res.morph = _arg4
        return res