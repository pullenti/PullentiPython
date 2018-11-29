# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
import typing
from pullenti.unisharp.Utils import Utils
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
    
    def toString(self, short_variant : bool, lang : 'MorphLang', lev : int=0) -> str:
        res = io.StringIO()
        str0_ = self.getStringValue(TitlePageReferent.ATTR_NAME)
        print("\"{0}\"".format(Utils.ifNotNull(str0_, "?")), end="", file=res, flush=True)
        if (not short_variant): 
            for r in self.slots: 
                if (r.type_name == TitlePageReferent.ATTR_TYPE): 
                    print(" ({0})".format(r.value), end="", file=res, flush=True)
                    break
            for r in self.slots: 
                if (r.type_name == TitlePageReferent.ATTR_AUTHOR and (isinstance(r.value, Referent))): 
                    print(", {0}".format((Utils.asObjectOrNull(r.value, Referent)).toString(True, lang, 0)), end="", file=res, flush=True)
        if (self.city is not None and not short_variant): 
            print(", {0}".format(self.city.toString(True, lang, 0)), end="", file=res, flush=True)
        if (self.date is not None): 
            if (not short_variant): 
                print(", {0}".format(self.date.toString(True, lang, 0)), end="", file=res, flush=True)
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
    
    def _addType(self, typ : str) -> None:
        if (not Utils.isNullOrEmpty(typ)): 
            self.addSlot(TitlePageReferent.ATTR_TYPE, typ.lower(), False, 0)
            self.__correctData()
    
    @property
    def names(self) -> typing.List[str]:
        """ Названия (одно или несколько) """
        res = list()
        for s in self.slots: 
            if (s.type_name == TitlePageReferent.ATTR_NAME): 
                res.append(str(s.value))
        return res
    
    def _addName(self, begin : 'Token', end : 'Token') -> 'Termin':
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.core.Termin import Termin
        if (BracketHelper.canBeStartOfSequence(begin, True, False)): 
            br = BracketHelper.tryParse(begin, BracketParseAttr.NO, 100)
            if (br is not None and br.end_token == end): 
                begin = begin.next0_
                end = end.previous
        val = MiscHelper.getTextValue(begin, end, Utils.valToEnum((GetTextAttr.KEEPREGISTER) | (GetTextAttr.KEEPQUOTES), GetTextAttr))
        if (val is None): 
            return None
        if (val.endswith(".") and not val.endswith("..")): 
            val = val[0:0+len(val) - 1].strip()
        self.addSlot(TitlePageReferent.ATTR_NAME, val, False, 0)
        return Termin(val.upper())
    
    def __correctData(self) -> None:
        pass
    
    @property
    def date(self) -> 'DateReferent':
        """ Дата """
        from pullenti.ner.date.DateReferent import DateReferent
        return Utils.asObjectOrNull(self.getSlotValue(TitlePageReferent.ATTR_DATE), DateReferent)
    @date.setter
    def date(self, value) -> 'DateReferent':
        if (value is None): 
            return value
        if (self.date is None): 
            self.addSlot(TitlePageReferent.ATTR_DATE, value, True, 0)
            return value
        if (self.date.month > 0 and value.month == 0): 
            return value
        if (self.date.day > 0 and value.day == 0): 
            return value
        self.addSlot(TitlePageReferent.ATTR_DATE, value, True, 0)
        return value
    
    @property
    def student_year(self) -> int:
        """ Номер курса (для студентов) """
        return self.getIntValue(TitlePageReferent.ATTR_STUDENTYEAR, 0)
    @student_year.setter
    def student_year(self, value) -> int:
        self.addSlot(TitlePageReferent.ATTR_STUDENTYEAR, value, True, 0)
        return value
    
    @property
    def org0_(self) -> 'OrganizationReferent':
        """ Организация """
        from pullenti.ner.org.OrganizationReferent import OrganizationReferent
        return Utils.asObjectOrNull(self.getSlotValue(TitlePageReferent.ATTR_ORG), OrganizationReferent)
    @org0_.setter
    def org0_(self, value) -> 'OrganizationReferent':
        self.addSlot(TitlePageReferent.ATTR_ORG, value, True, 0)
        return value
    
    @property
    def city(self) -> 'GeoReferent':
        """ Город """
        from pullenti.ner.geo.GeoReferent import GeoReferent
        return Utils.asObjectOrNull(self.getSlotValue(TitlePageReferent.ATTR_CITY), GeoReferent)
    @city.setter
    def city(self, value) -> 'GeoReferent':
        self.addSlot(TitlePageReferent.ATTR_CITY, value, True, 0)
        return value
    
    @property
    def speciality(self) -> str:
        """ Специальность """
        return self.getStringValue(TitlePageReferent.ATTR_SPECIALITY)
    @speciality.setter
    def speciality(self, value) -> str:
        self.addSlot(TitlePageReferent.ATTR_SPECIALITY, value, True, 0)
        return value