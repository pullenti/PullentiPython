# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

class MorphClass:
    """ Часть речи """
    
    def __init__(self) -> None:
        self.value = 0
    
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
    
    @property
    def is_misc(self) -> bool:
        """ Разное (частицы, междометия) """
        return self.__get_value(5)
    @is_misc.setter
    def is_misc(self, value_) -> bool:
        if (value_): 
            self.value = (0)
        self.__set_value(5, value_)
        return value_
    
    @property
    def is_preposition(self) -> bool:
        """ Предлог """
        return self.__get_value(6)
    @is_preposition.setter
    def is_preposition(self, value_) -> bool:
        self.__set_value(6, value_)
        return value_
    
    @property
    def is_conjunction(self) -> bool:
        """ Союз """
        return self.__get_value(7)
    @is_conjunction.setter
    def is_conjunction(self, value_) -> bool:
        self.__set_value(7, value_)
        return value_
    
    @property
    def is_proper(self) -> bool:
        """ Собственное имя (фамилия, имя, отчество, геогр.название и др.) """
        return self.__get_value(8)
    @is_proper.setter
    def is_proper(self, value_) -> bool:
        self.__set_value(8, value_)
        return value_
    
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
    
    @property
    def is_personal_pronoun(self) -> bool:
        """ Личное местоимение (я, мой, ты, он ...) """
        return self.__get_value(13)
    @is_personal_pronoun.setter
    def is_personal_pronoun(self, value_) -> bool:
        self.__set_value(13, value_)
        return value_
    
    __m_names = None
    
    def __str__(self) -> str:
        tmp_str = io.StringIO()
        if (self.is_noun): 
            print("существ.|", end="", file=tmp_str)
        if (self.is_adjective): 
            print("прилаг.|", end="", file=tmp_str)
        if (self.is_verb): 
            print("глагол|", end="", file=tmp_str)
        if (self.is_adverb): 
            print("наречие|", end="", file=tmp_str)
        if (self.is_pronoun): 
            print("местоим.|", end="", file=tmp_str)
        if (self.is_misc): 
            if (self.is_conjunction or self.is_preposition or self.is_proper): 
                pass
            else: 
                print("разное|", end="", file=tmp_str)
        if (self.is_preposition): 
            print("предлог|", end="", file=tmp_str)
        if (self.is_conjunction): 
            print("союз|", end="", file=tmp_str)
        if (self.is_proper): 
            print("собств.|", end="", file=tmp_str)
        if (self.is_proper_surname): 
            print("фамилия|", end="", file=tmp_str)
        if (self.is_proper_name): 
            print("имя|", end="", file=tmp_str)
        if (self.is_proper_secname): 
            print("отч.|", end="", file=tmp_str)
        if (self.is_proper_geo): 
            print("геогр.|", end="", file=tmp_str)
        if (self.is_personal_pronoun): 
            print("личн.местоим.|", end="", file=tmp_str)
        if (tmp_str.tell() > 0): 
            Utils.setLengthStringIO(tmp_str, tmp_str.tell() - 1)
        return Utils.toStringStringIO(tmp_str)
    
    UNDEFINED = None
    """ Неопределённое """
    
    NOUN = None
    """ Существительное """
    
    PRONOUN = None
    """ Местоимение """
    
    PERSONAL_PRONOUN = None
    """ Личное местоимение """
    
    VERB = None
    """ Глагол """
    
    ADJECTIVE = None
    """ Прилагательное """
    
    ADVERB = None
    """ Наречие """
    
    PREPOSITION = None
    """ Предлог """
    
    CONJUNCTION = None
    """ Союз """
    
    def equals(self, obj : object) -> bool:
        if (not (isinstance(obj, MorphClass))): 
            return False
        return self.value == obj.value
    
    def __hash__(self) -> int:
        return self.value
    
    def __and__(self : 'MorphClass', arg2 : 'MorphClass') -> 'MorphClass':
        """ Моделирование побитного "AND"
        
        Args:
            self(MorphClass): первый аргумент
            arg2(MorphClass): второй аргумент
        
        Returns:
            MorphClass: arg1 & arg2
        """
        val1 = 0
        val2 = 0
        if (self is not None): 
            val1 = self.value
        if (arg2 is not None): 
            val2 = arg2.value
        return MorphClass._new53(((val1) & (val2)))
    
    def __or__(self : 'MorphClass', arg2 : 'MorphClass') -> 'MorphClass':
        """ Моделирование побитного "OR"
        
        Args:
            self(MorphClass): первый аргумент
            arg2(MorphClass): второй аргумент
        
        Returns:
            MorphClass: arg1 | arg2
        """
        val1 = 0
        val2 = 0
        if (self is not None): 
            val1 = self.value
        if (arg2 is not None): 
            val2 = arg2.value
        return MorphClass._new53(((val1) | (val2)))
    
    def __xor__(self : 'MorphClass', arg2 : 'MorphClass') -> 'MorphClass':
        """ Моделирование побитного "XOR"
        
        Args:
            self(MorphClass): первый аргумент
            arg2(MorphClass): второй аргумент
        
        Returns:
            MorphClass: arg1 ^ arg2
        """
        val1 = 0
        val2 = 0
        if (self is not None): 
            val1 = self.value
        if (arg2 is not None): 
            val2 = arg2.value
        return MorphClass._new53(((val1) ^ (val2)))
    
    def __eq__(self : 'MorphClass', arg2 : 'MorphClass') -> bool:
        """ Моделирование сравнения ==
        
        Args:
            self(MorphClass): первый аргумент
            arg2(MorphClass): второй аргумент
        
        Returns:
            bool: arg1 == arg2
        """
        val1 = 0
        val2 = 0
        if (self is not None): 
            val1 = self.value
        if (arg2 is not None): 
            val2 = arg2.value
        return val1 == val2
    
    def __ne__(self : 'MorphClass', arg2 : 'MorphClass') -> bool:
        """ Моделирование неравенства !=
        
        Args:
            self(MorphClass): первый аргумент
            arg2(MorphClass): второй аргумент
        
        Returns:
            bool: arg1 != arg2
        """
        val1 = 0
        val2 = 0
        if (self is not None): 
            val1 = self.value
        if (arg2 is not None): 
            val2 = arg2.value
        return val1 != val2
    
    @staticmethod
    def _new44(_arg1 : bool) -> 'MorphClass':
        res = MorphClass()
        res.is_undefined = _arg1
        return res
    
    @staticmethod
    def _new45(_arg1 : bool) -> 'MorphClass':
        res = MorphClass()
        res.is_noun = _arg1
        return res
    
    @staticmethod
    def _new46(_arg1 : bool) -> 'MorphClass':
        res = MorphClass()
        res.is_pronoun = _arg1
        return res
    
    @staticmethod
    def _new47(_arg1 : bool) -> 'MorphClass':
        res = MorphClass()
        res.is_personal_pronoun = _arg1
        return res
    
    @staticmethod
    def _new48(_arg1 : bool) -> 'MorphClass':
        res = MorphClass()
        res.is_verb = _arg1
        return res
    
    @staticmethod
    def _new49(_arg1 : bool) -> 'MorphClass':
        res = MorphClass()
        res.is_adjective = _arg1
        return res
    
    @staticmethod
    def _new50(_arg1 : bool) -> 'MorphClass':
        res = MorphClass()
        res.is_adverb = _arg1
        return res
    
    @staticmethod
    def _new51(_arg1 : bool) -> 'MorphClass':
        res = MorphClass()
        res.is_preposition = _arg1
        return res
    
    @staticmethod
    def _new52(_arg1 : bool) -> 'MorphClass':
        res = MorphClass()
        res.is_conjunction = _arg1
        return res
    
    @staticmethod
    def _new53(_arg1 : int) -> 'MorphClass':
        res = MorphClass()
        res.value = _arg1
        return res
    
    @staticmethod
    def _new2568(_arg1 : bool) -> 'MorphClass':
        res = MorphClass()
        res.is_proper_surname = _arg1
        return res
    
    # static constructor for class MorphClass
    @staticmethod
    def _static_ctor():
        MorphClass.__m_names = ["существ.", "прилаг.", "глагол", "наречие", "местоим.", "разное", "предлог", "союз", "собств.", "фамилия", "имя", "отч.", "геогр.", "личн.местоим."]
        MorphClass.UNDEFINED = MorphClass._new44(True)
        MorphClass.NOUN = MorphClass._new45(True)
        MorphClass.PRONOUN = MorphClass._new46(True)
        MorphClass.PERSONAL_PRONOUN = MorphClass._new47(True)
        MorphClass.VERB = MorphClass._new48(True)
        MorphClass.ADJECTIVE = MorphClass._new49(True)
        MorphClass.ADVERB = MorphClass._new50(True)
        MorphClass.PREPOSITION = MorphClass._new51(True)
        MorphClass.CONJUNCTION = MorphClass._new52(True)

MorphClass._static_ctor()