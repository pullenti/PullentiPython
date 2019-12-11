# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
from pullenti.unisharp.Utils import Utils

class MorphClass:
    """ Часть речи """
    
    def __init__(self, val : 'MorphClass'=None) -> None:
        self.value = 0
        self.value = (0)
        if (val is not None): 
            self.value = val.value
    
    def __get_value(self, i : int) -> bool:
        return (((((self.value) >> i)) & 1)) != 0
    
    def __set_value(self, i : int, val : bool) -> None:
        if (val): 
            self.value |= ((1 << i))
        else: 
            self.value &= (~ ((1 << i)))
    
    @property
    def is_undefined(self) -> bool:
        """ Неопределённый тип """
        return self.value == (0)
    @is_undefined.setter
    def is_undefined(self, value_) -> bool:
        self.value = (0)
        return value_
    
    @property
    def is_noun(self) -> bool:
        """ Существительное """
        return self.__get_value(0)
    @is_noun.setter
    def is_noun(self, value_) -> bool:
        if (value_): 
            self.value = (0)
        self.__set_value(0, value_)
        return value_
    
    @staticmethod
    def is_noun_int(val : int) -> bool:
        return ((val & 1)) != 0
    
    @property
    def is_adjective(self) -> bool:
        """ Прилагательное """
        return self.__get_value(1)
    @is_adjective.setter
    def is_adjective(self, value_) -> bool:
        if (value_): 
            self.value = (0)
        self.__set_value(1, value_)
        return value_
    
    @staticmethod
    def is_adjective_int(val : int) -> bool:
        return ((val & 2)) != 0
    
    @property
    def is_verb(self) -> bool:
        """ Глагол """
        return self.__get_value(2)
    @is_verb.setter
    def is_verb(self, value_) -> bool:
        if (value_): 
            self.value = (0)
        self.__set_value(2, value_)
        return value_
    
    @staticmethod
    def is_verb_int(val : int) -> bool:
        return ((val & 4)) != 0
    
    @property
    def is_adverb(self) -> bool:
        """ Наречие """
        return self.__get_value(3)
    @is_adverb.setter
    def is_adverb(self, value_) -> bool:
        if (value_): 
            self.value = (0)
        self.__set_value(3, value_)
        return value_
    
    @staticmethod
    def is_adverb_int(val : int) -> bool:
        return ((val & 8)) != 0
    
    @property
    def is_pronoun(self) -> bool:
        """ Местоимение """
        return self.__get_value(4)
    @is_pronoun.setter
    def is_pronoun(self, value_) -> bool:
        if (value_): 
            self.value = (0)
        self.__set_value(4, value_)
        return value_
    
    @staticmethod
    def is_pronoun_int(val : int) -> bool:
        return ((val & 0x10)) != 0
    
    @property
    def is_misc(self) -> bool:
        """ Всякая ерунда (частицы, междометия) """
        return self.__get_value(5)
    @is_misc.setter
    def is_misc(self, value_) -> bool:
        if (value_): 
            self.value = (0)
        self.__set_value(5, value_)
        return value_
    
    @staticmethod
    def is_misc_int(val : int) -> bool:
        return ((val & 0x20)) != 0
    
    @property
    def is_preposition(self) -> bool:
        """ Предлог """
        return self.__get_value(6)
    @is_preposition.setter
    def is_preposition(self, value_) -> bool:
        self.__set_value(6, value_)
        return value_
    
    @staticmethod
    def is_preposition_int(val : int) -> bool:
        return ((val & 0x40)) != 0
    
    @property
    def is_conjunction(self) -> bool:
        """ Союз """
        return self.__get_value(7)
    @is_conjunction.setter
    def is_conjunction(self, value_) -> bool:
        self.__set_value(7, value_)
        return value_
    
    @staticmethod
    def is_conjunction_int(val : int) -> bool:
        return ((val & 0x80)) != 0
    
    @property
    def is_proper(self) -> bool:
        """ Собственное имя (фамилия, имя, отчество, геогр.название и др.) """
        return self.__get_value(8)
    @is_proper.setter
    def is_proper(self, value_) -> bool:
        self.__set_value(8, value_)
        return value_
    
    @staticmethod
    def is_proper_int(val : int) -> bool:
        return ((val & 0x100)) != 0
    
    @property
    def is_proper_surname(self) -> bool:
        """ Фамилия """
        return self.__get_value(9)
    @is_proper_surname.setter
    def is_proper_surname(self, value_) -> bool:
        if (value_): 
            self.is_proper = True
        self.__set_value(9, value_)
        return value_
    
    @staticmethod
    def is_proper_surname_int(val : int) -> bool:
        return ((val & 0x200)) != 0
    
    @property
    def is_proper_name(self) -> bool:
        """ Фамилия """
        return self.__get_value(10)
    @is_proper_name.setter
    def is_proper_name(self, value_) -> bool:
        if (value_): 
            self.is_proper = True
        self.__set_value(10, value_)
        return value_
    
    @staticmethod
    def is_proper_name_int(val : int) -> bool:
        return ((val & 0x400)) != 0
    
    @property
    def is_proper_secname(self) -> bool:
        """ Отчество """
        return self.__get_value(11)
    @is_proper_secname.setter
    def is_proper_secname(self, value_) -> bool:
        if (value_): 
            self.is_proper = True
        self.__set_value(11, value_)
        return value_
    
    @staticmethod
    def is_proper_secname_int(val : int) -> bool:
        return ((val & 0x800)) != 0
    
    @property
    def is_proper_geo(self) -> bool:
        """ Географическое название """
        return self.__get_value(12)
    @is_proper_geo.setter
    def is_proper_geo(self, value_) -> bool:
        if (value_): 
            self.is_proper = True
        self.__set_value(12, value_)
        return value_
    
    @staticmethod
    def is_proper_geo_int(val : int) -> bool:
        return ((val & 0x1000)) != 0
    
    @property
    def is_personal_pronoun(self) -> bool:
        """ Личное местоимение (я, мой, ты, он ...) """
        return self.__get_value(13)
    @is_personal_pronoun.setter
    def is_personal_pronoun(self, value_) -> bool:
        self.__set_value(13, value_)
        return value_
    
    @staticmethod
    def is_personal_pronoun_int(val : int) -> bool:
        return ((val & 0x2000)) != 0
    
    __m_names = None
    
    def __str__(self) -> str:
        tmp_str = io.StringIO()
        i = 0
        first_pass2899 = True
        while True:
            if first_pass2899: first_pass2899 = False
            else: i += 1
            if (not (i < len(MorphClass.__m_names))): break
            if (self.__get_value(i)): 
                if (i == 5): 
                    if (self.is_conjunction or self.is_preposition or self.is_proper): 
                        continue
                if (tmp_str.tell() > 0): 
                    print("|", end="", file=tmp_str)
                print(MorphClass.__m_names[i], end="", file=tmp_str)
        return Utils.toStringStringIO(tmp_str)
    
    def equals(self, obj : object) -> bool:
        if (not ((isinstance(obj, MorphClass)))): 
            return False
        return self.value == (obj).value
    
    def __hash__(self) -> int:
        return self.value
    
    def __and__(self : 'MorphClass', arg2 : 'MorphClass') -> 'MorphClass':
        val1 = 0
        val2 = 0
        if (self is not None): 
            val1 = self.value
        if (arg2 is not None): 
            val2 = arg2.value
        return MorphClass._new79(((val1) & (val2)))
    
    def __or__(self : 'MorphClass', arg2 : 'MorphClass') -> 'MorphClass':
        val1 = 0
        val2 = 0
        if (self is not None): 
            val1 = self.value
        if (arg2 is not None): 
            val2 = arg2.value
        return MorphClass._new79(((val1) | (val2)))
    
    def __xor__(self : 'MorphClass', arg2 : 'MorphClass') -> 'MorphClass':
        val1 = 0
        val2 = 0
        if (self is not None): 
            val1 = self.value
        if (arg2 is not None): 
            val2 = arg2.value
        return MorphClass._new79(((val1) ^ (val2)))
    
    def __eq__(self : 'MorphClass', arg2 : 'MorphClass') -> bool:
        val1 = 0
        val2 = 0
        if (self is not None): 
            val1 = self.value
        if (arg2 is not None): 
            val2 = arg2.value
        return val1 == val2
    
    def __ne__(self : 'MorphClass', arg2 : 'MorphClass') -> bool:
        val1 = 0
        val2 = 0
        if (self is not None): 
            val1 = self.value
        if (arg2 is not None): 
            val2 = arg2.value
        return val1 != val2
    
    UNDEFINED = None
    
    NOUN = None
    
    PRONOUN = None
    
    PERSONAL_PRONOUN = None
    
    VERB = None
    
    ADJECTIVE = None
    
    ADVERB = None
    
    PREPOSITION = None
    
    CONJUNCTION = None
    
    @staticmethod
    def _new79(_arg1 : int) -> 'MorphClass':
        res = MorphClass()
        res.value = _arg1
        return res
    
    @staticmethod
    def _new82(_arg1 : bool) -> 'MorphClass':
        res = MorphClass()
        res.is_undefined = _arg1
        return res
    
    @staticmethod
    def _new83(_arg1 : bool) -> 'MorphClass':
        res = MorphClass()
        res.is_noun = _arg1
        return res
    
    @staticmethod
    def _new84(_arg1 : bool) -> 'MorphClass':
        res = MorphClass()
        res.is_pronoun = _arg1
        return res
    
    @staticmethod
    def _new85(_arg1 : bool) -> 'MorphClass':
        res = MorphClass()
        res.is_personal_pronoun = _arg1
        return res
    
    @staticmethod
    def _new86(_arg1 : bool) -> 'MorphClass':
        res = MorphClass()
        res.is_verb = _arg1
        return res
    
    @staticmethod
    def _new87(_arg1 : bool) -> 'MorphClass':
        res = MorphClass()
        res.is_adjective = _arg1
        return res
    
    @staticmethod
    def _new88(_arg1 : bool) -> 'MorphClass':
        res = MorphClass()
        res.is_adverb = _arg1
        return res
    
    @staticmethod
    def _new89(_arg1 : bool) -> 'MorphClass':
        res = MorphClass()
        res.is_preposition = _arg1
        return res
    
    @staticmethod
    def _new90(_arg1 : bool) -> 'MorphClass':
        res = MorphClass()
        res.is_conjunction = _arg1
        return res
    
    @staticmethod
    def _new2576(_arg1 : bool) -> 'MorphClass':
        res = MorphClass()
        res.is_proper_surname = _arg1
        return res
    
    # static constructor for class MorphClass
    @staticmethod
    def _static_ctor():
        MorphClass.__m_names = ["существ.", "прилаг.", "глагол", "наречие", "местоим.", "разное", "предлог", "союз", "собств.", "фамилия", "имя", "отч.", "геогр.", "личн.местоим."]
        MorphClass.UNDEFINED = MorphClass._new82(True)
        MorphClass.NOUN = MorphClass._new83(True)
        MorphClass.PRONOUN = MorphClass._new84(True)
        MorphClass.PERSONAL_PRONOUN = MorphClass._new85(True)
        MorphClass.VERB = MorphClass._new86(True)
        MorphClass.ADJECTIVE = MorphClass._new87(True)
        MorphClass.ADVERB = MorphClass._new88(True)
        MorphClass.PREPOSITION = MorphClass._new89(True)
        MorphClass.CONJUNCTION = MorphClass._new90(True)

MorphClass._static_ctor()