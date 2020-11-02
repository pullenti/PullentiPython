# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
import typing
from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.date.DateReferent import DateReferent
from pullenti.ner.org.OrganizationReferent import OrganizationReferent
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.Referent import Referent
from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.titlepage.internal.MetaTitleInfo import MetaTitleInfo
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.core.Termin import Termin

class TitlePageReferent(Referent):
    """ Сущность, описывающая информацию из заголовков статей, книг, диссертация и пр.
    
    """
    
    def __init__(self, name : str=None) -> None:
        super().__init__(Utils.ifNotNull(name, TitlePageReferent.OBJ_TYPENAME))
        self.instance_of = MetaTitleInfo._global_meta
    
    OBJ_TYPENAME = "TITLEPAGE"
    """ Имя типа сущности TypeName ("TITLEPAGE") """
    
    ATTR_NAME = "NAME"
    """ Имя атрибута - наименование """
    
    ATTR_TYPE = "TYPE"
    """ Имя атрибута - тип """
    
    ATTR_AUTHOR = "AUTHOR"
    """ Имя атрибута - автор (PersonReferent) """
    
    ATTR_SUPERVISOR = "SUPERVISOR"
    """ Имя атрибута - руководитель (PersonReferent) """
    
    ATTR_EDITOR = "EDITOR"
    """ Имя атрибута - редактор (PersonReferent) """
    
    ATTR_CONSULTANT = "CONSULTANT"
    """ Имя атрибута - консультант (PersonReferent) """
    
    ATTR_OPPONENT = "OPPONENT"
    """ Имя атрибута - оппонент (PersonReferent) """
    
    ATTR_TRANSLATOR = "TRANSLATOR"
    """ Имя атрибута - переводчик (PersonReferent) """
    
    ATTR_AFFIRMANT = "AFFIRMANT"
    """ Имя атрибута - утвердивший (PersonReferent) """
    
    ATTR_ORG = "ORGANIZATION"
    """ Имя атрибута - организации (OrganizationReferent) """
    
    ATTR_STUDENTYEAR = "STUDENTYEAR"
    """ Имя атрибута - курс студента """
    
    ATTR_DATE = "DATE"
    """ Имя атрибута - дата (год) """
    
    ATTR_CITY = "CITY"
    """ Имя атрибута - город (GeoReferent) """
    
    ATTR_SPECIALITY = "SPECIALITY"
    """ Имя атрибута - специальность (для диссертаций) """
    
    ATTR_ATTR = "ATTR"
    """ Имя атрибута - дополнительный атрибут """
    
    def to_string(self, short_variant : bool, lang : 'MorphLang', lev : int=0) -> str:
        res = io.StringIO()
        str0_ = self.get_string_value(TitlePageReferent.ATTR_NAME)
        print("\"{0}\"".format(Utils.ifNotNull(str0_, "?")), end="", file=res, flush=True)
        if (not short_variant): 
            for r in self.slots: 
                if (r.type_name == TitlePageReferent.ATTR_TYPE): 
                    print(" ({0})".format(r.value), end="", file=res, flush=True)
                    break
            for r in self.slots: 
                if (r.type_name == TitlePageReferent.ATTR_AUTHOR and (isinstance(r.value, Referent))): 
                    print(", {0}".format(r.value.to_string(True, lang, 0)), end="", file=res, flush=True)
        if (self.city is not None and not short_variant): 
            print(", {0}".format(self.city.to_string(True, lang, 0)), end="", file=res, flush=True)
        if (self.date is not None): 
            if (not short_variant): 
                print(", {0}".format(self.date.to_string(True, lang, 0)), end="", file=res, flush=True)
            else: 
                print(", {0}".format(self.date.year), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @property
    def types(self) -> typing.List[str]:
        """ Список типов """
        res = list()
        for s in self.slots: 
            if (s.type_name == TitlePageReferent.ATTR_TYPE): 
                res.append(str(s.value))
        return res
    
    def _add_type(self, typ : str) -> None:
        if (not Utils.isNullOrEmpty(typ)): 
            self.add_slot(TitlePageReferent.ATTR_TYPE, typ.lower(), False, 0)
            self.__correct_data()
    
    @property
    def names(self) -> typing.List[str]:
        """ Названия (одно или несколько) """
        res = list()
        for s in self.slots: 
            if (s.type_name == TitlePageReferent.ATTR_NAME): 
                res.append(str(s.value))
        return res
    
    def _add_name(self, begin : 'Token', end : 'Token') -> 'Termin':
        if (BracketHelper.can_be_start_of_sequence(begin, True, False)): 
            br = BracketHelper.try_parse(begin, BracketParseAttr.NO, 100)
            if (br is not None and br.end_token == end): 
                begin = begin.next0_
                end = end.previous
        val = MiscHelper.get_text_value(begin, end, Utils.valToEnum((GetTextAttr.KEEPREGISTER) | (GetTextAttr.KEEPQUOTES), GetTextAttr))
        if (val is None): 
            return None
        if (val.endswith(".") and not val.endswith("..")): 
            val = val[0:0+len(val) - 1].strip()
        self.add_slot(TitlePageReferent.ATTR_NAME, val, False, 0)
        return Termin(val.upper())
    
    def __correct_data(self) -> None:
        pass
    
    @property
    def date(self) -> 'DateReferent':
        """ Дата """
        return Utils.asObjectOrNull(self.get_slot_value(TitlePageReferent.ATTR_DATE), DateReferent)
    @date.setter
    def date(self, value) -> 'DateReferent':
        if (value is None): 
            return value
        if (self.date is None): 
            self.add_slot(TitlePageReferent.ATTR_DATE, value, True, 0)
            return value
        if (self.date.month > 0 and value.month == 0): 
            return value
        if (self.date.day > 0 and value.day == 0): 
            return value
        self.add_slot(TitlePageReferent.ATTR_DATE, value, True, 0)
        return value
    
    @property
    def student_year(self) -> int:
        """ Номер курса (для студентов) """
        return self.get_int_value(TitlePageReferent.ATTR_STUDENTYEAR, 0)
    @student_year.setter
    def student_year(self, value) -> int:
        self.add_slot(TitlePageReferent.ATTR_STUDENTYEAR, value, True, 0)
        return value
    
    @property
    def org0_(self) -> 'OrganizationReferent':
        """ Организация """
        return Utils.asObjectOrNull(self.get_slot_value(TitlePageReferent.ATTR_ORG), OrganizationReferent)
    @org0_.setter
    def org0_(self, value) -> 'OrganizationReferent':
        self.add_slot(TitlePageReferent.ATTR_ORG, value, True, 0)
        return value
    
    @property
    def city(self) -> 'GeoReferent':
        """ Город """
        return Utils.asObjectOrNull(self.get_slot_value(TitlePageReferent.ATTR_CITY), GeoReferent)
    @city.setter
    def city(self, value) -> 'GeoReferent':
        self.add_slot(TitlePageReferent.ATTR_CITY, value, True, 0)
        return value
    
    @property
    def speciality(self) -> str:
        """ Специальность """
        return self.get_string_value(TitlePageReferent.ATTR_SPECIALITY)
    @speciality.setter
    def speciality(self, value) -> str:
        self.add_slot(TitlePageReferent.ATTR_SPECIALITY, value, True, 0)
        return value