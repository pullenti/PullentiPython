# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing
import io
from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphMood import MorphMood
from pullenti.morph.MorphVoice import MorphVoice
from pullenti.morph.MorphForm import MorphForm
from pullenti.morph.MorphPerson import MorphPerson
from pullenti.morph.MorphTense import MorphTense
from pullenti.morph.MorphAspect import MorphAspect

class MorphMiscInfo:
    """ Дополнительная морфологическая информация
    Дополнительная морф.информация
    """
    
    def __init__(self) -> None:
        self.__m_attrs = list()
        self.value = 0
        self.id0_ = 0
    
    @property
    def attrs(self) -> typing.List[str]:
        """ Дополнительные атрибуты """
        return self.__m_attrs
    
    def add_attr(self, a : str) -> None:
        if (not a in self.__m_attrs): 
            self.__m_attrs.append(a)
    
    def __get_bool_value(self, i : int) -> bool:
        return (((((self.value) >> i)) & 1)) != 0
    
    def __set_bool_value(self, i : int, val : bool) -> None:
        if (val): 
            self.value |= ((1 << i))
        else: 
            self.value &= (~ ((1 << i)))
    
    def copy_from(self, src : 'MorphMiscInfo') -> None:
        self.value = src.value
        for a in src.attrs: 
            self.__m_attrs.append(a)
    
    @property
    def person(self) -> 'MorphPerson':
        """ Лицо """
        res = MorphPerson.UNDEFINED
        if ("1 л." in self.__m_attrs): 
            res = (Utils.valToEnum((res) | (MorphPerson.FIRST), MorphPerson))
        if ("2 л." in self.__m_attrs): 
            res = (Utils.valToEnum((res) | (MorphPerson.SECOND), MorphPerson))
        if ("3 л." in self.__m_attrs): 
            res = (Utils.valToEnum((res) | (MorphPerson.THIRD), MorphPerson))
        return res
    @person.setter
    def person(self, value_) -> 'MorphPerson':
        if (((value_) & (MorphPerson.FIRST)) != (MorphPerson.UNDEFINED)): 
            self.add_attr("1 л.")
        if (((value_) & (MorphPerson.SECOND)) != (MorphPerson.UNDEFINED)): 
            self.add_attr("2 л.")
        if (((value_) & (MorphPerson.THIRD)) != (MorphPerson.UNDEFINED)): 
            self.add_attr("3 л.")
        return value_
    
    @property
    def tense(self) -> 'MorphTense':
        """ Время (для глаголов) """
        if ("п.вр." in self.__m_attrs): 
            return MorphTense.PAST
        if ("н.вр." in self.__m_attrs): 
            return MorphTense.PRESENT
        if ("б.вр." in self.__m_attrs): 
            return MorphTense.FUTURE
        return MorphTense.UNDEFINED
    @tense.setter
    def tense(self, value_) -> 'MorphTense':
        if (value_ == MorphTense.PAST): 
            self.add_attr("п.вр.")
        if (value_ == MorphTense.PRESENT): 
            self.add_attr("н.вр.")
        if (value_ == MorphTense.FUTURE): 
            self.add_attr("б.вр.")
        return value_
    
    @property
    def aspect(self) -> 'MorphAspect':
        """ Аспект (совершенный - несовершенный) """
        if ("нес.в." in self.__m_attrs): 
            return MorphAspect.IMPERFECTIVE
        if ("сов.в." in self.__m_attrs): 
            return MorphAspect.PERFECTIVE
        return MorphAspect.UNDEFINED
    @aspect.setter
    def aspect(self, value_) -> 'MorphAspect':
        if (value_ == MorphAspect.IMPERFECTIVE): 
            self.add_attr("нес.в.")
        if (value_ == MorphAspect.PERFECTIVE): 
            self.add_attr("сов.в.")
        return value_
    
    @property
    def mood(self) -> 'MorphMood':
        """ Наклонение (для глаголов) """
        if ("пов.накл." in self.__m_attrs): 
            return MorphMood.IMPERATIVE
        return MorphMood.UNDEFINED
    @mood.setter
    def mood(self, value_) -> 'MorphMood':
        if (value_ == MorphMood.IMPERATIVE): 
            self.add_attr("пов.накл.")
        return value_
    
    @property
    def voice(self) -> 'MorphVoice':
        """ Залог (для глаголов) """
        if ("дейст.з." in self.__m_attrs): 
            return MorphVoice.ACTIVE
        if ("страд.з." in self.__m_attrs): 
            return MorphVoice.PASSIVE
        return MorphVoice.UNDEFINED
    @voice.setter
    def voice(self, value_) -> 'MorphVoice':
        if (value_ == MorphVoice.ACTIVE): 
            self.add_attr("дейст.з.")
        if (value_ == MorphVoice.PASSIVE): 
            self.add_attr("страд.з.")
        return value_
    
    @property
    def form(self) -> 'MorphForm':
        """ Форма (краткая, синонимичная) """
        if ("к.ф." in self.__m_attrs): 
            return MorphForm.SHORT
        if ("синоним.форма" in self.__m_attrs): 
            return MorphForm.SYNONYM
        if (self.is_synonym_form): 
            return MorphForm.SYNONYM
        return MorphForm.UNDEFINED
    
    @property
    def is_synonym_form(self) -> bool:
        """ Синонимическая форма """
        return self.__get_bool_value(0)
    @is_synonym_form.setter
    def is_synonym_form(self, value_) -> bool:
        self.__set_bool_value(0, value_)
        return value_
    
    def __str__(self) -> str:
        if (len(self.__m_attrs) == 0 and self.value == (0)): 
            return ""
        res = io.StringIO()
        if (self.is_synonym_form): 
            print("синоним.форма ", end="", file=res)
        i = 0
        while i < len(self.__m_attrs): 
            print("{0} ".format(self.__m_attrs[i]), end="", file=res, flush=True)
            i += 1
        return Utils.trimEndString(Utils.toStringStringIO(res))
    
    def _deserialize(self, str0_ : 'ByteArrayWrapper', pos : int) -> None:
        sh = str0_.deserialize_short(pos)
        self.value = (sh)
        while True:
            s = str0_.deserialize_string(pos)
            if (Utils.isNullOrEmpty(s)): 
                break
            if (not s in self.__m_attrs): 
                self.__m_attrs.append(s)