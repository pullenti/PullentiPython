﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import typing
import io
from pullenti.unisharp.Utils import Utils
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.core.internal.SerializerHelper import SerializerHelper


class Token:
    """ Базовый класс для всех токенов """
    
    def __init__(self, kit_ : 'AnalysisKit', begin : int, end : int) -> None:
        self.kit = None;
        self.begin_char = 0
        self.end_char = 0
        self.tag = None;
        self._m_previous = None;
        self._m_next = None;
        self.__m_morph = None;
        self.chars = None;
        self.__m_attrs = 0
        self.kit = kit_
        self.begin_char = begin
        self.end_char = end
    
    @property
    def length_char(self) -> int:
        """ Длина в исходных символах """
        return (self.end_char - self.begin_char) + 1
    
    @property
    def previous(self) -> 'Token':
        """ Предыдущий токен """
        return self._m_previous
    @previous.setter
    def previous(self, value) -> 'Token':
        self._m_previous = value
        if (value is not None): 
            value._m_next = self
        self.__m_attrs = (0)
        return value
    
    @property
    def next0_(self) -> 'Token':
        """ Следующий токен """
        return self._m_next
    @next0_.setter
    def next0_(self, value) -> 'Token':
        self._m_next = value
        if (value is not None): 
            value._m_previous = self
        self.__m_attrs = (0)
        return value
    
    @property
    def morph(self) -> 'MorphCollection':
        """ Морфологическая информация """
        from pullenti.ner.MorphCollection import MorphCollection
        if (self.__m_morph is None): 
            self.__m_morph = MorphCollection()
        return self.__m_morph
    @morph.setter
    def morph(self, value) -> 'MorphCollection':
        self.__m_morph = value
        return value
    
    def __str__(self) -> str:
        return self.kit.sofa.text[self.begin_char:self.begin_char+(self.end_char + 1) - self.begin_char]
    
    def __getAttr(self, i : int) -> bool:
        if ((((self.__m_attrs) & 1)) == 0): 
            self.__m_attrs = (1)
            if (self._m_previous is None): 
                self._setAttr(1, True)
                self._setAttr(3, True)
            else: 
                j = self._m_previous.end_char + 1
                while j < self.begin_char: 
                    ch = self.kit.sofa.text[j]
                    if (Utils.isWhitespace((ch))): 
                        self._setAttr(1, True)
                        if ((ord(ch)) == 0xD or (ord(ch)) == 0xA or ch == '\f'): 
                            self._setAttr(3, True)
                    j += 1
            if (self._m_next is None): 
                self._setAttr(2, True)
                self._setAttr(4, True)
            else: 
                j = self.end_char + 1
                while j < self._m_next.begin_char: 
                    ch = self.kit.sofa.text[j]
                    if (Utils.isWhitespace(ch)): 
                        self._setAttr(2, True)
                        if ((ord(ch)) == 0xD or (ord(ch)) == 0xA or ch == '\f'): 
                            self._setAttr(4, True)
                    j += 1
        return (((((self.__m_attrs) >> i)) & 1)) != 0
    
    def _setAttr(self, i : int, val : bool) -> None:
        if (val): 
            self.__m_attrs |= ((1 << i))
        else: 
            self.__m_attrs &= (~ ((1 << i)))
    
    @property
    def is_whitespace_before(self) -> bool:
        """ Наличие пробельных символов перед """
        return self.__getAttr(1)
    @is_whitespace_before.setter
    def is_whitespace_before(self, value) -> bool:
        self._setAttr(1, value)
        return value
    
    @property
    def is_whitespace_after(self) -> bool:
        """ Наличие пробельных символов после """
        return self.__getAttr(2)
    @is_whitespace_after.setter
    def is_whitespace_after(self, value) -> bool:
        self._setAttr(2, value)
        return value
    
    @property
    def is_newline_before(self) -> bool:
        """ Элемент начинается с новой строки.
         Для 1-го элемента всегда true. """
        return self.__getAttr(3)
    @is_newline_before.setter
    def is_newline_before(self, value) -> bool:
        self._setAttr(3, value)
        return value
    
    @property
    def is_newline_after(self) -> bool:
        """ Элемент заканчивает строку.
         Для последнего элемента всегда true. """
        return self.__getAttr(4)
    @is_newline_after.setter
    def is_newline_after(self, value) -> bool:
        self._setAttr(4, value)
        return value
    
    @property
    def inner_bool(self) -> bool:
        """ Это используется внутренним образом """
        return self.__getAttr(5)
    @inner_bool.setter
    def inner_bool(self, value) -> bool:
        self._setAttr(5, value)
        return value
    
    @property
    def not_noun_phrase(self) -> bool:
        """ Это используется внутренним образом 
         (признак того, что здесь не начинается именная группа, чтобы повторно не пытаться выделять) """
        return self.__getAttr(6)
    @not_noun_phrase.setter
    def not_noun_phrase(self, value) -> bool:
        self._setAttr(6, value)
        return value
    
    @property
    def whitespaces_before_count(self) -> int:
        """ Количество пробелов перед, переход на новую строку = 10, табуляция = 5 """
        if (self.previous is None): 
            return 100
        if ((self.previous.end_char + 1) == self.begin_char): 
            return 0
        return self.__calcWhitespaces(self.previous.end_char + 1, self.begin_char - 1)
    
    @property
    def newlines_before_count(self) -> int:
        """ Количество переходов на новую строку перед """
        ch0 = chr(0)
        res = 0
        txt = self.kit.sofa.text
        for p in range(self.begin_char - 1, -1, -1):
            ch = txt[p]
            if ((ord(ch)) == 0xA): 
                res += 1
            elif ((ord(ch)) == 0xD and (ord(ch0)) != 0xA): 
                res += 1
            elif (ch == '\f'): 
                res += 10
            elif (not Utils.isWhitespace(ch)): 
                break
            ch0 = ch
        return res
    
    @property
    def newlines_after_count(self) -> int:
        """ Количество переходов на новую строку перед """
        ch0 = chr(0)
        res = 0
        txt = self.kit.sofa.text
        p = self.end_char + 1
        while p < len(txt): 
            ch = txt[p]
            if ((ord(ch)) == 0xD): 
                res += 1
            elif ((ord(ch)) == 0xA and (ord(ch0)) != 0xD): 
                res += 1
            elif (ch == '\f'): 
                res += 10
            elif (not Utils.isWhitespace(ch)): 
                break
            ch0 = ch
            p += 1
        return res
    
    @property
    def whitespaces_after_count(self) -> int:
        """ Количество пробелов перед, переход на новую строку = 10, табуляция = 5 """
        if (self.next0_ is None): 
            return 100
        if ((self.end_char + 1) == self.next0_.begin_char): 
            return 0
        return self.__calcWhitespaces(self.end_char + 1, self.next0_.begin_char - 1)
    
    def __calcWhitespaces(self, p0 : int, p1 : int) -> int:
        if ((p0 < 0) or p0 > p1 or p1 >= len(self.kit.sofa.text)): 
            return -1
        res = 0
        i = p0
        while i <= p1: 
            ch = self.kit.getTextCharacter(i)
            if (ch == '\r' or ch == '\n'): 
                res += 10
                ch1 = self.kit.getTextCharacter(i + 1)
                if (ch != ch1 and ((ch1 == '\r' or ch1 == '\n'))): 
                    i += 1
            elif (ch == '\t'): 
                res += 5
            elif (ch == '\u0007'): 
                res += 100
            elif (ch == '\f'): 
                res += 100
            else: 
                res += 1
            i += 1
        return res
    
    @property
    def is_hiphen(self) -> bool:
        """ Это символ переноса """
        ch = self.kit.sofa.text[self.begin_char]
        return LanguageHelper.isHiphen(ch)
    
    @property
    def is_table_control_char(self) -> bool:
        """ Это спец-символы для табличных элементов (7h, 1Eh, 1Fh) """
        ch = self.kit.sofa.text[self.begin_char]
        return (ord(ch)) == 7 or (ord(ch)) == 0x1F or (ord(ch)) == 0x1E
    
    @property
    def is_and(self) -> bool:
        """ Это соединительный союз И (на всех языках) """
        from pullenti.ner.TextToken import TextToken
        if (not self.morph.class0_.is_conjunction): 
            if (self.length_char == 1 and self.isChar('&')): 
                return True
            return False
        tt = Utils.asObjectOrNull(self, TextToken)
        if (tt is None): 
            return False
        val = tt.term
        if (val == "И" or val == "AND" or val == "UND"): 
            return True
        if (tt.morph.language.is_ua): 
            if (val == "І" or val == "ТА"): 
                return True
        return False
    
    @property
    def is_or(self) -> bool:
        """ Это соединительный союз ИЛИ (на всех языках) """
        from pullenti.ner.TextToken import TextToken
        if (not self.morph.class0_.is_conjunction): 
            return False
        tt = Utils.asObjectOrNull(self, TextToken)
        if (tt is None): 
            return False
        val = tt.term
        if (val == "ИЛИ" or val == "OR"): 
            return True
        if (tt.morph.language.is_ua): 
            if (val == "АБО"): 
                return True
        return False
    
    @property
    def is_comma(self) -> bool:
        """ Это запятая """
        return self.isChar(',')
    
    @property
    def is_comma_and(self) -> bool:
        """ Это запятая или союз И """
        return self.is_comma or self.is_and
    
    def isChar(self, ch : 'char') -> bool:
        """ Токен состоит из символа
        
        Args:
            ch('char'): проверяемый символ
        
        """
        return self.kit.sofa.text[self.begin_char] == ch
    
    def isCharOf(self, chars_ : str) -> bool:
        """ Токен состоит из одного символа, который есть в указанной строке
        
        Args:
            chars_(str): строка возможных символов
        
        """
        from pullenti.ner.ReferentToken import ReferentToken
        if (isinstance(self, ReferentToken)): 
            return False
        return chars_.find(self.kit.sofa.text[self.begin_char]) >= 0
    
    def isValue(self, term : str, termua : str=None) -> bool:
        from pullenti.ner.MetaToken import MetaToken
        if (isinstance(self, MetaToken)): 
            return (Utils.asObjectOrNull(self, MetaToken)).begin_token.isValue(term, termua)
        return False
    
    @property
    def is_letters(self) -> bool:
        """ Признак того, что это буквенный текстовой токен (TextToken) """
        from pullenti.ner.TextToken import TextToken
        tt = Utils.asObjectOrNull(self, TextToken)
        if (tt is None): 
            return False
        return str.isalpha(tt.term[0])
    
    @property
    def is_number(self) -> bool:
        """ Это число (в различных вариантах задания) """
        return False
    
    @property
    def is_referent(self) -> bool:
        """ Это сущность (Referent) """
        return False
    
    def getReferent(self) -> 'Referent':
        """ Ссылка на сущность (для ReferentToken) """
        from pullenti.ner.ReferentToken import ReferentToken
        if (not ((isinstance(self, ReferentToken)))): 
            return None
        return (Utils.asObjectOrNull(self, ReferentToken)).referent
    
    def getReferents(self) -> typing.List['Referent']:
        """ Получить список ссылок на все сущности, скрывающиеся под элементом
         (дело в том, что одни сущности могут поглощать дркгие, например, адрес поглотит город)
        
        """
        from pullenti.ner.MetaToken import MetaToken
        from pullenti.ner.ReferentToken import ReferentToken
        rt = Utils.asObjectOrNull(self, MetaToken)
        if (rt is None): 
            return None
        res = list()
        if ((isinstance(rt, ReferentToken)) and (Utils.asObjectOrNull(rt, ReferentToken)).referent is not None): 
            res.append((Utils.asObjectOrNull(rt, ReferentToken)).referent)
        t = rt.begin_token
        first_pass3178 = True
        while True:
            if first_pass3178: first_pass3178 = False
            else: t = t.next0_
            if (not (t is not None and t.end_char <= self.end_char)): break
            li = t.getReferents()
            if (li is None): 
                continue
            for r in li: 
                if (not r in res): 
                    res.append(r)
        return res
    
    def getNormalCaseText(self, mc : 'MorphClass'=MorphClass(), single_number : bool=False, gender : 'MorphGender'=MorphGender.UNDEFINED, keep_chars : bool=False) -> str:
        """ Получить связанный с токеном текст в именительном падеже
        
        Args:
            mc(MorphClass): 
            single_number(bool): переводить ли в единственное число
        
        """
        return str(self)
    
    def getSourceText(self) -> str:
        """ Получить чистый фрагмент исходного текста
        
        """
        len0_ = (self.end_char + 1) - self.begin_char
        if ((len0_ < 1) or (self.begin_char < 0)): 
            return None
        if ((self.begin_char + len0_) > len(self.kit.sofa.text)): 
            return None
        return self.kit.sofa.text[self.begin_char:self.begin_char+len0_]
    
    def getMorphClassInDictionary(self) -> 'MorphClass':
        """ Проверка, что это текстовый токен и есть в словаре соотв. тип
        
        Args:
            cla: 
        
        """
        from pullenti.ner.TextToken import TextToken
        from pullenti.morph.MorphWordForm import MorphWordForm
        tt = Utils.asObjectOrNull(self, TextToken)
        if (tt is None): 
            return self.morph.class0_
        res = MorphClass()
        for wf in tt.morph.items: 
            if ((isinstance(wf, MorphWordForm)) and (Utils.asObjectOrNull(wf, MorphWordForm)).is_in_dictionary): 
                res |= wf.class0_
        return res
    
    def _serialize(self, stream : io.IOBase) -> None:
        from pullenti.ner.MorphCollection import MorphCollection
        SerializerHelper.serializeInt(stream, self.begin_char)
        SerializerHelper.serializeInt(stream, self.end_char)
        SerializerHelper.serializeInt(stream, self.__m_attrs)
        SerializerHelper.serializeInt(stream, self.chars.value)
        if (self.__m_morph is None): 
            self.__m_morph = MorphCollection()
        self.__m_morph._serialize(stream)
    
    def _deserialize(self, stream : io.IOBase, kit_ : 'AnalysisKit') -> None:
        from pullenti.morph.CharsInfo import CharsInfo
        from pullenti.ner.MorphCollection import MorphCollection
        self.kit = kit_
        self.begin_char = SerializerHelper.deserializeInt(stream)
        self.end_char = SerializerHelper.deserializeInt(stream)
        self.__m_attrs = (SerializerHelper.deserializeInt(stream))
        self.chars = CharsInfo._new2668(SerializerHelper.deserializeInt(stream))
        self.__m_morph = MorphCollection()
        self.__m_morph._deserialize(stream)