# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.MorphLang import MorphLang
from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.MorphCase import MorphCase

class MorphBaseInfo:
    """ Базовая часть морфологической информации
    
    основная морф.информация
    """
    
    def __init__(self) -> None:
        self.__m_cla = MorphClass()
        self.__gender = MorphGender.UNDEFINED
        self.__number = MorphNumber.UNDEFINED
        self.__m_cas = MorphCase()
        self.__m_lang = MorphLang()
    
    @property
    def class0_(self) -> 'MorphClass':
        """ Часть речи """
        return self.__m_cla
    @class0_.setter
    def class0_(self, value) -> 'MorphClass':
        self.__m_cla = value
        return value
    
    @property
    def gender(self) -> 'MorphGender':
        """ Род """
        return self.__gender
    @gender.setter
    def gender(self, value) -> 'MorphGender':
        self.__gender = value
        return self.__gender
    
    @property
    def number(self) -> 'MorphNumber':
        """ Число """
        return self.__number
    @number.setter
    def number(self, value) -> 'MorphNumber':
        self.__number = value
        return self.__number
    
    @property
    def case_(self) -> 'MorphCase':
        """ Падеж """
        return self.__m_cas
    @case_.setter
    def case_(self, value) -> 'MorphCase':
        self.__m_cas = value
        return value
    
    @property
    def language(self) -> 'MorphLang':
        """ Язык """
        return self.__m_lang
    @language.setter
    def language(self, value) -> 'MorphLang':
        self.__m_lang = value
        return value
    
    def __str__(self) -> str:
        res = io.StringIO()
        if (not self.class0_.is_undefined): 
            print("{0} ".format(str(self.class0_)), end="", file=res, flush=True)
        if (self.number != MorphNumber.UNDEFINED): 
            if (self.number == MorphNumber.SINGULAR): 
                print("ед.ч. ", end="", file=res)
            elif (self.number == MorphNumber.PLURAL): 
                print("мн.ч. ", end="", file=res)
            else: 
                print("ед.мн.ч. ", end="", file=res)
        if (self.gender != MorphGender.UNDEFINED): 
            if (self.gender == MorphGender.MASCULINE): 
                print("муж.р. ", end="", file=res)
            elif (self.gender == MorphGender.NEUTER): 
                print("ср.р. ", end="", file=res)
            elif (self.gender == MorphGender.FEMINIE): 
                print("жен.р. ", end="", file=res)
            elif ((self.gender) == ((MorphGender.MASCULINE) | (MorphGender.NEUTER))): 
                print("муж.ср.р. ".format(), end="", file=res, flush=True)
            elif ((self.gender) == ((MorphGender.FEMINIE) | (MorphGender.NEUTER))): 
                print("жен.ср.р. ".format(), end="", file=res, flush=True)
            elif ((self.gender) == 7): 
                print("муж.жен.ср.р. ".format(), end="", file=res, flush=True)
            elif ((self.gender) == ((MorphGender.FEMINIE) | (MorphGender.MASCULINE))): 
                print("муж.жен.р. ".format(), end="", file=res, flush=True)
        if (not self.case_.is_undefined): 
            print("{0} ".format(str(self.case_)), end="", file=res, flush=True)
        if (not self.language.is_undefined and self.language != MorphLang.RU): 
            print("{0} ".format(str(self.language)), end="", file=res, flush=True)
        return Utils.trimEndString(Utils.toStringStringIO(res))
    
    def copy_from(self, src : 'MorphBaseInfo') -> None:
        cla = MorphClass()
        cla.value = src.class0_.value
        self.class0_ = cla
        self.gender = src.gender
        self.number = src.number
        cas = MorphCase()
        cas.value = src.case_.value
        self.case_ = cas
        lng = MorphLang()
        lng.value = src.language.value
        self.language = lng
    
    def contains_attr(self, attr_value : str, cla : 'MorphClass'=None) -> bool:
        return False
    
    def check_accord(self, v : 'MorphBaseInfo', ignore_gender : bool=False, ignore_number : bool=False) -> bool:
        if (v.language != self.language): 
            if (v.language == MorphLang.UNKNOWN and self.language == MorphLang.UNKNOWN): 
                return False
        num = (v.number) & (self.number)
        if ((num) == (MorphNumber.UNDEFINED) and not ignore_number): 
            if (v.number != MorphNumber.UNDEFINED and self.number != MorphNumber.UNDEFINED): 
                if (v.number == MorphNumber.SINGULAR and v.case_.is_genitive): 
                    if (self.number == MorphNumber.PLURAL and self.case_.is_genitive): 
                        if (((v.gender) & (MorphGender.MASCULINE)) == (MorphGender.MASCULINE)): 
                            return True
                return False
        if (not ignore_gender and (num) != (MorphNumber.PLURAL)): 
            if (((v.gender) & (self.gender)) == (MorphGender.UNDEFINED)): 
                if (v.gender != MorphGender.UNDEFINED and self.gender != MorphGender.UNDEFINED): 
                    return False
        if (((v.case_) & self.case_).is_undefined): 
            if (not v.case_.is_undefined and not self.case_.is_undefined): 
                return False
        return True
    
    @staticmethod
    def _new192(_arg1 : 'MorphClass', _arg2 : 'MorphNumber') -> 'MorphBaseInfo':
        res = MorphBaseInfo()
        res.class0_ = _arg1
        res.number = _arg2
        return res
    
    @staticmethod
    def _new193(_arg1 : 'MorphClass', _arg2 : 'MorphGender') -> 'MorphBaseInfo':
        res = MorphBaseInfo()
        res.class0_ = _arg1
        res.gender = _arg2
        return res
    
    @staticmethod
    def _new221(_arg1 : 'MorphCase', _arg2 : 'MorphClass', _arg3 : 'MorphNumber', _arg4 : 'MorphGender') -> 'MorphBaseInfo':
        res = MorphBaseInfo()
        res.case_ = _arg1
        res.class0_ = _arg2
        res.number = _arg3
        res.gender = _arg4
        return res
    
    @staticmethod
    def _new401(_arg1 : 'MorphClass', _arg2 : 'MorphGender', _arg3 : 'MorphNumber', _arg4 : 'MorphCase', _arg5 : 'MorphLang') -> 'MorphBaseInfo':
        res = MorphBaseInfo()
        res.class0_ = _arg1
        res.gender = _arg2
        res.number = _arg3
        res.case_ = _arg4
        res.language = _arg5
        return res
    
    @staticmethod
    def _new492(_arg1 : 'MorphClass', _arg2 : 'MorphGender', _arg3 : 'MorphNumber', _arg4 : 'MorphLang') -> 'MorphBaseInfo':
        res = MorphBaseInfo()
        res.class0_ = _arg1
        res.gender = _arg2
        res.number = _arg3
        res.language = _arg4
        return res
    
    @staticmethod
    def _new493(_arg1 : 'MorphGender', _arg2 : 'MorphCase', _arg3 : 'MorphNumber') -> 'MorphBaseInfo':
        res = MorphBaseInfo()
        res.gender = _arg1
        res.case_ = _arg2
        res.number = _arg3
        return res
    
    @staticmethod
    def _new495(_arg1 : 'MorphClass', _arg2 : 'MorphCase', _arg3 : 'MorphNumber', _arg4 : 'MorphGender') -> 'MorphBaseInfo':
        res = MorphBaseInfo()
        res.class0_ = _arg1
        res.case_ = _arg2
        res.number = _arg3
        res.gender = _arg4
        return res
    
    @staticmethod
    def _new496(_arg1 : 'MorphClass', _arg2 : 'MorphCase', _arg3 : 'MorphNumber') -> 'MorphBaseInfo':
        res = MorphBaseInfo()
        res.class0_ = _arg1
        res.case_ = _arg2
        res.number = _arg3
        return res
    
    @staticmethod
    def _new499(_arg1 : 'MorphCase', _arg2 : 'MorphLang') -> 'MorphBaseInfo':
        res = MorphBaseInfo()
        res.case_ = _arg1
        res.language = _arg2
        return res
    
    @staticmethod
    def _new511(_arg1 : 'MorphClass') -> 'MorphBaseInfo':
        res = MorphBaseInfo()
        res.class0_ = _arg1
        return res
    
    @staticmethod
    def _new1815(_arg1 : 'MorphCase', _arg2 : 'MorphGender', _arg3 : 'MorphNumber') -> 'MorphBaseInfo':
        res = MorphBaseInfo()
        res.case_ = _arg1
        res.gender = _arg2
        res.number = _arg3
        return res
    
    @staticmethod
    def _new2348(_arg1 : 'MorphClass', _arg2 : 'MorphGender', _arg3 : 'MorphLang') -> 'MorphBaseInfo':
        res = MorphBaseInfo()
        res.class0_ = _arg1
        res.gender = _arg2
        res.language = _arg3
        return res
    
    @staticmethod
    def _new2472(_arg1 : 'MorphCase') -> 'MorphBaseInfo':
        res = MorphBaseInfo()
        res.case_ = _arg1
        return res
    
    @staticmethod
    def _new2485(_arg1 : 'MorphCase', _arg2 : 'MorphGender') -> 'MorphBaseInfo':
        res = MorphBaseInfo()
        res.case_ = _arg1
        res.gender = _arg2
        return res
    
    @staticmethod
    def _new2499(_arg1 : 'MorphGender', _arg2 : 'MorphCase') -> 'MorphBaseInfo':
        res = MorphBaseInfo()
        res.gender = _arg1
        res.case_ = _arg2
        return res
    
    @staticmethod
    def _new2521(_arg1 : 'MorphGender') -> 'MorphBaseInfo':
        res = MorphBaseInfo()
        res.gender = _arg1
        return res
    
    @staticmethod
    def _new2569(_arg1 : 'MorphCase', _arg2 : 'MorphGender', _arg3 : 'MorphClass') -> 'MorphBaseInfo':
        res = MorphBaseInfo()
        res.case_ = _arg1
        res.gender = _arg2
        res.class0_ = _arg3
        return res
    
    @staticmethod
    def _new2606(_arg1 : 'MorphNumber', _arg2 : 'MorphLang') -> 'MorphBaseInfo':
        res = MorphBaseInfo()
        res.number = _arg1
        res.language = _arg2
        return res
    
    @staticmethod
    def _new2611(_arg1 : 'MorphGender', _arg2 : 'MorphNumber', _arg3 : 'MorphLang') -> 'MorphBaseInfo':
        res = MorphBaseInfo()
        res.gender = _arg1
        res.number = _arg2
        res.language = _arg3
        return res
    
    @staticmethod
    def _new2613(_arg1 : 'MorphNumber', _arg2 : 'MorphGender', _arg3 : 'MorphLang') -> 'MorphBaseInfo':
        res = MorphBaseInfo()
        res.number = _arg1
        res.gender = _arg2
        res.language = _arg3
        return res