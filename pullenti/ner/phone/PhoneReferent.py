# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
import typing
from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.ReferentsEqualType import ReferentsEqualType
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.phone.internal.MetaPhone import MetaPhone
from pullenti.ner.Referent import Referent
from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.phone.PhoneKind import PhoneKind

class PhoneReferent(Referent):
    """ Сущность - телефонный номер
    
    """
    
    def __init__(self) -> None:
        super().__init__(PhoneReferent.OBJ_TYPENAME)
        self._m_template = None;
        self.instance_of = MetaPhone._global_meta
    
    OBJ_TYPENAME = "PHONE"
    """ Имя типа сущности TypeName ("PHONE") """
    
    ATTR_NUNBER = "NUMBER"
    """ Имя атрибута - номер (слитно, без кода страны) """
    
    ATTR_KIND = "KIND"
    """ Имя атрибута - тип (PhoneKind) """
    
    ATTR_COUNTRYCODE = "COUNTRYCODE"
    """ Имя атрибута - код страны """
    
    ATTR_ADDNUMBER = "ADDNUMBER"
    """ Имя атрибута - добавочный номер """
    
    def to_string(self, short_variant : bool, lang : 'MorphLang'=None, lev : int=0) -> str:
        res = io.StringIO()
        if (self.country_code is not None): 
            print("{0}{1} ".format(("+" if self.country_code != "8" else ""), self.country_code), end="", file=res, flush=True)
        num = self.number
        if (num is not None and len(num) >= 9): 
            cou = 3
            if (len(num) >= 11): 
                cou = (len(num) - 7)
            print("({0}) ".format(num[0:0+cou]), end="", file=res, flush=True)
            num = num[cou:]
        elif (num is not None and len(num) == 8): 
            print("({0}) ".format(num[0:0+2]), end="", file=res, flush=True)
            num = num[2:]
        if (num is None): 
            print("???-??-??", end="", file=res)
        else: 
            print(num, end="", file=res)
            if (len(num) > 5): 
                Utils.insertStringIO(res, res.tell() - 4, '-')
                Utils.insertStringIO(res, res.tell() - 2, '-')
        if (self.add_number is not None): 
            print(" (доб.{0})".format(self.add_number), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @property
    def number(self) -> str:
        """ Основной номер (без кода страны) """
        return self.get_string_value(PhoneReferent.ATTR_NUNBER)
    @number.setter
    def number(self, value) -> str:
        self.add_slot(PhoneReferent.ATTR_NUNBER, value, True, 0)
        return value
    
    @property
    def add_number(self) -> str:
        """ Добавочный номер (если есть) """
        return self.get_string_value(PhoneReferent.ATTR_ADDNUMBER)
    @add_number.setter
    def add_number(self, value) -> str:
        self.add_slot(PhoneReferent.ATTR_ADDNUMBER, value, True, 0)
        return value
    
    @property
    def country_code(self) -> str:
        """ Код страны """
        return self.get_string_value(PhoneReferent.ATTR_COUNTRYCODE)
    @country_code.setter
    def country_code(self, value) -> str:
        self.add_slot(PhoneReferent.ATTR_COUNTRYCODE, value, True, 0)
        return value
    
    @property
    def kind(self) -> 'PhoneKind':
        """ Тип телефона """
        str0_ = self.get_string_value(PhoneReferent.ATTR_KIND)
        if (str0_ is None): 
            return PhoneKind.UNDEFINED
        try: 
            return Utils.valToEnum(str0_, PhoneKind)
        except Exception as ex: 
            return PhoneKind.UNDEFINED
    @kind.setter
    def kind(self, value) -> 'PhoneKind':
        if (value != PhoneKind.UNDEFINED): 
            self.add_slot(PhoneReferent.ATTR_KIND, Utils.enumToString(value).lower(), True, 0)
        return value
    
    def get_compare_strings(self) -> typing.List[str]:
        num = self.number
        if (num is None): 
            return None
        if (len(num) > 9): 
            num = num[9:]
        res = list()
        res.append(num)
        add = self.add_number
        if (add is not None): 
            res.append("{0}*{1}".format(num, add))
        return res
    
    def can_be_equals(self, obj : 'Referent', typ : 'ReferentsEqualType') -> bool:
        return self.__can_be_equal(obj, typ, False)
    
    def __can_be_equal(self, obj : 'Referent', typ : 'ReferentsEqualType', ignore_add_number : bool) -> bool:
        ph = Utils.asObjectOrNull(obj, PhoneReferent)
        if (ph is None): 
            return False
        if (ph.country_code is not None and self.country_code is not None): 
            if (ph.country_code != self.country_code): 
                return False
        if (ignore_add_number): 
            if (self.add_number is not None and ph.add_number is not None): 
                if (ph.add_number != self.add_number): 
                    return False
        elif (self.add_number is not None or ph.add_number is not None): 
            if (self.add_number != ph.add_number): 
                return False
        if (self.number is None or ph.number is None): 
            return False
        if (self.number == ph.number): 
            return True
        if (typ != ReferentsEqualType.DIFFERENTTEXTS): 
            if (LanguageHelper.ends_with(self.number, ph.number) or LanguageHelper.ends_with(ph.number, self.number)): 
                return True
        return False
    
    def can_be_general_for(self, obj : 'Referent') -> bool:
        if (not self.__can_be_equal(obj, ReferentsEqualType.WITHINONETEXT, True)): 
            return False
        ph = Utils.asObjectOrNull(obj, PhoneReferent)
        if (self.country_code is not None and ph.country_code is None): 
            return False
        if (self.add_number is None): 
            if (ph.add_number is not None): 
                return True
        elif (ph.add_number is None): 
            return False
        if (LanguageHelper.ends_with(ph.number, self.number)): 
            return True
        return False
    
    def merge_slots(self, obj : 'Referent', merge_statistic : bool=True) -> None:
        ph = Utils.asObjectOrNull(obj, PhoneReferent)
        if (ph is None): 
            return
        if (ph.country_code is not None and self.country_code is None): 
            self.country_code = ph.country_code
        if (ph.number is not None and LanguageHelper.ends_with(ph.number, self.number)): 
            self.number = ph.number
    
    def _correct(self) -> None:
        if (self.kind == PhoneKind.UNDEFINED): 
            if (self.find_slot(PhoneReferent.ATTR_ADDNUMBER, None, True) is not None): 
                self.kind = PhoneKind.WORK
            elif (self.country_code is None or self.country_code == "7"): 
                num = self.number
                if (len(num) == 10 and num[0] == '9'): 
                    self.kind = PhoneKind.MOBILE