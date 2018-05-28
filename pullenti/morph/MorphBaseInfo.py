# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import io
from pullenti.ntopy.Utils import Utils
from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphNumber import MorphNumber


class MorphBaseInfo:
    """ Базовая часть морфологической информации """
    
    def __init__(self, bi : 'MorphBaseInfo'=None) -> None:
        from pullenti.morph.MorphCase import MorphCase
        from pullenti.morph.MorphLang import MorphLang
        self.__m_cla = MorphClass()
        self.__gender = MorphGender.UNDEFINED
        self.__number = MorphNumber.UNDEFINED
        self.__m_cas = MorphCase()
        self.__m_lang = MorphLang()
        if (bi is not None): 
            bi.copy_to(self)
    
    @property
    def class0(self) -> 'MorphClass':
        """ Часть речи """
        return self.__m_cla
    
    @class0.setter
    def class0(self, value) -> 'MorphClass':
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
    def case(self) -> 'MorphCase':
        """ Падеж """
        return self.__m_cas
    
    @case.setter
    def case(self, value) -> 'MorphCase':
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
        from pullenti.morph.MorphLang import MorphLang
        res = Utils.newStringIO(None)
        if (not self.class0.is_undefined): 
            print("{0} ".format(str(self.class0)), end="", file=res, flush=True)
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
            elif (self.gender == ((MorphGender.MASCULINE | MorphGender.NEUTER))): 
                print("муж.ср.р. ".format(), end="", file=res, flush=True)
            elif (self.gender == ((MorphGender.FEMINIE | MorphGender.NEUTER))): 
                print("жен.ср.р. ".format(), end="", file=res, flush=True)
            elif (self.gender == 7): 
                print("муж.жен.ср.р. ".format(), end="", file=res, flush=True)
            elif (self.gender == ((MorphGender.FEMINIE | MorphGender.MASCULINE))): 
                print("муж.жен.р. ".format(), end="", file=res, flush=True)
        if (not self.case.is_undefined): 
            print("{0} ".format(str(self.case)), end="", file=res, flush=True)
        if (not self.language.is_undefined and self.language != MorphLang.RU): 
            print("{0} ".format(str(self.language)), end="", file=res, flush=True)
        return Utils.trimEndString(Utils.toStringStringIO(res))
    
    def copy_to(self, dst : 'MorphBaseInfo') -> None:
        from pullenti.morph.MorphCase import MorphCase
        from pullenti.morph.MorphLang import MorphLang
        dst.class0 = MorphClass(self.class0)
        dst.gender = self.gender
        dst.number = self.number
        dst.case = MorphCase(self.case)
        dst.language = MorphLang(self.language)
    
    def contains_attr(self, attr_value : str, cla : 'MorphClass'=MorphClass()) -> bool:
        from pullenti.morph.MorphWordForm import MorphWordForm
        wf = (self if isinstance(self, MorphWordForm) else None)
        if (wf is None): 
            return False
        if (wf.misc is not None and wf.misc.attrs is not None): 
            return attr_value in wf.misc.attrs
        return False
    
    def clone(self) -> object:
        res = MorphBaseInfo()
        self.copy_to(res)
        return res
    
    def check_accord(self, v : 'MorphBaseInfo', ignore_gender : bool=False) -> bool:
        from pullenti.morph.MorphLang import MorphLang
        if (v.language != self.language): 
            if (v.language == MorphLang.UNKNOWN and self.language == MorphLang.UNKNOWN): 
                return False
        if (((v.number & self.number)) == MorphNumber.UNDEFINED): 
            if (v.number != MorphNumber.UNDEFINED and self.number != MorphNumber.UNDEFINED): 
                if (v.number == MorphNumber.SINGULAR and v.case.is_genitive): 
                    if (self.number == MorphNumber.PLURAL and self.case.is_genitive): 
                        if (((v.gender & MorphGender.MASCULINE)) == MorphGender.MASCULINE): 
                            return True
                return False
        if (not ignore_gender): 
            if (((v.gender & self.gender)) == MorphGender.UNDEFINED): 
                if (v.gender != MorphGender.UNDEFINED and self.gender != MorphGender.UNDEFINED): 
                    return False
        if ((v.case & self.case).is_undefined): 
            if (not v.case.is_undefined and not self.case.is_undefined): 
                return False
        return True

    
    @staticmethod
    def _new210(_arg1 : 'MorphClass', _arg2 : 'MorphNumber') -> 'MorphBaseInfo':
        res = MorphBaseInfo()
        res.class0 = _arg1
        res.number = _arg2
        return res
    
    @staticmethod
    def _new211(_arg1 : 'MorphClass', _arg2 : 'MorphGender') -> 'MorphBaseInfo':
        res = MorphBaseInfo()
        res.class0 = _arg1
        res.gender = _arg2
        return res
    
    @staticmethod
    def _new238(_arg1 : 'MorphCase', _arg2 : 'MorphClass', _arg3 : 'MorphNumber', _arg4 : 'MorphGender') -> 'MorphBaseInfo':
        res = MorphBaseInfo()
        res.case = _arg1
        res.class0 = _arg2
        res.number = _arg3
        res.gender = _arg4
        return res
    
    @staticmethod
    def _new486(_arg1 : 'MorphClass', _arg2 : 'MorphGender', _arg3 : 'MorphNumber', _arg4 : 'MorphLang') -> 'MorphBaseInfo':
        res = MorphBaseInfo()
        res.class0 = _arg1
        res.gender = _arg2
        res.number = _arg3
        res.language = _arg4
        return res
    
    @staticmethod
    def _new487(_arg1 : 'MorphGender', _arg2 : 'MorphCase', _arg3 : 'MorphNumber') -> 'MorphBaseInfo':
        res = MorphBaseInfo()
        res.gender = _arg1
        res.case = _arg2
        res.number = _arg3
        return res
    
    @staticmethod
    def _new488(_arg1 : 'MorphCase', _arg2 : 'MorphLang') -> 'MorphBaseInfo':
        res = MorphBaseInfo()
        res.case = _arg1
        res.language = _arg2
        return res
    
    @staticmethod
    def _new566(_arg1 : 'MorphClass') -> 'MorphBaseInfo':
        res = MorphBaseInfo()
        res.class0 = _arg1
        return res
    
    @staticmethod
    def _new1430(_arg1 : 'MorphClass', _arg2 : 'MorphGender', _arg3 : 'MorphNumber', _arg4 : 'MorphCase', _arg5 : 'MorphLang') -> 'MorphBaseInfo':
        res = MorphBaseInfo()
        res.class0 = _arg1
        res.gender = _arg2
        res.number = _arg3
        res.case = _arg4
        res.language = _arg5
        return res
    
    @staticmethod
    def _new1531(_arg1 : 'MorphCase', _arg2 : 'MorphGender', _arg3 : 'MorphNumber') -> 'MorphBaseInfo':
        res = MorphBaseInfo()
        res.case = _arg1
        res.gender = _arg2
        res.number = _arg3
        return res
    
    @staticmethod
    def _new2017(_arg1 : 'MorphClass', _arg2 : 'MorphGender', _arg3 : 'MorphLang') -> 'MorphBaseInfo':
        res = MorphBaseInfo()
        res.class0 = _arg1
        res.gender = _arg2
        res.language = _arg3
        return res
    
    @staticmethod
    def _new2094(_arg1 : 'MorphCase') -> 'MorphBaseInfo':
        res = MorphBaseInfo()
        res.case = _arg1
        return res
    
    @staticmethod
    def _new2152(_arg1 : 'MorphCase', _arg2 : 'MorphGender') -> 'MorphBaseInfo':
        res = MorphBaseInfo()
        res.case = _arg1
        res.gender = _arg2
        return res
    
    @staticmethod
    def _new2166(_arg1 : 'MorphGender', _arg2 : 'MorphCase') -> 'MorphBaseInfo':
        res = MorphBaseInfo()
        res.gender = _arg1
        res.case = _arg2
        return res
    
    @staticmethod
    def _new2188(_arg1 : 'MorphGender') -> 'MorphBaseInfo':
        res = MorphBaseInfo()
        res.gender = _arg1
        return res
    
    @staticmethod
    def _new2234(_arg1 : 'MorphCase', _arg2 : 'MorphGender', _arg3 : 'MorphClass') -> 'MorphBaseInfo':
        res = MorphBaseInfo()
        res.case = _arg1
        res.gender = _arg2
        res.class0 = _arg3
        return res
    
    @staticmethod
    def _new2269(_arg1 : 'MorphNumber', _arg2 : 'MorphLang') -> 'MorphBaseInfo':
        res = MorphBaseInfo()
        res.number = _arg1
        res.language = _arg2
        return res
    
    @staticmethod
    def _new2272(_arg1 : 'MorphGender', _arg2 : 'MorphNumber', _arg3 : 'MorphLang') -> 'MorphBaseInfo':
        res = MorphBaseInfo()
        res.gender = _arg1
        res.number = _arg2
        res.language = _arg3
        return res
    
    @staticmethod
    def _new2274(_arg1 : 'MorphNumber', _arg2 : 'MorphGender', _arg3 : 'MorphLang') -> 'MorphBaseInfo':
        res = MorphBaseInfo()
        res.number = _arg1
        res.gender = _arg2
        res.language = _arg3
        return res