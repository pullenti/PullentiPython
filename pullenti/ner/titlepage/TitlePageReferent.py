# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import io
import typing
from pullenti.ntopy.Utils import Utils
from pullenti.ner.Referent import Referent
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.core.GetTextAttr import GetTextAttr


class TitlePageReferent(Referent):
    """ Сущность, описывающая информацию из заголовков статей, книг, диссертация и пр. """
    
    def __init__(self, name : str=None) -> None:
        from pullenti.ner.titlepage.internal.MetaTitleInfo import MetaTitleInfo
        super().__init__(Utils.ifNotNull(name, TitlePageReferent.OBJ_TYPENAME))
        self.instance_of = MetaTitleInfo._global_meta
    
    OBJ_TYPENAME = "TITLEPAGE"
    
    ATTR_NAME = "NAME"
    
    ATTR_TYPE = "TYPE"
    
    ATTR_AUTHOR = "AUTHOR"
    
    ATTR_SUPERVISOR = "SUPERVISOR"
    
    ATTR_EDITOR = "EDITOR"
    
    ATTR_CONSULTANT = "CONSULTANT"
    
    ATTR_OPPONENT = "OPPONENT"
    
    ATTR_TRANSLATOR = "TRANSLATOR"
    
    ATTR_AFFIRMANT = "AFFIRMANT"
    
    ATTR_ORG = "ORGANIZATION"
    
    ATTR_DEP = "DEPARTMENT"
    
    ATTR_STUDENTYEAR = "STUDENTYEAR"
    
    ATTR_DATE = "DATE"
    
    ATTR_CITY = "CITY"
    
    ATTR_SPECIALITY = "SPECIALITY"
    
    ATTR_ATTR = "ATTR"
    
    def to_string(self, short_variant : bool, lang : 'MorphLang', lev : int=0) -> str:
        res = Utils.newStringIO(None)
        str0 = self.get_string_value(TitlePageReferent.ATTR_NAME)
        print("\"{0}\"".format(Utils.ifNotNull(str0, "?")), end="", file=res, flush=True)
        if (not short_variant): 
            for r in self.slots: 
                if (r.type_name == TitlePageReferent.ATTR_TYPE): 
                    print(" ({0})".format(r.value), end="", file=res, flush=True)
                    break
            for r in self.slots: 
                if (r.type_name == TitlePageReferent.ATTR_AUTHOR and isinstance(r.value, Referent)): 
                    print(", {0}".format((r.value if isinstance(r.value, Referent) else None).to_string(True, lang, 0)), end="", file=res, flush=True)
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
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.core.Termin import Termin
        if (BracketHelper.can_be_start_of_sequence(begin, True, False)): 
            br = BracketHelper.try_parse(begin, BracketParseAttr.NO, 100)
            if (br is not None and br.end_token == end): 
                begin = begin.next0
                end = end.previous
        val = MiscHelper.get_text_value(begin, end, Utils.valToEnum(GetTextAttr.KEEPREGISTER | GetTextAttr.KEEPQUOTES, GetTextAttr))
        if (val is None): 
            return None
        if (val.endswith(".") and not val.endswith("..")): 
            val = val[0 : (len(val) - 1)].strip()
        self.add_slot(TitlePageReferent.ATTR_NAME, val, False, 0)
        return Termin(val.upper())
    
    def __correct_data(self) -> None:
        pass
    
    @property
    def date(self) -> 'DateReferent':
        """ Дата """
        from pullenti.ner.date.DateReferent import DateReferent
        return (self.get_value(TitlePageReferent.ATTR_DATE) if isinstance(self.get_value(TitlePageReferent.ATTR_DATE), DateReferent) else None)
    
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
    def org(self) -> 'OrganizationReferent':
        """ Организация """
        from pullenti.ner.org.OrganizationReferent import OrganizationReferent
        return (self.get_value(TitlePageReferent.ATTR_ORG) if isinstance(self.get_value(TitlePageReferent.ATTR_ORG), OrganizationReferent) else None)
    
    @org.setter
    def org(self, value) -> 'OrganizationReferent':
        self.add_slot(TitlePageReferent.ATTR_ORG, value, True, 0)
        return value
    
    @property
    def city(self) -> 'GeoReferent':
        """ Город """
        from pullenti.ner.geo.GeoReferent import GeoReferent
        return (self.get_value(TitlePageReferent.ATTR_CITY) if isinstance(self.get_value(TitlePageReferent.ATTR_CITY), GeoReferent) else None)
    
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