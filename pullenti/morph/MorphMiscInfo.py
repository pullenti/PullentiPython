# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import typing
import io
from pullenti.ntopy.Utils import Utils
from pullenti.morph.MorphPerson import MorphPerson
from pullenti.morph.MorphTense import MorphTense
from pullenti.morph.MorphAspect import MorphAspect
from pullenti.morph.MorphMood import MorphMood
from pullenti.morph.MorphVoice import MorphVoice
from pullenti.morph.MorphForm import MorphForm


class MorphMiscInfo:
    """ Дополнительная морфологическая информация """
    
    def __init__(self) -> None:
        self.__m_attrs = list()
        self._m_value = 0
        self._id0_ = 0
    
    @property
    def attrs(self) -> typing.List[str]:
        """ Дополнительные атрибуты """
        return self.__m_attrs
    
    def __get_value(self, i : int) -> bool:
        return ((((self._m_value >> i)) & 1)) != 0
    
    def __set_value(self, i : int, val : bool) -> None:
        if (val): 
            self._m_value |= (1 << i)
        else: 
            self._m_value &= ~ ((1 << i))
    
    def __add_attr(self, attr : str) -> None:
        if (not attr in self.__m_attrs): 
            self.__m_attrs.append(attr)
    
    def clone(self) -> 'MorphMiscInfo':
        res = MorphMiscInfo()
        res._m_value = self._m_value
        res.__m_attrs.extend(self.__m_attrs)
        return res
    
    @property
    def person(self) -> 'MorphPerson':
        """ Лицо """
        res = MorphPerson.UNDEFINED
        if ("1 л." in self.__m_attrs): 
            res = Utils.valToEnum(res | MorphPerson.FIRST, MorphPerson)
        if ("2 л." in self.__m_attrs): 
            res = Utils.valToEnum(res | MorphPerson.SECOND, MorphPerson)
        if ("3 л." in self.__m_attrs): 
            res = Utils.valToEnum(res | MorphPerson.THIRD, MorphPerson)
        return res
    
    @person.setter
    def person(self, value) -> 'MorphPerson':
        if (((value & MorphPerson.FIRST)) != MorphPerson.UNDEFINED): 
            self.__add_attr("1 л.")
        if (((value & MorphPerson.SECOND)) != MorphPerson.UNDEFINED): 
            self.__add_attr("2 л.")
        if (((value & MorphPerson.THIRD)) != MorphPerson.UNDEFINED): 
            self.__add_attr("3 л.")
        return value
    
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
    def tense(self, value) -> 'MorphTense':
        if (value == MorphTense.PAST): 
            self.__add_attr("п.вр.")
        if (value == MorphTense.PRESENT): 
            self.__add_attr("н.вр.")
        if (value == MorphTense.FUTURE): 
            self.__add_attr("б.вр.")
        return value
    
    @property
    def aspect(self) -> 'MorphAspect':
        """ Аспект (совершенный - несовершенный) """
        if ("нес.в." in self.__m_attrs): 
            return MorphAspect.IMPERFECTIVE
        if ("сов.в." in self.__m_attrs): 
            return MorphAspect.PERFECTIVE
        return MorphAspect.UNDEFINED
    
    @aspect.setter
    def aspect(self, value) -> 'MorphAspect':
        if (value == MorphAspect.IMPERFECTIVE): 
            self.__add_attr("нес.в.")
        if (value == MorphAspect.PERFECTIVE): 
            self.__add_attr("сов.в.")
        return value
    
    @property
    def mood(self) -> 'MorphMood':
        """ Наклонение (для глаголов) """
        if ("пов.накл." in self.__m_attrs): 
            return MorphMood.IMPERATIVE
        return MorphMood.UNDEFINED
    
    @mood.setter
    def mood(self, value) -> 'MorphMood':
        if (value == MorphMood.IMPERATIVE): 
            self.__add_attr("пов.накл.")
        return value
    
    @property
    def voice(self) -> 'MorphVoice':
        """ Залог (для глаголов) """
        if ("дейст.з." in self.__m_attrs): 
            return MorphVoice.ACTIVE
        if ("страд.з." in self.__m_attrs): 
            return MorphVoice.PASSIVE
        return MorphVoice.UNDEFINED
    
    @voice.setter
    def voice(self, value) -> 'MorphVoice':
        if (value == MorphVoice.ACTIVE): 
            self.__add_attr("дейст.з.")
        if (value == MorphVoice.PASSIVE): 
            self.__add_attr("страд.з.")
        return value
    
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
        return self.__get_value(0)
    
    @is_synonym_form.setter
    def is_synonym_form(self, value) -> bool:
        self.__set_value(0, value)
        return value
    
    def __str__(self) -> str:
        if (len(self.__m_attrs) == 0 and self._m_value == 0): 
            return ""
        res = Utils.newStringIO(None)
        if (self.is_synonym_form): 
            print("синоним.форма ", end="", file=res)
        for i in range(len(self.__m_attrs)):
            print("{0} ".format(self.__m_attrs[i]), end="", file=res, flush=True)
        return Utils.trimEndString(Utils.toStringStringIO(res))