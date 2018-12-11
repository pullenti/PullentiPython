# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

from pullenti.unisharp.Utils import Utils

from pullenti.ner.Referent import Referent
from pullenti.ner.ReferentClass import ReferentClass
from pullenti.ner.date.DateReferent import DateReferent
from pullenti.ner.date.internal.MetaDateRange import MetaDateRange

class DateRangeReferent(Referent):
    """ Сущность, представляющая диапазон дат """
    
    def __init__(self) -> None:
        super().__init__(DateRangeReferent.OBJ_TYPENAME)
        self.instance_of = MetaDateRange.GLOBAL_META
    
    OBJ_TYPENAME = "DATERANGE"
    
    ATTR_FROM = "FROM"
    
    ATTR_TO = "TO"
    
    @property
    def date_from(self) -> 'DateReferent':
        """ Начало диапазона """
        return Utils.asObjectOrNull(self.getSlotValue(DateRangeReferent.ATTR_FROM), DateReferent)
    @date_from.setter
    def date_from(self, value) -> 'DateReferent':
        self.addSlot(DateRangeReferent.ATTR_FROM, value, True, 0)
        return value
    
    @property
    def date_to(self) -> 'DateReferent':
        """ Конец диапазона """
        return Utils.asObjectOrNull(self.getSlotValue(DateRangeReferent.ATTR_TO), DateReferent)
    @date_to.setter
    def date_to(self, value) -> 'DateReferent':
        self.addSlot(DateRangeReferent.ATTR_TO, value, True, 0)
        return value
    
    def toString(self, short_variant : bool, lang : 'MorphLang'=None, lev : int=0) -> str:
        fr = (None if self.date_from is None else self.date_from._ToString(short_variant, lang, lev, 1))
        to = (None if self.date_to is None else self.date_to._ToString(short_variant, lang, lev, 2))
        if (fr is not None and to is not None): 
            return "{0} {1}".format(fr, (to if self.date_to.century > 0 and self.date_to.year == 0 else to.lower()))
        if (fr is not None): 
            return str(fr)
        if (to is not None): 
            return to
        return "{0} ? по ?".format(('з' if lang.is_ua else 'с'))
    
    def canBeEquals(self, obj : 'Referent', typ : 'EqualType') -> bool:
        dr = Utils.asObjectOrNull(obj, DateRangeReferent)
        if (dr is None): 
            return False
        if (self.date_from is not None): 
            if (not self.date_from.canBeEquals(dr.date_from, typ)): 
                return False
        elif (dr.date_from is not None): 
            return False
        if (self.date_to is not None): 
            if (not self.date_to.canBeEquals(dr.date_to, typ)): 
                return False
        elif (dr.date_to is not None): 
            return False
        return True
    
    @property
    def quarter_number(self) -> int:
        """ Проверка, что диапазон задаёт квартал, возвращает номер 1..4 """
        if (self.date_from is None or self.date_to is None or self.date_from.year != self.date_to.year): 
            return 0
        m1 = self.date_from.month
        m2 = self.date_to.month
        if (m1 == 1 and m2 == 3): 
            return 1
        if (m1 == 4 and m2 == 6): 
            return 2
        if (m1 == 7 and m2 == 9): 
            return 3
        if (m1 == 10 and m2 == 12): 
            return 4
        return 0
    
    @property
    def halfyear_number(self) -> int:
        """ Проверка, что диапазон задаёт полугодие, возвращает номер 1..2 """
        if (self.date_from is None or self.date_to is None or self.date_from.year != self.date_to.year): 
            return 0
        m1 = self.date_from.month
        m2 = self.date_to.month
        if (m1 == 1 and m2 == 6): 
            return 1
        if (m1 == 7 and m2 == 12): 
            return 2
        return 0
    
    @staticmethod
    def _new728(_arg1 : 'DateReferent', _arg2 : 'DateReferent') -> 'DateRangeReferent':
        res = DateRangeReferent()
        res.date_from = _arg1
        res.date_to = _arg2
        return res
    
    @staticmethod
    def _new733(_arg1 : 'DateReferent') -> 'DateRangeReferent':
        res = DateRangeReferent()
        res.date_to = _arg1
        return res